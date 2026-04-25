"""
scan_service.py
---------------
All business logic for threat detection and analysis.

Implements:
  - analyze_url()
  - analyze_phone()
  - analyze_text()
  - get_user_scan_history()
"""

import re
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session
import os

from tld import get_tld
print(f"[scan_service] Current working directory: {os.getcwd()}")
from app.ml import text_classifier
from app.ml import url_classifier
from app.models.lookup import InputType, ReportStatus, ThreatCategory, URLClassification
from app.models.scan import Scan, PhoneNumber, Report


# ──────────────────────────────────────────────
# HELPERS: CATEGORY ORDERING
# ──────────────────────────────────────────────

_CATEGORY_ORDER: dict[ThreatCategory, int] = {
    ThreatCategory.NO_DATA: -1,
    ThreatCategory.SAFE: 0,
    ThreatCategory.SUSPICIOUS: 1,
    ThreatCategory.HIGH_RISK: 2,
}


def _max_category(*categories: ThreatCategory) -> ThreatCategory:
    """
    Return the highest-severity category from the provided values.
    NO_DATA signals are ignored; if all signals are NO_DATA, returns NO_DATA.
    """
    valid = [c for c in categories if c != ThreatCategory.NO_DATA]
    if not valid:
        return ThreatCategory.NO_DATA
    return max(valid, key=lambda c: _CATEGORY_ORDER[c])


# ──────────────────────────────────────────────
# HELPERS: COMMUNITY SIGNAL
# ──────────────────────────────────────────────

def _community_category_for_value(
    db: Session, input_type: InputType, input_value: str
) -> ThreatCategory:
    """
    Derive a community-based ThreatCategory from VERIFIED_SCAM / SAFE reports only.
    """
    if input_type == InputType.URL:
        def process_tld(url):
            try:
                res = get_tld(url, as_object=True, fix_protocol=True)
                return res.parsed_url.netloc
            except:
                return None
        domain = process_tld(input_value)
        reports = (
            db.query(Report)
            .filter(
                Report.input_type == input_type,
                Report.input_value.ilike(f"%{domain}%"),
                Report.status.in_([ReportStatus.VERIFIED_SCAM, ReportStatus.SAFE, ReportStatus.UNDER_REVIEW]),
            )
            .all()
        )
    else:
        reports = (
            db.query(Report)
            .filter(
                Report.input_type == input_type,
                Report.input_value == input_value,
                Report.status.in_([ReportStatus.VERIFIED_SCAM, ReportStatus.SAFE, ReportStatus.UNDER_REVIEW]),
            )
            .all()
        )

    if not reports:
        return ThreatCategory.NO_DATA

    scam_count = sum(1 for r in reports if r.status == ReportStatus.VERIFIED_SCAM)
    safe_count = sum(1 for r in reports if r.status == ReportStatus.SAFE)
    under_review_count = sum(1 for r in reports if r.status == ReportStatus.UNDER_REVIEW)
    
    if scam_count > 0 and safe_count == 0:
        return ThreatCategory.HIGH_RISK
    if under_review_count > 0 and safe_count == 0:
        return ThreatCategory.SUSPICIOUS
    if safe_count > 0 and scam_count == 0:
        return ThreatCategory.SAFE
    # Mixed signals → Suspicious
    return ThreatCategory.SUSPICIOUS


# ──────────────────────────────────────────────
# HELPERS: PHONE SPAM RATE → CATEGORY
# ──────────────────────────────────────────────

def _spam_rate_to_category(spam_rate: float) -> ThreatCategory:
    if spam_rate < 0.10:
        return ThreatCategory.SAFE
    if spam_rate <= 0.60:
        return ThreatCategory.SUSPICIOUS
    return ThreatCategory.HIGH_RISK


# ──────────────────────────────────────────────
# HELPERS: URL EXTRACTION
# ──────────────────────────────────────────────

_URL_RE = re.compile(
    r'\b(?:https?://|www\.)[^\s<>"{}|\\^`\[\]]+'   # full URLs
    r'|\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s<>"{}|\\^`\[\]]*)?'  # domains + optional path
)


def _extract_urls(text: str) -> list[str]:
    return _URL_RE.findall(text)


# ──────────────────────────────────────────────
# HELPERS: ARABIC TRANSLATION
# ──────────────────────────────────────────────

def _to_english(text: str) -> tuple[Optional[str], bool]:
    """
    Returns (translated_text, success_flag)

    - If text is English → returns original text, True
    - If translation succeeds → returns translated text, True
    - If translation fails → returns None, False
    """
    try:
        from langdetect import detect
        from deep_translator import GoogleTranslator

        if detect(text) == "en":
            print("[translator] Text detected as English, skipping translation.")
            return text, True

        translated = GoogleTranslator(source="auto", target="en").translate(text)
        if translated:
            print(["[translator] Translation successful."])
            return translated, True
        print(["[translator] Translation failed or returned empty."])
    except Exception:
        pass

    return None, False


# ──────────────────────────────────────────────
# HELPERS: PHONE RECORD UPSERT (for text scans)
# ──────────────────────────────────────────────

def _upsert_phone_counters(
    db: Session, phone_number: str, category: ThreatCategory
) -> None:
    """
    Create or update the PhoneNumber record for a sender phone.
    Called when a text analysis includes a phone_number.
    """
    record = (
        db.query(PhoneNumber)
        .filter(PhoneNumber.number == phone_number)
        .first()
    )
    if not record:
        record = PhoneNumber(number=phone_number)
        db.add(record)
        db.flush()

    record.total_reports += 1
    record.last_seen = datetime.now(timezone.utc)

    if category in (ThreatCategory.HIGH_RISK, ThreatCategory.SUSPICIOUS):
        record.spam_reports += 1
    elif category == ThreatCategory.SAFE:
        record.ham_reports += 1


def _analyze_single_url(db: Session, url: str) -> dict:
    """
    Analyze a single URL (used inside text analysis).

    Returns:
      - full analysis
      - "found": whether any signal exists
    """
    if not url.startswith(("http://", "https://")):
        return {
            "url": url,
            "found": False,
            "category": ThreatCategory.SUSPICIOUS.value,
            "explanation": "Invalid URL format, enter complete URL with http:// or https://",
            "contributing_factors": ["input_validation"],
        }
    signals: list[ThreatCategory] = []
    contributing_factors: list[str] = []

    # ========================
    # 🔹 Community FIRST (same as main service)
    # ========================
    comm_cat = _community_category_for_value(db, InputType.URL, url)

    if comm_cat in [ThreatCategory.HIGH_RISK, ThreatCategory.SAFE]:
        return {
            "url": url,
            "found": True,

            "ml_result": None,
            "community_result": comm_cat.value,

            "category": comm_cat.value,
            "explanation": "Verified by admins based on user reports.",
            "contributing_factors": ["community_reports"],
        }

    # ========================
    # 🔹 ML
    # ========================
    try:
        ml_result = url_classifier.predict_url(url)
        ml_cat = ml_result["category"]

        signals.append(ml_cat)
        contributing_factors.append("ml_model")

        ml_detail = {
            "category": ml_cat.value,
            "risk_score": ml_result["malicious_score"],
            "reasons": ml_result["reason"],
        }

    except Exception as e:
        ml_cat = ThreatCategory.NO_DATA
        ml_detail = {
            "category": ThreatCategory.NO_DATA.value,
            "risk_score": 0.0,
            "reasons": [f"ml_error: {str(e)}"],
        }

    # ========================
    # 🔹 Add community if usable
    # ========================
    if comm_cat != ThreatCategory.NO_DATA:
        signals.append(comm_cat)
        contributing_factors.append("community_reports")

    # ========================
    # 🔹 Final decision
    # ========================
    valid_signals = [s for s in signals if s != ThreatCategory.NO_DATA]

    if not valid_signals:
        final_category = ThreatCategory.NO_DATA
        explanation = "No data available for this URL."
        found = False

    else:
        found = True

        suspicious_count = sum(
            1 for s in valid_signals if s == ThreatCategory.SUSPICIOUS
        )

        base_max = max(valid_signals, key=lambda c: _CATEGORY_ORDER[c])

        if suspicious_count >= 2 and base_max == ThreatCategory.SUSPICIOUS:
            final_category = ThreatCategory.HIGH_RISK
            explanation = (
                "Both ML and community marked Suspicious; escalated to High Risk."
            )
        else:
            final_category = base_max

            parts: list[str] = []

            if ml_cat != ThreatCategory.NO_DATA:
                parts.append(
                    f"ML: {ml_cat.value} (risk={ml_detail['risk_score']:.2f})"
                )

            if comm_cat != ThreatCategory.NO_DATA:
                parts.append(f"Community: {comm_cat.value}")

            explanation = ". ".join(parts) + "."

    # ========================
    # 🔹 Return
    # ========================
    return {
        "url": url,
        "found": found,

        "ml_result": ml_detail,
        "community_result": comm_cat.value,

        "category": final_category.value,
        "explanation": explanation,
        "contributing_factors": contributing_factors,
    }

# ──────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────
def analyze_url(db: Session, user_id: int, url: str) -> dict:
    """
    Analyze a URL using:
      1. ML classifier (primary signal)
      2. Community reports (secondary signal)

    Final category rules:
      - final = max(all signals)
      - If both signals == SUSPICIOUS → HIGH_RISK
      - If no data → NO_DATA
    """
    signals: list[ThreatCategory] = []
    contributing_factors: list[str] = []

        # 3. Community analysis
    comm_cat = _community_category_for_value(db, InputType.URL, url)
    comm_detail = None

    if comm_cat == ThreatCategory.HIGH_RISK or comm_cat == ThreatCategory.SAFE:
        signals.append(comm_cat)
        contributing_factors.append("community_reports")
        scan = Scan(
            user_id=user_id,
            input_type=InputType.URL,
            input_value=url,
            ml_confidence=None,
            threat_category=comm_cat,
            analysis_details=None,
        )

        db.add(scan)
        db.commit()
        db.refresh(scan)
        return {
            "scan_id": scan.id,
            "final_category": scan.threat_category,
            "ml_risk_score": scan.ml_confidence,
            "ml_probabilities": None,
            "explanation": "Verified by our admins based on user reports.",
            "contributing_factors": contributing_factors,
            "analysis_details": None,
        }
        
    # 2. ML analysis
    ml_result = None
    ml_category = ThreatCategory.NO_DATA
    try:
        ml_result = url_classifier.predict_url(url)

        ml_category = ml_result["category"]
        signals.append(ml_category)
        contributing_factors.append("ml_model")

        ml_detail = {
            "category": ml_category.value,
            "risk_score": ml_result["malicious_score"],
            "reasons": ml_result["reason"],
        }

    except Exception as e:
        print(f"[scan url service]-ERROR did not run model {e}")
        ml_detail = {
            "category": ThreatCategory.NO_DATA.value,
            "risk_score": 0.0,
            "probabilities": None,
            "reasons": [f"ml_error: {str(e)}"],
        }


    # 3. Final decision (same pattern as text analyzer)
    valid_signals = [s for s in signals if s != ThreatCategory.NO_DATA]

    if not valid_signals:
        final_category = ThreatCategory.NO_DATA
        explanation = "Unable to determine — no data found for this URL."
    else:
        suspicious_count = sum(
            1 for s in valid_signals if s == ThreatCategory.SUSPICIOUS
        )

        base_max = max(valid_signals, key=lambda c: _CATEGORY_ORDER[c])

        if suspicious_count >= 2 and base_max == ThreatCategory.SUSPICIOUS:
            final_category = ThreatCategory.HIGH_RISK
            explanation = (
                "Both ML model and community signals are Suspicious; "
                "escalated to High Risk."
            )
        else:
            final_category = base_max

            parts: list[str] = []

            if ml_category != ThreatCategory.NO_DATA:
                parts.append(
                    f"ML model: {ml_category.value} "
                    f"(risk={ml_result['malicious_score']:.2f})"
                )

            if comm_cat != ThreatCategory.NO_DATA:
                parts.append(f"Community reports: {comm_cat.value}")

            explanation = ". ".join(parts) + "."

    # 4. Assemble analysis details
    analysis_details = {
        "ml_result": ml_detail,
        "community_result": comm_detail,
        "explanation": explanation,
        "contributing_factors": contributing_factors,
    }

    # 5. Persist scan
    scan = Scan(
        user_id=user_id,
        input_type=InputType.URL,
        input_value=url,
        ml_confidence=ml_result["malicious_score"] if ml_result else None,
        threat_category=final_category,
        analysis_details=analysis_details,
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    # 6. Return response (same style as text analyzer)
    return {
        "scan_id": scan.id,
        "final_category": final_category,
        "ml_risk_score": ml_result["malicious_score"] if ml_result else None,
        "ml_probabilities": None,
        "explanation": explanation,
        "contributing_factors": contributing_factors,
        "analysis_details": analysis_details,
    }


def analyze_phone(
    db: Session,
    user_id: int,
    phone_number: str,
) -> dict:
    """
    Analyze input using raw Report rows (no aggregation).
    """

    normalized_value = phone_number.strip().lower()

    reports = (
        db.query(Report)
        .filter(
            Report.input_type == InputType.PHONE,
            Report.input_value == normalized_value,
            Report.status.in_([
                ReportStatus.VERIFIED_SCAM,
                ReportStatus.SAFE,
            ]),
        )
        .all()
    )

    # ========================
    # 🔥 No data case
    # ========================
    if not reports:
        final_category = ThreatCategory.NO_DATA
        explanation = "No data found for this input."
        contributing_factors = []

        analysis_details = {
            "total_reports": 0,
            "spam_reports": 0,
            "ham_reports": 0,
            "spam_rate": None,
            "explanation": explanation,
            "contributing_factors": [],
        }

    else:
        # ========================
        # 🔢 Manual counting
        # ========================
        spam_reports = 0
        ham_reports = 0

        for report in reports:
            if report.status == ReportStatus.VERIFIED_SCAM:
                spam_reports += 1
            elif report.status == ReportStatus.SAFE:
                ham_reports += 1

        total_reports = len(reports)

        # ========================
        # 🔥 Hard Rules
        # ========================

        # ✅ ONLY SAFE
        if ham_reports > 0 and spam_reports == 0:
            final_category = ThreatCategory.SAFE
            explanation = f"{ham_reports} safe report(s), no scam reports."

        # ❌ ONLY SCAM
        elif spam_reports > 0 and ham_reports == 0:
            final_category = ThreatCategory.HIGH_RISK
            explanation = f"{spam_reports} scam report(s), no safe reports."

        # ⚖️ MIXED
        else:
            spam_rate = spam_reports / total_reports

            final_category = _spam_rate_to_category(spam_rate)

            explanation = (
                f"Mixed reports: {spam_reports} scam / {ham_reports} safe "
                f"({spam_rate:.0%} spam rate)."
            )

        contributing_factors = ["community_reports"]

        analysis_details = {
            "total_reports": total_reports,
            "spam_reports": spam_reports,
            "ham_reports": ham_reports,
            "spam_rate": (spam_reports / total_reports) if total_reports else None,
            "explanation": explanation,
            "contributing_factors": contributing_factors,
        }

    # ========================
    # 💾 Save Scan
    # ========================
    scan = Scan(
        user_id=user_id,
        input_type=InputType.PHONE,
        input_value=normalized_value,
        ml_confidence=None,
        threat_category=final_category,
        analysis_details=analysis_details,
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    # ========================
    # 📦 Return
    # ========================
    return {
        "scan_id": scan.id,
        "final_category": final_category,
        "ml_risk_score": None,
        "ml_probabilities": None,
        "explanation": explanation,
        "contributing_factors": contributing_factors,
        "analysis_details": analysis_details,
    }


def analyze_text(
    db: Session,
    user_id: int,
    message: str,
    phone_number: Optional[str]
) -> dict:
    """
    Analyze a text message.

    Signals combined:
      1. ML classifier (mandatory)
      2. URL analysis for each URL found in the message
      3. Phone analysis if a sender phone number is provided

    Final category rules:
      - final = max(all present signals)
      - If ≥2 signals == SUSPICIOUS and max is still SUSPICIOUS → HIGH_RISK
      - If all signals == NO_DATA → "Unable to determine — no data found"
    """
    # 1. Translate non-English (incl. Arabic) to English before classifier
    translated_message, translation_ok = _to_english(message)

    signals: list[ThreatCategory] = []
    contributing_factors: list[str] = []
    ml_detail = None

    # 2. run classifier if translation succeeded
    if translation_ok:
        print(f"[scan_service] translation ok, running classifier on message")
        ml_result = text_classifier.predict_text(translated_message)

        ml_category: ThreatCategory = ml_result["category"]
        ml_risk_score: float = ml_result["risk_score"]

        signals.append(ml_category)
        contributing_factors.append("ml_model")

        ml_detail = {
            "category": ml_category.value,
            "risk_score": ml_risk_score,
            "probabilities": ml_result["probabilities"],
            "reasons": ml_result["reasons"],
        }
    else:
        # log or track this
        ml_detail = {
            "category": "NO_DATA",
            "risk_score": 0.0,
            "probabilities": None,
            "reasons": ["translation_failed"],
        }

    # 3. URL analysis
    urls = _extract_urls(message)
    url_details: list[dict] = []
    for url in urls:
        result = _analyze_single_url(db, url)
        url_details.append(result)
        url_cat = ThreatCategory(result["category"])
        if url_cat != ThreatCategory.NO_DATA:
            signals.append(url_cat)
            if "url_analysis" not in contributing_factors:
                contributing_factors.append("url_analysis")

    # 4. Phone analysis (UPDATED)
    phone_detail: Optional[dict] = None
    phone_category: Optional[ThreatCategory] = None

    if phone_number:
        phone_result = analyze_phone(db, user_id, phone_number)

        phone_category = phone_result["final_category"]

        phone_detail = {
            "category": phone_category.value,
            "analysis_details": phone_result["analysis_details"],
        }

        if phone_category != ThreatCategory.NO_DATA:
            signals.append(phone_category)
            contributing_factors.append("phone_analysis")

    # 5. Determine final category
    valid_signals = [s for s in signals if s != ThreatCategory.NO_DATA]

    if not valid_signals:
        final_category = ThreatCategory.NO_DATA
        explanation = "Unable to determine — no data found."
    else:
        suspicious_count = sum(
            1 for s in valid_signals if s == ThreatCategory.SUSPICIOUS
        )
        base_max = max(valid_signals, key=lambda c: _CATEGORY_ORDER[c])

        if suspicious_count >= 2 and base_max == ThreatCategory.SUSPICIOUS:
            final_category = ThreatCategory.HIGH_RISK
            explanation = (
                "Two or more signals independently returned Suspicious; "
                "escalated to High Risk."
            )
        else:
            final_category = base_max
            parts: list[str] = []
            if ml_category != ThreatCategory.NO_DATA:
                parts.append(f"ML model: {ml_category.value}")
            active_url_cats = [
                d["category"]
                for d in url_details
                if d["category"] != ThreatCategory.NO_DATA.value
            ]
            if active_url_cats:
                parts.append(f"URL analysis: {', '.join(active_url_cats)}")
            if phone_category and phone_category != ThreatCategory.NO_DATA:
                parts.append(f"Phone analysis: {phone_category.value}")
            explanation = (
                ". ".join(parts) + "." if parts else "Analysis complete."
            )

    # 6. Update phone counters if phone was provided
    if phone_number:
        _upsert_phone_counters(db, phone_number, final_category)

    # 7. Assemble analysis_details
    analysis_details: dict = {
        "ml_result": ml_detail,
        "url_analysis": url_details,
        "phone_analysis": phone_detail,
        "explanation": explanation,
        "contributing_factors": contributing_factors,
    }

    # 8. Persist scan
    scan = Scan(
        user_id=user_id,
        input_type=InputType.TEXT_MESSAGE,
        input_value=message,
        phone_number=None,
        ml_confidence=ml_risk_score * 100,
        threat_category=final_category,
        analysis_details=analysis_details,
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    return {
        "scan_id": scan.id,
        "final_category": final_category,
        "ml_risk_score": ml_risk_score,
        "ml_probabilities": ml_result["probabilities"],
        "explanation": explanation,
        "contributing_factors": contributing_factors,
        "analysis_details": analysis_details,
    }


def get_user_scan_history(
    db: Session, user_id: int, page: int, page_size: int
) -> dict:
    """
    Return a paginated list of scans for the current user, newest first.
    page_size is capped at 50.
    """
    page_size = min(page_size, 50)
    offset = (page - 1) * page_size

    query = db.query(Scan).filter(Scan.user_id == user_id)
    total = query.count()
    scans = (
        query.order_by(Scan.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": [
            {
                "id": s.id,
                "input_type": s.input_type,
                "input_value": s.input_value,
                "threat_category": s.threat_category,
                "created_at": s.created_at,
            }
            for s in scans
        ],
    }

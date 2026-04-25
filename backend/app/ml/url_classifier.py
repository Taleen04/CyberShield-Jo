import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from functools import lru_cache
from app.ml.model_loader import load_pipeline
from app.models.lookup import ThreatCategory
from app.ml.Preprocessing import URLDomainExtractor
from tld import get_tld


MODEL_PATH = Path(__file__).parent.parent / "./ml/models/url_phishing_model_pipeline.joblib"
def _validate_url(url: str) -> bool:
    if not url.startswith(("http://", "https://")):
        return False
    try:
        # Basic check for URL format using tld library
        get_tld(url, fix_protocol=True)
        return True
    except Exception as e:
        print(f"[url-classifier] URL validation error: {e}")
        return False

def predict_url(url: str) -> dict:
    if not _validate_url(url):
        return {
            "malicious_score": 0.0,
            "safe_score": 0.0,
            "category": ThreatCategory.SUSPICIOUS,
            "reason": "Invalid URL format, enter complete URL with http:// or https://",
        }
    pipeline = load_pipeline('url')
    
    model_input = [url]

    print(f"[url-classifier] Predicting URL: {url}")
    print(f"[url-classifier] model input: {model_input}") 
    probs = pipeline.predict_proba(model_input)[0]

    # binary assumption:
    safe_prob = probs[0]
    malicious_prob = probs[1]

    print(f"[url-classifier] {probs}")

    # --- thresholds ---
    high_risk_threshold = 0.9
    sus_threshold = 0.10        
    # --- decision logic ---
    if malicious_prob < sus_threshold:
        category = ThreatCategory.SAFE

    elif malicious_prob < high_risk_threshold:
        category = ThreatCategory.SUSPICIOUS

    else:
        category = ThreatCategory.HIGH_RISK

    # --- reasoning ---
    if category == ThreatCategory.SAFE:
        reason = "Low malicious probability"

    elif category == ThreatCategory.SUSPICIOUS:
        reason = f"Uncertain risk zone (p={malicious_prob:.2f})"

    else:
        reason = f"High malicious confidence (p={malicious_prob:.2f})"

    return {
        "malicious_score": float(malicious_prob),
        "safe_score": float(safe_prob),
        "category": category,
        "reason": reason,
    }
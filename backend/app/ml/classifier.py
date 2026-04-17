import joblib
import numpy as np
from pathlib import Path
from functools import lru_cache
import sys
import types
import pandas as pd
from app.ml.model_loader import load_pipeline
from app.models.lookup import ThreatCategory


    
def predict(message: str, message_source: str) -> dict:
    pipeline = load_pipeline()

    model_input = pd.DataFrame({
        "text": [message],
        "source": [message_source]
    })

    probs = pipeline.predict_proba(model_input)[0]
    classes = pipeline.classes_

    prob_dict = dict(zip(classes, probs))

    spam_prob = prob_dict.get("spam", 0.0)
    phishing_prob = prob_dict.get("phishing", 0.0)

    # Combined malicious probability
    risk_score = spam_prob + phishing_prob

    # --- Category based ONLY on your thresholds ---
    if risk_score < 0.10:
        category = ThreatCategory.SAFE
    elif risk_score <= 0.60:
        category = ThreatCategory.SUSPICIOUS
    else:
        category = ThreatCategory.HIGH_RISK

    # --- Reasoning aligned with category ---
    reasons = []

    if category == ThreatCategory.SAFE:
        reasons.append("Very low probability of spam or phishing")
    
    elif category == ThreatCategory.SUSPICIOUS:
        if spam_prob > phishing_prob:
            reasons.append(f"Moderate spam likelihood ({spam_prob:.2f})")
        elif phishing_prob > spam_prob:
            reasons.append(f"Moderate phishing likelihood ({phishing_prob:.2f})")
        else:
            reasons.append("Moderate risk signals detected")

    elif category == ThreatCategory.HIGH_RISK:
        if spam_prob > phishing_prob:
            reasons.append(f"High spam probability ({spam_prob:.2f})")
        elif phishing_prob > spam_prob:
            reasons.append(f"High phishing probability ({phishing_prob:.2f})")
        else:
            reasons.append("High combined malicious probability")

    return {
        "risk_score": float(risk_score),
        "category": category,
        "probabilities": {
            "legit": prob_dict.get("legit", 0.0),
            "spam": spam_prob,
            "phishing": phishing_prob
        },
        "reasons": reasons
    }
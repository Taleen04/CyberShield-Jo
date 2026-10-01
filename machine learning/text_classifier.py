import joblib
import numpy as np
from pathlib import Path
from functools import lru_cache
import sys
import types
import pandas as pd
from app.ml.model_loader import load_pipeline
from app.models.lookup import ThreatCategory
from app.ml.Preprocessing import clean_text
from tensorflow.keras.preprocessing.sequence import pad_sequences
    
def predict_text(message: str) -> dict:
    model, tokenizer, max_len = load_pipeline('text')
    
    # 1. clean
    cleaned = clean_text(message)

    # 2. tokenize (USE FITTED tokenizer)
    seq = tokenizer.texts_to_sequences([cleaned])

    # 3. pad
    padded = pad_sequences(seq, maxlen=max_len, padding='post', truncating='post')

    # 4. predict
    probs = model.predict(padded)[0]

    pred_class = np.argmax(probs)

    print(f"[text-classifier] message: {message}")
    print(f"[text-classifier] Model probabilities: {probs}")


    spam_prob = probs[1]
    phishing_prob = probs[2]

    # Combined malicious probability
    risk_score = spam_prob + phishing_prob

    # --- Category based ONLY on your thresholds ---
    if pred_class == 0:
        category = ThreatCategory.SAFE
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
    print(f"[classifier] Prediction complete: {category}, risk_score={risk_score:.2f}, spam_prob={spam_prob:.2f}, phishing_prob={phishing_prob:.2f}")
    return {
        "risk_score": float(risk_score),
        "category": category,
        "probabilities": {
            "legit": float(probs[0]),
            "spam": float(spam_prob),
            "phishing": float(phishing_prob)
        },
        "reasons": reasons
    }
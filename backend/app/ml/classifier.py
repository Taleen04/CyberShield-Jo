import joblib
import numpy as np
from pathlib import Path
from functools import lru_cache
import sys
import types
import pandas as pd
from app.ml.model_loader import load_pipeline


    
def predict(message: str, message_source: str) -> dict:
    pipeline = load_pipeline()

    model_input = pd.DataFrame({
        "text": [message],
        "source": [message_source]
    })

    label_int = pipeline.predict(model_input)[0]
    probs = pipeline.predict_proba(model_input)[0]

    print(f"Prediction probabilities: {probs}")

    confidence = float(max(probs))  # confidence of predicted class

    if label_int == 0:
        label = "legit"
        confidence = float(probs[0])
    elif label_int == 1:
        label = "spam"
        confidence = float(probs[1])
    else:
        label = "phishing"
        confidence = float(max(probs))  # fallback if multi-class

    return {
        "label": label,
        "confidence": confidence
    }
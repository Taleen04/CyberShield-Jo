import os
import pickle
import joblib
from functools import lru_cache
from pathlib import Path
from app.ml.Preprocessing import TextCleaner
from app.ml.Preprocessing import NumericFeatures 
from app.ml.Preprocessing import SourceTypeEncoder
from huggingface_hub import hf_hub_download
from tensorflow.keras.models import load_model


token = os.getenv("HF_TOKEN")
@lru_cache(maxsize=1)
def load_pipeline(model_type: str):
    """
    Loads the pipeline from disk exactly once (cached).
    lru_cache ensures the model isn't reloaded on every request.
    """
    if model_type == "text":
        MODEL_PATH = hf_hub_download(
            repo_id="aboudiua/sms_phishing_model_pipeline1",
            repo_type="model",
            filename="model.keras",
            token=token
        )
        print("[model-loader] loading text model")
        model = load_model(MODEL_PATH)
        tokenizer_path = hf_hub_download(
            repo_id="aboudiua/sms_phishing_model_pipeline1",
            repo_type="model",
            filename="tokenizer.pkl",
            token=token
        )
        
        with open(tokenizer_path, "rb") as f:
            tokenizer = pickle.load(f)
        max_len_path = hf_hub_download(
            repo_id="aboudiua/sms_phishing_model_pipeline1",
            repo_type="model",
            filename="max_len.pkl",
            token=token
        )
        with open(max_len_path, "rb") as f:
            max_len = pickle.load(f)
        return model, tokenizer, max_len
    elif model_type == "url":
        MODEL_PATH = hf_hub_download(
            repo_id="aboudiua/url_phishing_model_pipeline1",
            repo_type="model",
            filename="model.joblib",
            token=token,
        )
        print("[model-loader] loading url model")
        model = joblib.load(MODEL_PATH)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    if MODEL_PATH is None:
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Run ml/train.py first."
        )
    print(f"[{model_type}-Classifier] Loading pipeline from {MODEL_PATH}")
    return model
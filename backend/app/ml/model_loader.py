import joblib
from functools import lru_cache
from pathlib import Path
from app.ml.Preprocessing import TextCleaner
from app.ml.Preprocessing import NumericFeatures
from app.ml.Preprocessing import SourceTypeEncoder



MODEL_PATH = Path(__file__).parent.parent / "./ml/models/sms_phishing_model_pipeline.joblib"
 
@lru_cache(maxsize=1)
def load_pipeline():
    """
    Loads the pipeline from disk exactly once (cached).
    lru_cache ensures the model isn't reloaded on every request.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Run ml/train.py first."
        )
    print(f"[classifier] Loading pipeline from {MODEL_PATH}")
    return joblib.load(MODEL_PATH)
import re
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd


class TextCleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self._is_fitted_ = True
        return self

    def transform(self, X):
        cleaned_texts = []
        
        for message in X:
            message = str(message).lower()
            
            # preserve URL + numbers
            message = re.sub(r"http\S+", " URL ", message)
            message = re.sub(r"\d+", " NUM ", message)
            
            # remove punctuation
            message = re.sub(r"[^a-zA-Z\s]", " ", message)
            
            # normalize whitespace
            message = re.sub(r"\s+", " ", message).strip()
            
            cleaned_texts.append(message)
        
        return np.array(cleaned_texts)
    
    
class NumericFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, clip_max=10):
        self.clip_max = clip_max

    def fit(self, X, y=None):
        self._is_fitted_ = True
        return self

    def _extract_from_text(self, text):
        # find URLs
        urls = re.findall(r"http[s]?://\S+|www\.\S+", str(text))

        url_count = len(urls)
        url_count_clipped = min(url_count, self.clip_max)
        has_url = 1 if url_count > 0 else 0

        return has_url, url_count_clipped

    def transform(self, X):
        has_url_list = []
        url_count_list = []

        for text in X:
            has_url, url_count = self._extract_from_text(text)
            has_url_list.append(has_url)
            url_count_list.append(url_count)

        return np.column_stack([has_url_list, url_count_list])

class SourceTypeEncoder(BaseEstimator, TransformerMixin):
    """
    Encodes message source into binary values:
    email -> 0
    anything else -> 1
    """

    def __init__(self, source_col="source"):
        self.source_col = source_col

    def fit(self, X, y=None):
        # Set a fitted attribute for sklearn's check_is_fitted
        self._is_fitted_ = True
        return self

    def transform(self, X):
        X = X.copy()

        # Ensure DataFrame format
        if isinstance(X, pd.Series):
            X = X.to_frame()

        source = X[self.source_col].fillna("").str.lower()

        X[self.source_col] = np.where(source == "email", 0, 1)

        return X[[self.source_col]].values
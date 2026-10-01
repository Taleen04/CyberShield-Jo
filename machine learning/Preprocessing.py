import re
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
from tld import get_tld
from urllib.parse import urlparse
import re
import string
import unicodedata
from sklearn.base import BaseEstimator, TransformerMixin
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def clean_text(text):
    text = str(text).lower()
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')

    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', ' url ', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'\w*\d\w*', ' num ', text)
    text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text

class TextCleaner(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self._is_fitted_ = True
        return self

    def transform(self, X):
        return [clean_text(text) for text in X]
        
    
    
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
    
class URLFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.symbols = ['@','?','-','=','.','#','%','+','$','!','*',',','//']

    def fit(self, X, y=None):
        self._is_fitted_ = True
        return self

    def transform(self, X):
        X = pd.DataFrame(X, columns=["url"])
        df = pd.DataFrame()

        df['url_len'] = X['url'].astype(str).apply(len)

        # domain
        def process_tld(url):
            try:
                res = get_tld(url, as_object=True, fix_protocol=True)
                return res.parsed_url.netloc
            except:
                return None

        df['domain'] = X['url'].apply(process_tld)

        # symbol counts
        for sym in self.symbols:
            df[sym] = X['url'].astype(str).apply(lambda x: x.count(sym))

        # abnormal
        def abnormal_url(url):
            hostname = str(urlparse(url).hostname)
            return 1 if hostname and hostname in url else 0

        df['abnormal_url'] = X['url'].astype(str).apply(abnormal_url)

        # https
        df['https'] = X['url'].astype(str).apply(lambda x: 1 if urlparse(x).scheme == 'https' else 0)

        # digits
        df['digits'] = X['url'].astype(str).apply(lambda x: sum(c.isdigit() for c in x))

        # letters
        df['letters'] = X['url'].astype(str).apply(lambda x: sum(c.isalpha() for c in x))

        # shortening
        def shortening(url):
            return 1 if re.search(r'bit\.ly|tinyurl|goo\.gl|t\.co', url) else 0

        df['Shortining_Service'] = X['url'].astype(str).apply(shortening)

        # IP
        def has_ip(url):
            return 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

        df['having_ip_address'] = X['url'].astype(str).apply(has_ip)

        return df.drop(columns=["domain"])
    
class URLDomainExtractor(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        self._is_fitted_ = True
        return self

    def transform(self, X):
        X = pd.DataFrame(X, columns=["url"])
        df = pd.DataFrame()

        # domain
        def process_tld(url):
            try:
                res = get_tld(url, as_object=True, fix_protocol=True)
                return res.parsed_url.netloc
            except:
                return None

        df['domain'] = X['url'].apply(process_tld)

        return df
    
    

class TextTokenizer(BaseEstimator, TransformerMixin):
    def __init__(self, num_words=20000):
        self.is_fitted_ = False
        self.num_words = num_words
        self.tokenizer = Tokenizer(num_words=num_words, oov_token="UNK")

    def fit(self, X, y=None):
        self.tokenizer.fit_on_texts(X)
        self.is_fitted_ = True
        return self

    def transform(self, X):
        return self.tokenizer.texts_to_sequences(X)
    


class SequencePadding(BaseEstimator, TransformerMixin):
    def __init__(self, max_len):
        self.max_len = max_len

    def fit(self, X, y=None):
        self._is_fitted_ = True
        return self

    def transform(self, X):
        return pad_sequences(X, maxlen=self.max_len, padding='post', truncating='post')
"""
ML Preprocess Module for PitchLens AI
Loads dataset and constructs TF-IDF feature matrices.
"""
import logging
from pathlib import Path
from typing import Tuple, Optional, Any
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from config.settings import DATASET_PATH

logger = logging.getLogger("PitchLens.MLPreprocess")


def load_dataset_for_training(dataset_path: Optional[Path] = None) -> Tuple[pd.Series, pd.Series, pd.DataFrame]:
    """Load dataset CSV and separate text X and label y."""
    path = dataset_path or DATASET_PATH
    if not path.exists():
        raise FileNotFoundError(f"Training dataset not found at {path}")

    df = pd.read_csv(path)
    if "pitch_text" not in df.columns or "success_label" not in df.columns:
        raise ValueError("Dataset CSV must contain 'pitch_text' and 'success_label' columns.")

    df["pitch_text"] = df["pitch_text"].fillna("")
    X_text = df["pitch_text"]
    y = df["success_label"]
    return X_text, y, df


def build_tfidf_features(X_text: pd.Series, vectorizer: Optional[TfidfVectorizer] = None) -> Tuple[Any, TfidfVectorizer]:
    """Transform pitch text series using TfidfVectorizer."""
    if vectorizer is None:
        vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=500)
        X_tfidf = vectorizer.fit_transform(X_text)
    else:
        X_tfidf = vectorizer.transform(X_text)
    return X_tfidf, vectorizer

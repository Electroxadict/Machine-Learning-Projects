"""
Benchmark Engine Module for PitchLens AI
Calculates TF-IDF cosine similarity against dataset pitches.
"""
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config.settings import DATASET_PATH, DISCLAIMER_TEXT

logger = logging.getLogger("PitchLens.BenchmarkEngine")


class BenchmarkEngine:
    """Finds most similar pitch examples in dataset using TF-IDF cosine similarity."""

    def __init__(self, dataset_path: Optional[Path] = None):
        self.dataset_path = dataset_path or DATASET_PATH
        self.df_dataset: Optional[pd.DataFrame] = None
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self.load_dataset()

    def load_dataset(self) -> None:
        """Load dataset CSV and compute TF-IDF matrix."""
        try:
            if not self.dataset_path.exists():
                logger.warning(f"Dataset CSV not found at {self.dataset_path}")
                return

            self.df_dataset = pd.read_csv(self.dataset_path)
            if "pitch_text" not in self.df_dataset.columns:
                logger.error("Dataset CSV missing 'pitch_text' column.")
                return

            texts = self.df_dataset["pitch_text"].fillna("").tolist()
            self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
            logger.info(f"Benchmark dataset loaded with {len(self.df_dataset)} records.")
        except Exception as e:
            logger.error(f"Error loading benchmark dataset: {e}", exc_info=True)

    def find_similar_pitches(self, pitch_text: str, top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Compute similarity of input pitch text against dataset.
        Returns list of top_n similar pitch dicts with percentage similarity.
        """
        if self.df_dataset is None or self.vectorizer is None or self.tfidf_matrix is None:
            logger.warning("Benchmark dataset not initialized.")
            return []

        if not pitch_text.strip():
            return []

        try:
            input_vec = self.vectorizer.transform([pitch_text])
            similarities = cosine_similarity(input_vec, self.tfidf_matrix).flatten()

            # Rank indices by similarity score descending
            top_indices = similarities.argsort()[::-1][:top_n]

            results = []
            for idx in top_indices:
                sim_score = float(similarities[idx])
                row = self.df_dataset.iloc[idx]
                results.append({
                    "id": int(row.get("id", idx + 1)),
                    "pitch_name": str(row.get("pitch_name", "Untitled")),
                    "industry": str(row.get("industry", "General")),
                    "similarity_percentage": round(sim_score * 100.0, 1),
                    "problem_summary": str(row.get("problem", ""))[:120],
                    "solution_summary": str(row.get("solution", ""))[:120],
                    "disclaimer": "Textual/feature similarity — not a prediction of business success."
                })

            return results
        except Exception as e:
            logger.error(f"Error executing similarity search: {e}", exc_info=True)
            return []

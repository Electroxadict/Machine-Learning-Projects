"""
ML Predictor Module for PitchLens AI
Loads joblib model & vectorizer to predict pitch benchmark alignment.
"""
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import joblib
from config.settings import MODEL_PATH, VECTORIZER_PATH, DISCLAIMER_TEXT

logger = logging.getLogger("PitchLens.MLPredictor")


class MLPredictor:
    """Inference engine for saved joblib classification model."""

    def __init__(self, model_path: Optional[Path] = None, vectorizer_path: Optional[Path] = None):
        self.model_path = model_path or MODEL_PATH
        self.vectorizer_path = vectorizer_path or VECTORIZER_PATH
        self.model = None
        self.vectorizer = None
        self.is_loaded = False
        self.load_model()

    def load_model(self) -> bool:
        """Load trained model and vectorizer from disk."""
        try:
            if self.model_path.exists() and self.vectorizer_path.exists():
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
                self.is_loaded = True
                logger.info(f"Loaded ML model from {self.model_path}")
                return True
            else:
                logger.warning(f"ML model files not found at {self.model_path}")
                self.is_loaded = False
                return False
        except Exception as e:
            logger.error(f"Error loading ML model: {e}", exc_info=True)
            self.is_loaded = False
            return False

    def predict(self, pitch_text: str) -> Dict[str, Any]:
        """
        Predict pitch benchmark alignment probability.
        Returns dict with predicted class, confidence, and disclaimers.
        """
        if not self.is_loaded or self.model is None or self.vectorizer is None:
            return {
                "is_model_available": False,
                "predicted_label": 0,
                "confidence_score": 0.0,
                "status_message": "Model not trained — using baseline evaluation.",
                "disclaimer": DISCLAIMER_TEXT
            }

        try:
            X_vec = self.vectorizer.transform([pitch_text])
            pred_class = int(self.model.predict(X_vec)[0])
            proba = self.model.predict_proba(X_vec)[0]
            confidence = float(proba[pred_class])

            return {
                "is_model_available": True,
                "predicted_label": pred_class,
                "confidence_score": round(confidence * 100.0, 1),
                "status_message": "Strong Benchmark Alignment" if pred_class == 1 else "Developing Pitch Alignment",
                "disclaimer": DISCLAIMER_TEXT
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}", exc_info=True)
            return {
                "is_model_available": False,
                "predicted_label": 0,
                "confidence_score": 0.0,
                "status_message": f"Prediction error: {str(e)}",
                "disclaimer": DISCLAIMER_TEXT
            }

"""
ML Model Wrapper for PitchLens AI
Supports Logistic Regression, Random Forest, and Gradient Boosting models.
"""
import logging
from typing import Dict, Any, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

logger = logging.getLogger("PitchLens.MLModel")


def get_candidate_models() -> Dict[str, Any]:
    """Return dictionary of classifier model instances for training comparison."""
    return {
        "Logistic Regression": LogisticRegression(C=1.0, max_iter=200, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=50, learning_rate=0.1, random_state=42),
    }

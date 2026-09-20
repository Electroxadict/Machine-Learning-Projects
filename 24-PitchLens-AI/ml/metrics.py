"""
ML Metrics Module for PitchLens AI
Evaluates model performance metrics.
"""
from typing import Dict, Any, Optional
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


def evaluate_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_proba: Optional[np.ndarray] = None) -> Dict[str, float]:
    """Calculate accuracy, precision, recall, f1, and roc_auc metrics."""
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))

    auc = 0.5
    if y_proba is not None and len(np.unique(y_true)) > 1:
        try:
            auc = float(roc_auc_score(y_true, y_proba))
        except Exception:
            auc = 0.5

    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(auc, 4),
    }

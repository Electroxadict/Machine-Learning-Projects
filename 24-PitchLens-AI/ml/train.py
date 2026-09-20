"""
ML Training Script for PitchLens AI
Trains, compares, and saves the best performing classifier model on pitch data.
"""
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import joblib
from sklearn.model_selection import StratifiedKFold
import numpy as np

from config.settings import MODEL_PATH, VECTORIZER_PATH, DATASET_PATH, MODELS_DIR
from ml.preprocess import load_dataset_for_training, build_tfidf_features
from ml.model import get_candidate_models
from ml.metrics import evaluate_classification_metrics

# Configure Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("PitchLens.MLTrain")


def train_and_save_model(dataset_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Train candidate models, compare validation performance, save best model,
    and return evaluation summary.
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load Data
    X_text, y, df = load_dataset_for_training(dataset_path or DATASET_PATH)
    logger.info(f"Loaded {len(df)} dataset records for model training.")

    # 2. Build TF-IDF Features
    X_tfidf, vectorizer = build_tfidf_features(X_text)

    # 3. Model Comparison
    models = get_candidate_models()
    best_name = None
    best_f1 = -1.0
    best_model = None
    results = {}

    n_splits = min(3, len(df) // 2)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

    for name, model_inst in models.items():
        oof_preds = np.zeros(len(y))
        oof_probas = np.zeros(len(y))

        for train_idx, val_idx in skf.split(X_tfidf, y):
            X_tr, X_val = X_tfidf[train_idx], X_tfidf[val_idx]
            y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]

            model_inst.fit(X_tr, y_tr)
            preds = model_inst.predict(X_val)
            oof_preds[val_idx] = preds

            if hasattr(model_inst, "predict_proba"):
                oof_probas[val_idx] = model_inst.predict_proba(X_val)[:, 1]

        metrics = evaluate_classification_metrics(y.values, oof_preds, oof_probas)
        results[name] = metrics
        logger.info(f"Model '{name}' -> Accuracy: {metrics['accuracy']}, F1: {metrics['f1_score']}")

        if metrics["f1_score"] > best_f1:
            best_f1 = metrics["f1_score"]
            best_name = name
            best_model = model_inst

    # Refit best model on full dataset
    best_model.fit(X_tfidf, y)

    # Save best model and vectorizer
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    logger.info(f"Successfully saved best model '{best_name}' to {MODEL_PATH}")

    return {
        "best_model_name": best_name,
        "best_f1_score": best_f1,
        "metrics_summary": results,
        "dataset_size": len(df),
        "feature_count": X_tfidf.shape[1],
        "model_path": str(MODEL_PATH),
    }


if __name__ == "__main__":
    summary = train_and_save_model()
    print("\n================ ML TRAINING COMPLETE ================")
    print(f"Selected Model : {summary['best_model_name']}")
    print(f"Dataset Records: {summary['dataset_size']}")
    print(f"Features       : {summary['feature_count']}")
    print(f"Validation F1  : {summary['best_f1_score']}")
    print("======================================================\n")

"""
Pitch Evaluator Master Module for PitchLens AI
Orchestrates text processing, feature extraction, section detection, explainable scoring,
benchmark similarity search, recommendation generation, and ML inference.
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from config.settings import DEFAULT_CATEGORY_WEIGHTS, DISCLAIMER_TEXT, DEMO_NOTICE_TEXT
from core.text_processor import TextProcessor
from core.feature_extractor import FeatureExtractor
from core.section_detector import SectionDetector
from core.scoring import ScoringEngine
from core.benchmark import BenchmarkEngine
from core.recommender import RecommenderEngine

logger = logging.getLogger("PitchLens.PitchEvaluator")


class PitchEvaluator:
    """Master Pitch Evaluation Engine."""

    def __init__(self, category_weights: Optional[Dict[str, float]] = None):
        self.category_weights = category_weights or DEFAULT_CATEGORY_WEIGHTS.copy()
        self.text_processor = TextProcessor()
        self.feature_extractor = FeatureExtractor()
        self.section_detector = SectionDetector()
        self.scoring_engine = ScoringEngine(self.category_weights)
        self.benchmark_engine = BenchmarkEngine()
        self.recommender_engine = RecommenderEngine()

    def update_weights(self, new_weights: Dict[str, float]) -> None:
        """Update category evaluation weights."""
        self.category_weights = new_weights.copy()
        self.scoring_engine = ScoringEngine(self.category_weights)

    def evaluate(self, pitch_text: str, pitch_name: str = "Untitled Pitch", structured_fields: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Execute full evaluation pipeline on pitch text.
        Raises ValueError if text is invalid or too short.
        """
        # Validate Input
        if not pitch_text or not pitch_text.strip():
            raise ValueError("Pitch text cannot be empty. Please enter or upload pitch content.")

        cleaned_text = self.text_processor.clean_text(pitch_text)

        # Merge structured breakdown fields if provided
        if structured_fields:
            extra_parts = []
            for field, val in structured_fields.items():
                if val and val.strip():
                    extra_parts.append(f"{field.replace('_', ' ').title()}: {val.strip()}")
            if extra_parts:
                cleaned_text += "\n\n" + "\n".join(extra_parts)

        # Re-check length after cleaning
        words = cleaned_text.split()
        if len(words) < 15:
            raise ValueError("Pitch text is too short (<15 words) for a meaningful evaluation. Please provide more detail.")

        logger.info(f"Starting pitch evaluation for '{pitch_name}' ({len(words)} words)")

        # 1. Text Processing & Basic Metrics
        text_metrics = self.text_processor.get_basic_metrics(cleaned_text)

        # 2. Feature Extraction
        features = self.feature_extractor.get_all_features(cleaned_text)

        # 3. Section Detection & Missing Elements
        section_analysis = self.section_detector.detect_sections(cleaned_text, features)

        # 4. Explainable Scoring Engine
        scoring_results = self.scoring_engine.evaluate_all(text_metrics, features, section_analysis)

        # 5. Benchmark Cosine Similarity Search
        similar_pitches = self.benchmark_engine.find_similar_pitches(cleaned_text, top_n=3)

        # 6. Recommendation Engine (Recommendations, Strengths, Weaknesses, Missing Elements)
        recommendations = self.recommender_engine.generate_recommendations(
            scoring_results["category_scores"], section_analysis, features
        )
        strengths = self.recommender_engine.extract_strengths(section_analysis, features)
        weaknesses = self.recommender_engine.extract_weaknesses(section_analysis, features)
        missing_elements = self.recommender_engine.extract_missing_elements(section_analysis)

        # 7. Package Evaluation Object
        eval_result = {
            "pitch_name": pitch_name.strip() or "Untitled Pitch",
            "pitch_text": cleaned_text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "word_count": text_metrics["word_count"],
            "sentence_count": text_metrics["sentence_count"],
            "avg_sentence_length": text_metrics["avg_sentence_length"],
            "vocabulary_richness": text_metrics["vocabulary_richness"],
            "overall_score": scoring_results["overall_score"],
            "readiness": scoring_results["readiness"],
            "readiness_color": scoring_results["readiness_color"],
            "evidence_coverage": scoring_results["evidence_coverage"],
            "category_scores": scoring_results["category_scores"],
            "category_explanations": scoring_results["category_explanations"],
            "category_statuses": scoring_results["category_statuses"],
            "similar_pitches": similar_pitches,
            "recommendations": recommendations,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "missing_elements": missing_elements,
            "disclaimer": DISCLAIMER_TEXT,
            "demo_notice": DEMO_NOTICE_TEXT,
        }

        logger.info(f"Evaluation complete for '{pitch_name}'. Overall Score: {eval_result['overall_score']}/100 ({eval_result['readiness']})")
        return eval_result

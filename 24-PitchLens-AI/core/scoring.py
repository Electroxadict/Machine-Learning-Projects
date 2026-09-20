"""
Scoring Engine Module for PitchLens AI
Provides explainable, feature-driven scoring for 10 pitch categories, weighted overall score,
readiness tier classification, and evidence coverage percentage.
"""
import logging
from typing import Dict, Any, Tuple

from config.settings import DEFAULT_CATEGORY_WEIGHTS, READINESS_TIERS, CATEGORY_DISPLAY_NAMES

logger = logging.getLogger("PitchLens.ScoringEngine")


class ScoringEngine:
    """Calculates category scores, weighted overall score, readiness tier, and evidence coverage."""

    def __init__(self, category_weights: Dict[str, float] = None):
        self.weights = category_weights or DEFAULT_CATEGORY_WEIGHTS.copy()
        # Normalize weights to sum to 1.0
        total_w = sum(self.weights.values())
        if total_w > 0:
            self.weights = {k: v / total_w for k, v in self.weights.items()}

    def evaluate_all(
        self,
        text_metrics: Dict[str, Any],
        features: Dict[str, Any],
        section_analysis: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Compute category scores, explanations, overall weighted score, and readiness tier.
        """
        category_scores = {}
        category_explanations = {}
        category_statuses = {}

        quant = features.get("quantitative_evidence", {})
        has_quant = quant.get("has_quantitative_evidence", False)
        vocab_richness = text_metrics.get("vocabulary_richness", 0.5)

        for cat_key, analysis in section_analysis.items():
            status = analysis["status"]
            missing = analysis.get("missing_elements", [])
            reason = analysis.get("reason", "")

            base_score = 0.0
            if status == "PRESENT":
                base_score = 80.0
                if has_quant:
                    base_score += 12.0
                if vocab_richness > 0.5:
                    base_score += 5.0
                if len(missing) == 0:
                    base_score += 3.0
            elif status == "PARTIALLY_PRESENT":
                base_score = 50.0
                if has_quant:
                    base_score += 10.0
                if vocab_richness > 0.4:
                    base_score += 5.0
            else:  # MISSING
                base_score = 15.0
                if vocab_richness > 0.6:
                    base_score += 10.0

            # Cap score between 0 and 100
            score = round(max(0.0, min(100.0, base_score)), 1)

            # Build evidence-backed explanation string
            display_name = CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key.replace("_", " ").title())
            if status == "PRESENT":
                explanation = f"Score: {score}/100. {display_name} is clearly articulated with supporting details."
                if has_quant:
                    explanation += " Quantitative evidence detected."
            elif status == "PARTIALLY_PRESENT":
                missing_str = ", ".join(missing) if missing else "further details"
                explanation = f"Score: {score}/100. {display_name} is partially addressed but missing: {missing_str}."
            else:
                explanation = f"Score: {score}/100. {display_name} is missing from the pitch narrative."

            category_scores[cat_key] = score
            category_explanations[cat_key] = explanation
            category_statuses[cat_key] = status

        # Calculate Overall Weighted Score
        overall_score = 0.0
        for cat_key, score_val in category_scores.items():
            weight = self.weights.get(cat_key, 0.10)
            overall_score += weight * score_val

        overall_score = round(max(0.0, min(100.0, overall_score)), 1)

        # Calculate Evidence Coverage percentage
        present_count = sum(1 for s in category_statuses.values() if s == "PRESENT")
        partial_count = sum(1 for s in category_statuses.values() if s == "PARTIALLY_PRESENT")
        total_categories = len(section_analysis)
        coverage = round(((present_count * 1.0 + partial_count * 0.5) / max(total_categories, 1)) * 100.0, 1)

        # Determine Readiness Tier
        readiness_label, color_hex = self.classify_readiness(overall_score)

        return {
            "overall_score": overall_score,
            "readiness": readiness_label,
            "readiness_color": color_hex,
            "evidence_coverage": coverage,
            "category_scores": category_scores,
            "category_explanations": category_explanations,
            "category_statuses": category_statuses,
        }

    @staticmethod
    def classify_readiness(score: float) -> Tuple[str, str]:
        """Classify score into readiness tier label and color hex."""
        for min_s, max_s, label, color in READINESS_TIERS:
            if min_s <= score <= max_s:
                return label, color
        if score >= 90:
            return "Highly Developed", "#8BE9FD"
        return "Needs Major Improvement", "#FF5555"

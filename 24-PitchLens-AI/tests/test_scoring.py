"""
Unit Tests for Scoring Engine
"""
import pytest
from core.scoring import ScoringEngine


def test_category_scores_bounds():
    engine = ScoringEngine()
    text_metrics = {"word_count": 150, "sentence_count": 8, "vocabulary_richness": 0.65}
    features = {"quantitative_evidence": {"has_quantitative_evidence": True}}

    section_analysis = {
        "problem_clarity": {"status": "PRESENT", "missing_elements": [], "reason": ""},
        "solution_strength": {"status": "PARTIALLY_PRESENT", "missing_elements": ["Architecture"], "reason": ""},
        "market_opportunity": {"status": "MISSING", "missing_elements": ["TAM"], "reason": ""},
    }

    results = engine.evaluate_all(text_metrics, features, section_analysis)
    
    assert "overall_score" in results
    assert 0.0 <= results["overall_score"] <= 100.0
    assert "readiness" in results
    assert "evidence_coverage" in results
    assert 0.0 <= results["evidence_coverage"] <= 100.0


def test_readiness_tier_classification():
    assert ScoringEngine.classify_readiness(30)[0] == "Needs Major Improvement"
    assert ScoringEngine.classify_readiness(50)[0] == "Developing"
    assert ScoringEngine.classify_readiness(65)[0] == "Promising"
    assert ScoringEngine.classify_readiness(80)[0] == "Strongly Developed"
    assert ScoringEngine.classify_readiness(95)[0] == "Highly Developed"

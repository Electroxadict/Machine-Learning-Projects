"""
Unit Tests for Pitch Evaluator Workflow
"""
import pytest
from core.evaluator import PitchEvaluator


def test_empty_input_rejection():
    evaluator = PitchEvaluator()
    with pytest.raises(ValueError, match="cannot be empty"):
        evaluator.evaluate("")


def test_short_input_rejection():
    evaluator = PitchEvaluator()
    with pytest.raises(ValueError, match="too short"):
        evaluator.evaluate("We make cool apps.")


def test_full_pitch_evaluation():
    evaluator = PitchEvaluator()
    pitch_text = (
        "CloudPulse Analytics is a real-time cloud infrastructure cost optimization platform. "
        "Engineering teams waste over $30B annually on idle cloud resources because existing monitoring tools "
        "lack automated cost-remediation capabilities. CloudPulse solves this with an AI-driven agent that "
        "dynamically resizes Kubernetes clusters. Our target market is mid-market DevOps teams ($8.4B TAM). "
        "We operate a B2B SaaS subscription model charging $499 per month per cluster with an 82% gross margin. "
        "We have 45 paying enterprise customers and $28,000 Monthly Recurrent Revenue (MRR). "
        "Unlike CloudHealth, we provide automated 1-click resource saving actions. "
        "Our team consists of former AWS senior architects and Stanford computer science graduates."
    )

    result = evaluator.evaluate(pitch_text, pitch_name="CloudPulse Pitch Test")

    assert result["pitch_name"] == "CloudPulse Pitch Test"
    assert result["overall_score"] > 60.0
    assert result["readiness"] in ["Promising", "Strongly Developed", "Highly Developed"]
    assert len(result["category_scores"]) == 10
    assert len(result["similar_pitches"]) > 0
    assert len(result["recommendations"]) > 0
    assert len(result["strengths"]) > 0
    assert "disclaimer" in result

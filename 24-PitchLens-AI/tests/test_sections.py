"""
Unit Tests for Section Detector
"""
import pytest
from core.feature_extractor import FeatureExtractor
from core.section_detector import SectionDetector


def test_section_status_detection():
    text = (
        "CloudPulse is a real-time cloud cost optimization platform. "
        "Engineering teams waste $30B annually on idle cloud resources. "
        "We operate a B2B SaaS subscription model charging $499 per month per cluster. "
        "We have 45 paying clients and $28,000 MRR."
    )

    features = FeatureExtractor.get_all_features(text)
    sections = SectionDetector.detect_sections(text, features)

    assert "problem_clarity" in sections
    assert sections["problem_clarity"]["status"] in ["PRESENT", "PARTIALLY_PRESENT"]

    assert "business_model" in sections
    assert sections["business_model"]["status"] == "PRESENT"

    assert "traction_validation" in sections
    assert sections["traction_validation"]["status"] == "PRESENT"

    assert "team_execution" in sections
    assert sections["team_execution"]["status"] == "MISSING"
    assert "Founder backgrounds" in sections["team_execution"]["missing_elements"]

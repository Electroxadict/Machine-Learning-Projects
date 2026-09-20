"""
Unit Tests for Feature Extractor
"""
import pytest
from core.feature_extractor import FeatureExtractor


def test_presence_flags_extraction():
    text = "Our problem is that engineering teams waste $30B on cloud infrastructure. Our AI platform automates cluster sizing."
    flags = FeatureExtractor.extract_presence_flags(text)

    assert flags.get("problem_present") is True
    assert flags.get("solution_present") is True
    assert flags.get("technology_present") is True


def test_quantitative_evidence_extraction():
    text = "We have 2,500 active users and generated ₹4.2 lakh revenue with an 18% MoM growth rate."
    quant = FeatureExtractor.extract_quantitative_evidence(text)

    assert quant["has_quantitative_evidence"] is True
    assert len(quant["currency_mentions"]) > 0
    assert len(quant["percentage_mentions"]) > 0
    assert len(quant["user_metric_mentions"]) > 0

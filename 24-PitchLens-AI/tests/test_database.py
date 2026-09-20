"""
Unit Tests for Database Manager
"""
import pytest
from pathlib import Path
import tempfile
from database.database import DatabaseManager


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    db = DatabaseManager(db_path)
    yield db
    if db_path.exists():
        try:
            db_path.unlink()
        except PermissionError:
            pass


def test_save_and_retrieve_evaluation(temp_db):
    eval_payload = {
        "pitch_name": "Test Pitch",
        "pitch_text": "Sample text for database testing.",
        "date": "2026-09-20 12:00",
        "overall_score": 82.5,
        "readiness": "Strongly Developed",
        "evidence_coverage": 85.0,
        "category_scores": {"problem_clarity": 80.0, "solution_strength": 85.0},
        "category_statuses": {"problem_clarity": "PRESENT", "solution_strength": "PRESENT"},
        "category_explanations": {"problem_clarity": "Good clarity.", "solution_strength": "Strong solution."},
        "recommendations": [
            {
                "priority": "HIGH",
                "title": "Add Pricing",
                "problem": "Missing pricing.",
                "why_it_matters": "Investors care.",
                "what_to_add": "Add $499/mo.",
                "suggested_questions": "What is the price?"
            }
        ]
    }

    eval_id = temp_db.save_evaluation(eval_payload)
    assert eval_id > 0

    retrieved = temp_db.get_evaluation_by_id(eval_id)
    assert retrieved is not None
    assert retrieved["pitch_name"] == "Test Pitch"
    assert retrieved["overall_score"] == 82.5
    assert retrieved["version"] == 1
    assert "problem_clarity" in retrieved["category_scores"]
    assert len(retrieved["recommendations"]) == 1


def test_version_auto_increment(temp_db):
    eval_payload = {
        "pitch_name": "Versioned Pitch",
        "pitch_text": "Sample text.",
        "overall_score": 70.0,
        "readiness": "Promising",
        "category_scores": {},
        "category_statuses": {},
        "category_explanations": {},
        "recommendations": []
    }

    id1 = temp_db.save_evaluation(eval_payload)
    id2 = temp_db.save_evaluation(eval_payload)

    v1 = temp_db.get_evaluation_by_id(id1)
    v2 = temp_db.get_evaluation_by_id(id2)

    assert v1["version"] == 1
    assert v2["version"] == 2

"""
PitchLens AI - Global Configuration & Settings
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
DATABASE_DIR = BASE_DIR / "database"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"

# File Paths
DB_PATH = DATABASE_DIR / "pitchlens.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"
DATASET_PATH = DATA_DIR / "successful_pitches.csv"
SAMPLE_PITCHES_PATH = DATA_DIR / "sample_pitches.csv"
MODEL_PATH = MODELS_DIR / "pitchlens_model.joblib"
VECTORIZER_PATH = MODELS_DIR / "vectorizer.joblib"
LOG_FILE_PATH = LOGS_DIR / "pitchlens.log"

# Default Evaluation Category Weights (Must sum to 1.0)
DEFAULT_CATEGORY_WEIGHTS = {
    "problem_clarity": 0.10,
    "solution_strength": 0.15,
    "market_opportunity": 0.12,
    "value_proposition": 0.12,
    "business_model": 0.10,
    "competitive_advantage": 0.08,
    "traction_validation": 0.12,
    "team_execution": 0.07,
    "scalability": 0.07,
    "presentation_quality": 0.07,
}

# Category Display Labels
CATEGORY_DISPLAY_NAMES = {
    "problem_clarity": "Problem Clarity",
    "solution_strength": "Solution Strength",
    "market_opportunity": "Market Opportunity",
    "value_proposition": "Value Proposition",
    "business_model": "Business Model",
    "competitive_advantage": "Competitive Advantage",
    "traction_validation": "Traction & Validation",
    "team_execution": "Team & Execution",
    "scalability": "Scalability",
    "presentation_quality": "Presentation Quality",
}

# Readiness Tiers: (min_score, max_score, label, color_hex)
READINESS_TIERS = [
    (0, 39, "Needs Major Improvement", "#FF5555"),
    (40, 59, "Developing", "#FFB86C"),
    (60, 74, "Promising", "#F1FA8C"),
    (75, 89, "Strongly Developed", "#50FA7B"),
    (90, 100, "Highly Developed", "#8BE9FD"),
]

# Application Disclaimers & Notices
DISCLAIMER_TEXT = (
    "This evaluation measures pitch characteristics and similarity to the available dataset. "
    "It does not predict business success or guarantee investment outcomes."
)

DEMO_NOTICE_TEXT = (
    "PitchLens AI is running with demonstration data. "
    "Replace the dataset with validated pitch data for production evaluation."
)

APP_TITLE = "PitchLens AI"
APP_TAGLINE = "Evaluate. Improve. Pitch Better."

# UI Dark Theme Colors
THEME_COLORS = {
    "bg_dark": "#181825",
    "bg_card": "#1E1E2E",
    "bg_sidebar": "#11111B",
    "bg_hover": "#313244",
    "accent_primary": "#89B4FA",
    "accent_secondary": "#B4BEFE",
    "text_main": "#CDD6F4",
    "text_muted": "#A6ADC8",
    "border": "#45475A",
    "success": "#A6E3A1",
    "warning": "#F9E2AF",
    "danger": "#F38BA8",
    "info": "#89DCEB",
}


def ensure_directories():
    """Ensure all required application directories exist."""
    for directory in [
        CONFIG_DIR,
        DATA_DIR,
        MODELS_DIR,
        DATABASE_DIR,
        REPORTS_DIR,
        LOGS_DIR,
        ASSETS_DIR,
        ASSETS_DIR / "icons",
        ASSETS_DIR / "images",
        ASSETS_DIR / "styles",
    ]:
        directory.mkdir(parents=True, exist_ok=True)

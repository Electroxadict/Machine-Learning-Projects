# PitchLens AI

> **"Evaluate. Improve. Pitch Better."**

PitchLens AI is a professional, standalone desktop application built with Python and PySide6 that evaluates startup pitch narratives against structured pitch quality criteria and benchmark dataset examples.

It provides transparent, explainable scoring across 10 core pitch dimensions, rule-based section detection, NLP feature extraction, TF-IDF cosine similarity benchmarking, priority-ranked recommendations, version tracking, and presentation-ready PDF reports.

---

## Key Features

- 🖥️ **Modern Desktop UI**: Built with PySide6 (Qt) featuring a modern SaaS dark-themed dashboard, metric cards, progress visualizers, and interactive Matplotlib charts.
- 🔍 **Multi-Method Input**: Supports direct text pasting, file import (.txt, .pdf, .docx), demo sample presets, and structured component input breakdown.
- 📐 **10-Category Explainable Framework**: Evaluates Problem Clarity, Solution Strength, Market Opportunity, Value Proposition, Business Model, Competitive Advantage, Traction & Validation, Team & Execution, Scalability, and Presentation Quality.
- 🤖 **NLP & Machine Learning Engine**: Feature extraction (n-grams, Type-Token Ratio), regex quantitative evidence detection (revenue, user counts, market size, growth %), scikit-learn TF-IDF cosine similarity, and classifier model training (Logistic Regression, Random Forest, Gradient Boosting).
- 📊 **Analytics & Version Tracking**: SQLite database persistence (`database/pitchlens.db`), side-by-side pitch version progression comparison (V1 vs V2 vs V3), and aggregate analytics dashboard.
- 📄 **Export Capabilities**: Presentation-ready ReportLab PDF reports, formatted JSON exports, and CSV summaries.
- ⚠️ **Transparent Disclaimers**: Clear labeling that evaluation measures pitch characteristics and dataset similarity without claiming to guarantee business success.

---

## Project Structure

```
PitchLens-AI/
│
├── app.py                      # Main desktop application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Complete system documentation
├── .gitignore                  # Git ignore rules
│
├── config/
│   └── settings.py             # Global settings, paths, weights, and theme colors
│
├── ui/                         # PySide6 Desktop GUI modules
│   ├── __init__.py
│   ├── main_window.py          # Sidebar, stacked layout, status bar
│   ├── dashboard.py            # Overview dashboard & recent evaluations table
│   ├── pitch_input.py          # Input tabs (Text, File, Samples, Structured)
│   ├── evaluation.py           # Evaluation results, score bars, radar plot
│   ├── history.py              # SQLite history table & version comparison
│   ├── analytics.py            # Aggregate Matplotlib performance charts
│   ├── dataset.py              # Dataset inspector & ML model training control
│   ├── settings.py             # Category weight customization sliders
│   └── widgets/
│       ├── __init__.py
│       ├── metric_card.py       # SaaS metric card widget
│       ├── score_card.py        # Hero score card widget
│       ├── radar_chart.py       # Matplotlib 10-axis radar chart
│       └── recommendation_card.py # Actionable recommendation card
│
├── core/                       # Core NLP, Scoring, and Analysis Engines
│   ├── __init__.py
│   ├── text_processor.py       # Document extraction (TXT/PDF/DOCX) & text metrics
│   ├── feature_extractor.py    # Keyword lexicons & quantitative evidence detection
│   ├── section_detector.py    # Rule-based 10-section status detector
│   ├── scoring.py              # Explainable category & weighted overall scoring
│   ├── benchmark.py            # TF-IDF Cosine Similarity benchmark engine
│   ├── recommender.py          # Actionable priority recommendation generator
│   └── evaluator.py            # Master evaluation pipeline coordinator
│
├── ml/                         # Machine Learning Pipeline
│   ├── __init__.py
│   ├── preprocess.py           # Dataset loading & TF-IDF feature matrix
│   ├── model.py                # Classifier model instances
│   ├── metrics.py              # Accuracy, F1, Precision, Recall, ROC-AUC
│   ├── predict.py              # Joblib model inference wrapper
│   └── train.py                # CLI & module training script
│
├── data/                       # Benchmark Datasets
│   ├── successful_pitches.csv  # Synthetic demo dataset (15 structured pitches)
│   ├── sample_pitches.csv      # Ready-to-use sample pitches for UI testing
│   ├── generate_datasets.py    # Dataset generator script
│   └── README.md
│
├── models/                     # Saved ML Models (.joblib)
│   ├── pitchlens_model.joblib
│   └── vectorizer.joblib
│
├── database/                   # SQLite Storage
│   ├── __init__.py
│   ├── database.py             # Database DAO manager
│   └── schema.sql              # Database DDL schema
│
├── reports/                    # Generated PDF/JSON/CSV Reports
│   ├── __init__.py
│   └── pdf_report.py           # ReportLab PDF & export generator
│
├── tests/                      # PyTest Unit Test Suite
│   ├── test_scoring.py
│   ├── test_features.py
│   ├── test_sections.py
│   ├── test_database.py
│   └── test_evaluator.py
│
└── logs/                       # Application Runtime Logs
    └── pitchlens.log
```

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Windows OS

### Step 1: Clone / Navigate to Directory
```cmd
cd C:\Users\manig\OneDrive\Desktop\PitchLens-AI
```

### Step 2: Create and Activate Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```cmd
pip install -r requirements.txt
```

---

## Running the Application

Launch the desktop GUI:
```cmd
python app.py
```

### Machine Learning Model Training
Train and evaluate candidate models on the benchmark dataset:
```cmd
python -m ml.train
```

### Running Test Suite
Run unit tests with pytest:
```cmd
python -m pytest
```

---

## Evaluation Methodology

### 10 Evaluation Categories & Default Weights
- **Problem Clarity** (10%): Specific customer pain points and quantified scale of impact.
- **Solution Strength** (15%): Product overview, mechanism, and technical architecture.
- **Market Opportunity** (12%): Addressable customer segment and TAM/SAM/SOM sizing.
- **Value Proposition** (12%): Quantified customer ROI and primary benefits.
- **Business Model** (10%): Monetization strategy, price points, and gross margins.
- **Competitive Advantage** (8%): Competitors list and defensible moat.
- **Traction & Validation** (12%): Verified user numbers, revenue, or pilot data.
- **Team & Execution** (7%): Founder credentials and domain experience.
- **Scalability** (7%): Technical/operational scaling model and expansion roadmap.
- **Presentation Quality** (7%): Structure, clarity, and executive precision.

### Readiness Tiers
- **0–39**: Needs Major Improvement
- **40–59**: Developing
- **60–74**: Promising
- **75–89**: Strongly Developed
- **90–100**: Highly Developed

---

## Important Disclaimers

> **Disclaimer**: This evaluation measures pitch narrative characteristics, structural completeness, and feature similarity to the available training dataset. It does not predict real-world business success or guarantee investment outcomes.

> **Dataset Note**: The included benchmark dataset contains **DEMO / SYNTHETIC DATA** created for system demonstration and testing purposes.

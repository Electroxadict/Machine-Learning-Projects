-- PitchLens AI SQLite Database Schema

CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pitch_name TEXT NOT NULL,
    pitch_text TEXT NOT NULL,
    date TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    overall_score REAL NOT NULL,
    readiness TEXT NOT NULL,
    evidence_coverage REAL NOT NULL DEFAULT 0.0,
    report_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS category_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluation_id INTEGER NOT NULL,
    category_key TEXT NOT NULL,
    score REAL NOT NULL,
    status TEXT NOT NULL,
    explanation TEXT,
    FOREIGN KEY (evaluation_id) REFERENCES evaluations (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluation_id INTEGER NOT NULL,
    priority TEXT NOT NULL,
    title TEXT NOT NULL,
    problem TEXT NOT NULL,
    why_it_matters TEXT NOT NULL,
    what_to_add TEXT NOT NULL,
    suggested_questions TEXT NOT NULL,
    FOREIGN KEY (evaluation_id) REFERENCES evaluations (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pitch_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pitch_name TEXT NOT NULL,
    version INTEGER NOT NULL,
    evaluation_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (evaluation_id) REFERENCES evaluations (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

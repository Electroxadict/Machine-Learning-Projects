"""
Database Manager for PitchLens AI
Provides SQLite connection management and clean DAO interfaces.
"""
import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from config.settings import DB_PATH, SCHEMA_PATH

logger = logging.getLogger("PitchLens.Database")


class DatabaseManager:
    """Manages SQLite database connections and operations."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """Get SQLite connection with foreign keys enabled and dict-like rows."""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """Initialize database schema if tables do not exist."""
        try:
            with self.get_connection() as conn:
                if SCHEMA_PATH.exists():
                    schema_script = SCHEMA_PATH.read_text(encoding="utf-8")
                    conn.executescript(schema_script)
                else:
                    logger.warning(f"Schema file not found at {SCHEMA_PATH}, creating default tables.")
                    self._create_default_tables(conn)
                conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}", exc_info=True)
            raise

    def _create_default_tables(self, conn: sqlite3.Connection) -> None:
        """Fallback inline table creation."""
        conn.executescript("""
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
        """)

    def save_evaluation(self, eval_data: Dict[str, Any]) -> int:
        """
        Save a full evaluation result to the database.
        Automatically increments version if pitch_name already exists.
        Returns the new evaluation_id.
        """
        pitch_name = eval_data.get("pitch_name", "Untitled Pitch").strip()
        pitch_text = eval_data.get("pitch_text", "")
        date_str = eval_data.get("date", datetime.now().strftime("%Y-%m-%d %H:%M"))
        overall_score = float(eval_data.get("overall_score", 0.0))
        readiness = eval_data.get("readiness", "Needs Major Improvement")
        evidence_coverage = float(eval_data.get("evidence_coverage", 0.0))
        report_path = eval_data.get("report_path", "")

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Determine next version number for this pitch name
                cursor.execute(
                    "SELECT MAX(version) FROM evaluations WHERE pitch_name = ?", (pitch_name,)
                )
                max_ver = cursor.fetchone()[0]
                next_version = (max_ver or 0) + 1

                # Insert evaluation record
                cursor.execute(
                    """
                    INSERT INTO evaluations 
                    (pitch_name, pitch_text, date, version, overall_score, readiness, evidence_coverage, report_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (pitch_name, pitch_text, date_str, next_version, overall_score, readiness, evidence_coverage, report_path)
                )
                eval_id = cursor.lastrowid

                # Record version mapping
                cursor.execute(
                    """
                    INSERT INTO pitch_versions (pitch_name, version, evaluation_id)
                    VALUES (?, ?, ?)
                    """,
                    (pitch_name, next_version, eval_id)
                )

                # Save category scores
                category_scores = eval_data.get("category_scores", {})
                category_explanations = eval_data.get("category_explanations", {})
                category_statuses = eval_data.get("category_statuses", {})

                for cat_key, score_val in category_scores.items():
                    status_val = category_statuses.get(cat_key, "PRESENT")
                    explanation_val = category_explanations.get(cat_key, "")
                    cursor.execute(
                        """
                        INSERT INTO category_scores (evaluation_id, category_key, score, status, explanation)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (eval_id, cat_key, float(score_val), status_val, explanation_val)
                    )

                # Save recommendations
                recommendations = eval_data.get("recommendations", [])
                for rec in recommendations:
                    cursor.execute(
                        """
                        INSERT INTO recommendations 
                        (evaluation_id, priority, title, problem, why_it_matters, what_to_add, suggested_questions)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            eval_id,
                            rec.get("priority", "MEDIUM"),
                            rec.get("title", ""),
                            rec.get("problem", ""),
                            rec.get("why_it_matters", ""),
                            rec.get("what_to_add", ""),
                            rec.get("suggested_questions", "")
                        )
                    )

                conn.commit()
                logger.info(f"Saved evaluation ID {eval_id} for pitch '{pitch_name}' v{next_version}")
                return eval_id

        except Exception as e:
            logger.error(f"Error saving evaluation: {e}", exc_info=True)
            raise

    def get_all_evaluations(self) -> List[Dict[str, Any]]:
        """Retrieve summary list of all evaluations."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, pitch_name, date, version, overall_score, readiness, evidence_coverage, report_path, created_at
                    FROM evaluations
                    ORDER BY id DESC
                    """
                )
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching evaluations: {e}", exc_info=True)
            return []

    def get_evaluation_by_id(self, eval_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve complete evaluation record by ID including categories & recommendations."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM evaluations WHERE id = ?", (eval_id,))
                eval_row = cursor.fetchone()
                if not eval_row:
                    return None

                result = dict(eval_row)

                # Categories
                cursor.execute(
                    "SELECT category_key, score, status, explanation FROM category_scores WHERE evaluation_id = ?",
                    (eval_id,)
                )
                cat_rows = cursor.fetchall()
                result["category_scores"] = {r["category_key"]: r["score"] for r in cat_rows}
                result["category_statuses"] = {r["category_key"]: r["status"] for r in cat_rows}
                result["category_explanations"] = {r["category_key"]: r["explanation"] for r in cat_rows}

                # Recommendations
                cursor.execute(
                    "SELECT priority, title, problem, why_it_matters, what_to_add, suggested_questions FROM recommendations WHERE evaluation_id = ?",
                    (eval_id,)
                )
                rec_rows = cursor.fetchall()
                result["recommendations"] = [dict(r) for r in rec_rows]

                return result

        except Exception as e:
            logger.error(f"Error retrieving evaluation ID {eval_id}: {e}", exc_info=True)
            return None

    def delete_evaluation(self, eval_id: int) -> bool:
        """Delete an evaluation record by ID."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM evaluations WHERE id = ?", (eval_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting evaluation ID {eval_id}: {e}", exc_info=True)
            return False

    def get_pitch_versions(self, pitch_name: str) -> List[Dict[str, Any]]:
        """Retrieve all versions of a specific pitch name for version comparison."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, pitch_name, date, version, overall_score, readiness, evidence_coverage
                    FROM evaluations
                    WHERE pitch_name = ?
                    ORDER BY version ASC
                    """,
                    (pitch_name,)
                )
                rows = cursor.fetchall()
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"Error fetching versions for pitch '{pitch_name}': {e}", exc_info=True)
            return []

    def get_unique_pitch_names(self) -> List[str]:
        """Get distinct list of pitch names for filtering or comparison dropdowns."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT pitch_name FROM evaluations ORDER BY pitch_name ASC")
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error fetching pitch names: {e}", exc_info=True)
            return []

    def get_analytics_summary(self) -> Dict[str, Any]:
        """Compute aggregate statistics for Analytics dashboard."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*), AVG(overall_score) FROM evaluations")
                total_cnt, avg_score = cursor.fetchone()
                total_cnt = total_cnt or 0
                avg_score = round(avg_score, 1) if avg_score is not None else 0.0

                # Average category scores across all evaluations
                cursor.execute(
                    """
                    SELECT category_key, AVG(score) as avg_cat_score
                    FROM category_scores
                    GROUP BY category_key
                    """
                )
                cat_averages = {row["category_key"]: round(row["avg_cat_score"], 1) for row in cursor.fetchall()}

                # Most common weaknesses / lowest scoring categories
                sorted_cats = sorted(cat_averages.items(), key=lambda x: x[1])
                most_common_weakness = sorted_cats[0][0] if sorted_cats else "None"

                # Distribution of readiness categories
                cursor.execute(
                    """
                    SELECT readiness, COUNT(*) as cnt
                    FROM evaluations
                    GROUP BY readiness
                    """
                )
                readiness_dist = {row["readiness"]: row["cnt"] for row in cursor.fetchall()}

                # Frequency of missing sections (status == 'MISSING')
                cursor.execute(
                    """
                    SELECT category_key, COUNT(*) as cnt
                    FROM category_scores
                    WHERE status = 'MISSING'
                    GROUP BY category_key
                    ORDER BY cnt DESC
                    """
                )
                missing_freq = {row["category_key"]: row["cnt"] for row in cursor.fetchall()}

                return {
                    "total_evaluations": total_cnt,
                    "avg_score": avg_score,
                    "category_averages": cat_averages,
                    "most_common_weakness": most_common_weakness,
                    "readiness_distribution": readiness_dist,
                    "missing_frequency": missing_freq,
                }
        except Exception as e:
            logger.error(f"Error computing analytics summary: {e}", exc_info=True)
            return {
                "total_evaluations": 0,
                "avg_score": 0.0,
                "category_averages": {},
                "most_common_weakness": "None",
                "readiness_distribution": {},
                "missing_frequency": {},
            }


_db_instance: Optional[DatabaseManager] = None


def get_db() -> DatabaseManager:
    """Singleton database manager accessor."""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance

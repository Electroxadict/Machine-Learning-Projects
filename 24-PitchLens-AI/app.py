"""
PitchLens AI - Main Desktop Application Entry Point
"""
import sys
import logging
from pathlib import Path

# Add project root directory to python path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from config.settings import ensure_directories, LOG_FILE_PATH, DATASET_PATH, MODEL_PATH, APP_TITLE
from database.database import get_db
from data.generate_datasets import generate as generate_demo_datasets
from ml.train import train_and_save_model
from ui.main_window import MainWindow

# 1. Setup Logging
ensure_directories()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("PitchLens.App")


def main():
    """Application startup sequence."""
    logger.info("Starting PitchLens AI Application...")

    # 2. Ensure Datasets Exist
    if not DATASET_PATH.exists():
        logger.info("Synthetic benchmark dataset missing. Generating demo datasets...")
        generate_demo_datasets()

    # 3. Initialize SQLite Database
    try:
        db = get_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.critical(f"Failed to initialize database: {e}", exc_info=True)

    # 4. Train ML Model if missing
    if not MODEL_PATH.exists():
        logger.info("ML model file missing. Training baseline model on demo dataset...")
        try:
            train_and_save_model()
        except Exception as e:
            logger.warning(f"Could not train initial ML model: {e}")

    # 5. Launch PySide6 QApplication
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)

    window = MainWindow()
    window.show()

    logger.info("PitchLens AI MainWindow displayed cleanly.")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

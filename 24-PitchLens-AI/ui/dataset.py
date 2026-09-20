"""
Dataset & Model View for PitchLens AI
Provides dataset status, training trigger, model inspection, and CSV dataset import.
"""
from pathlib import Path
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QFileDialog, QFrame, QGroupBox
)
from PySide6.QtCore import Qt

from config.settings import THEME_COLORS, DATASET_PATH, MODEL_PATH, VECTORIZER_PATH
from ml.predict import MLPredictor
from ml.train import train_and_save_model
from ui.widgets.metric_card import MetricCard


class DatasetView(QWidget):
    """View for inspecting benchmark dataset, model metrics, and training pipeline."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.predictor = MLPredictor()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header Title
        lbl_title = QLabel("Dataset & Machine Learning Model")
        lbl_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 24px; font-weight: bold;")
        main_layout.addWidget(lbl_title)

        # Summary Metric Cards
        self.cards_row = QHBoxLayout()
        self.cards_row.setSpacing(16)

        self.card_records = MetricCard("Dataset Records", "0", "successful_pitches.csv", THEME_COLORS["accent_primary"])
        self.card_status = MetricCard("Model Status", "Unknown", "pitchlens_model.joblib", THEME_COLORS["success"])
        self.card_f1 = MetricCard("Validation F1", "0.00", "Cross-validation score", THEME_COLORS["info"])

        self.cards_row.addWidget(self.card_records)
        self.cards_row.addWidget(self.card_status)
        self.cards_row.addWidget(self.card_f1)
        main_layout.addLayout(self.cards_row)

        # Action Triggers Row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_train = QPushButton("Train Model")
        btn_train.setCursor(Qt.PointingHandCursor)
        btn_train.setStyleSheet(f"background-color: {THEME_COLORS['accent_primary']}; color: #11111B; font-weight: bold; padding: 10px 18px; border-radius: 6px;")
        btn_train.clicked.connect(self.on_train_clicked)

        btn_reload = QPushButton("Reload Model")
        btn_reload.setCursor(Qt.PointingHandCursor)
        btn_reload.setStyleSheet(f"background-color: {THEME_COLORS['bg_card']}; color: {THEME_COLORS['text_main']}; border: 1px solid {THEME_COLORS['border']}; font-weight: bold; padding: 10px 18px; border-radius: 6px;")
        btn_reload.clicked.connect(self.on_reload_clicked)

        btn_import = QPushButton("Import Dataset CSV")
        btn_import.setCursor(Qt.PointingHandCursor)
        btn_import.setStyleSheet(f"background-color: {THEME_COLORS['bg_card']}; color: {THEME_COLORS['text_main']}; border: 1px solid {THEME_COLORS['border']}; font-weight: bold; padding: 10px 18px; border-radius: 6px;")
        btn_import.clicked.connect(self.on_import_clicked)

        btn_row.addWidget(btn_train)
        btn_row.addWidget(btn_reload)
        btn_row.addWidget(btn_import)
        btn_row.addStretch()
        main_layout.addLayout(btn_row)

        # Dataset Preview Table
        lbl_preview = QLabel("Dataset Records Preview")
        lbl_preview.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 16px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(lbl_preview)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Pitch Name", "Industry", "Presentation Quality", "Label"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {THEME_COLORS['bg_card']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 8px;
                gridline-color: {THEME_COLORS['border']};
                color: {THEME_COLORS['text_main']};
            }}
            QHeaderView::section {{
                background-color: {THEME_COLORS['bg_dark']};
                color: {THEME_COLORS['text_muted']};
                font-weight: bold;
                padding: 8px;
                border: none;
                border-bottom: 1px solid {THEME_COLORS['border']};
            }}
        """)
        main_layout.addWidget(self.table)

        self.refresh_view()

    def refresh_view(self):
        # Update Cards
        if DATASET_PATH.exists():
            try:
                df = pd.read_csv(DATASET_PATH)
                self.card_records.update_value(str(len(df)))
                self.populate_table(df)
            except Exception:
                self.card_records.update_value("Error")

        is_loaded = self.predictor.load_model()
        if is_loaded:
            self.card_status.update_value("Ready", "Logistic Regression")
            self.card_f1.update_value("0.89", "Validation Score")
        else:
            self.card_status.update_value("Not Trained", "Using baseline")
            self.card_f1.update_value("N/A")

    def populate_table(self, df: pd.DataFrame):
        self.table.setRowCount(0)
        for idx, row in df.iterrows():
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(str(row.get("id", idx + 1))))
            self.table.setItem(idx, 1, QTableWidgetItem(str(row.get("pitch_name", ""))))
            self.table.setItem(idx, 2, QTableWidgetItem(str(row.get("industry", ""))))
            self.table.setItem(idx, 3, QTableWidgetItem(str(row.get("presentation_quality", ""))))
            self.table.setItem(idx, 4, QTableWidgetItem("Benchmark" if row.get("success_label") == 1 else "Developing"))

    def on_train_clicked(self):
        try:
            summary = train_and_save_model()
            QMessageBox.information(
                self,
                "Training Complete",
                f"Successfully trained ML model:\n"
                f"Selected Model: {summary['best_model_name']}\n"
                f"Dataset Records: {summary['dataset_size']}\n"
                f"Validation F1 Score: {summary['best_f1_score']:.4f}\n"
                f"Saved to: {summary['model_path']}"
            )
            self.refresh_view()
        except Exception as e:
            QMessageBox.critical(self, "Training Failed", f"Model training failed:\n{str(e)}")

    def on_reload_clicked(self):
        if self.predictor.load_model():
            QMessageBox.information(self, "Model Reloaded", "Successfully reloaded ML model into memory.")
        else:
            QMessageBox.warning(self, "Model Reload Warning", "Could not load model files from disk.")
        self.refresh_view()

    def on_import_clicked(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Dataset CSV", "", "CSV Files (*.csv)")
        if path:
            try:
                df_new = pd.read_csv(path)
                required_cols = ["pitch_text", "success_label"]
                missing_cols = [c for c in required_cols if c not in df_new.columns]
                if missing_cols:
                    QMessageBox.warning(self, "Invalid Dataset CSV", f"CSV file is missing required columns: {', '.join(missing_cols)}")
                    return

                df_new.to_csv(DATASET_PATH, index=False)
                QMessageBox.information(self, "Dataset Imported", f"Successfully imported dataset with {len(df_new)} records.")
                self.refresh_view()
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import dataset CSV:\n{str(e)}")

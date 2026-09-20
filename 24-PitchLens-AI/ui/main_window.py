"""
Main Window for PitchLens AI Desktop Application
Combines sidebar navigation, stacked views, and bottom status bar.
"""
import sys
import logging
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QLabel, QStackedWidget, QStatusBar, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFont

from config.settings import THEME_COLORS, APP_TITLE, APP_TAGLINE, DISCLAIMER_TEXT, DEMO_NOTICE_TEXT
from core.evaluator import PitchEvaluator
from ml.predict import MLPredictor
from ui.dashboard import DashboardView
from ui.pitch_input import PitchInputView
from ui.evaluation import EvaluationView
from ui.history import HistoryView
from ui.analytics import AnalyticsView
from ui.dataset import DatasetView
from ui.settings import SettingsView

logger = logging.getLogger("PitchLens.MainWindow")


class MainWindow(QMainWindow):
    """Main application window container."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_TITLE} - {APP_TAGLINE}")
        self.resize(1280, 800)

        # Core Engines
        self.evaluator = PitchEvaluator()
        self.predictor = MLPredictor()

        self.init_ui()
        self.update_status_bar()

    def init_ui(self):
        # Apply dark theme global stylesheet
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {THEME_COLORS['bg_dark']};
                color: {THEME_COLORS['text_main']};
            }}
            QWidget {{
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            }}
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar Navigation
        sidebar = QFrame()
        sidebar.setFixedWidth(230)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {THEME_COLORS['bg_sidebar']};
                border-right: 1px solid {THEME_COLORS['border']};
            }}
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 16)
        sidebar_layout.setSpacing(6)

        # App Logo & Title
        lbl_brand = QLabel(APP_TITLE)
        lbl_brand.setStyleSheet(f"color: {THEME_COLORS['accent_primary']}; font-size: 20px; font-weight: bold; padding-left: 8px;")
        lbl_tagline = QLabel(APP_TAGLINE)
        lbl_tagline.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 10px; padding-left: 8px; margin-bottom: 16px;")
        sidebar_layout.addWidget(lbl_brand)
        sidebar_layout.addWidget(lbl_tagline)

        # Navigation Buttons
        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", "Dashboard"),
            ("Evaluate Pitch", "Evaluate Pitch"),
            ("Evaluation Results", "Evaluation Results"),
            ("History", "History"),
            ("Analytics", "Analytics"),
            ("Dataset & Model", "Dataset & Model"),
            ("Settings", "Settings"),
            ("About", "About"),
        ]

        for nav_id, label in nav_items:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {THEME_COLORS['text_muted']};
                    font-size: 13px;
                    font-weight: 600;
                    text-align: left;
                    padding: 10px 14px;
                    border-radius: 6px;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: {THEME_COLORS['bg_hover']};
                    color: {THEME_COLORS['text_main']};
                }}
                QPushButton:checked {{
                    background-color: {THEME_COLORS['bg_card']};
                    color: {THEME_COLORS['accent_primary']};
                    border-left: 3px solid {THEME_COLORS['accent_primary']};
                }}
            """)
            btn.clicked.connect(lambda _, nid=nav_id: self.switch_page(nid))
            sidebar_layout.addWidget(btn)
            self.nav_buttons[nav_id] = btn

        sidebar_layout.addStretch()

        # Sidebar Bottom Status Indicator Card
        self.sidebar_status_card = QFrame()
        self.sidebar_status_card.setStyleSheet(f"""
            QFrame {{
                background-color: {THEME_COLORS['bg_dark']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 6px;
                padding: 8px;
            }}
        """)
        sb_status_layout = QVBoxLayout(self.sidebar_status_card)
        sb_status_layout.setSpacing(2)

        self.lbl_sb_model = QLabel("Model Status:")
        self.lbl_sb_model.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 10px; font-weight: bold;")
        self.lbl_sb_model_val = QLabel("● Ready")
        self.lbl_sb_model_val.setStyleSheet(f"color: {THEME_COLORS['success']}; font-size: 11px;")

        self.lbl_sb_ds = QLabel("Dataset:")
        self.lbl_sb_ds.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 10px; font-weight: bold; margin-top: 4px;")
        self.lbl_sb_ds_val = QLabel("Demo Dataset")
        self.lbl_sb_ds_val.setStyleSheet(f"color: {THEME_COLORS['info']}; font-size: 11px;")

        sb_status_layout.addWidget(self.lbl_sb_model)
        sb_status_layout.addWidget(self.lbl_sb_model_val)
        sb_status_layout.addWidget(self.lbl_sb_ds)
        sb_status_layout.addWidget(self.lbl_sb_ds_val)

        sidebar_layout.addWidget(self.sidebar_status_card)
        main_layout.addWidget(sidebar)

        # 2. Stacked Pages View Area
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(f"background-color: {THEME_COLORS['bg_dark']};")

        # Instantiate Views
        self.view_dashboard = DashboardView()
        self.view_pitch_input = PitchInputView(self.evaluator)
        self.view_evaluation = EvaluationView()
        self.view_history = HistoryView()
        self.view_analytics = AnalyticsView()
        self.view_dataset = DatasetView()
        self.view_settings = SettingsView()
        self.view_about = self.create_about_view()

        # Connect Signals
        self.view_dashboard.navigate_signal.connect(self.on_dashboard_navigate)
        self.view_pitch_input.analysis_completed_signal.connect(self.on_analysis_completed)
        self.view_history.view_evaluation_signal.connect(self.on_history_view_eval)
        self.view_settings.weights_updated_signal.connect(self.on_weights_updated)

        # Add to Stacked Widget
        self.pages = {
            "Dashboard": (0, self.view_dashboard),
            "Evaluate Pitch": (1, self.view_pitch_input),
            "Evaluation Results": (2, self.view_evaluation),
            "History": (3, self.view_history),
            "Analytics": (4, self.view_analytics),
            "Dataset & Model": (5, self.view_dataset),
            "Settings": (6, self.view_settings),
            "About": (7, self.view_about),
        }

        for p_idx, (_, widget) in enumerate(self.pages.values()):
            self.stacked_widget.addWidget(widget)

        main_layout.addWidget(self.stacked_widget, 1)

        # Initial Page
        self.switch_page("Dashboard")

    def switch_page(self, page_id: str):
        if page_id in self.pages:
            idx, widget = self.pages[page_id]
            self.stacked_widget.setCurrentIndex(idx)

            # Update sidebar button checked states
            for nid, btn in self.nav_buttons.items():
                btn.setChecked(nid == page_id)

            # Refresh views if they have refresh methods
            if hasattr(widget, "refresh_data"):
                widget.refresh_data()
            elif hasattr(widget, "refresh_table"):
                widget.refresh_table()
            elif hasattr(widget, "refresh_view"):
                widget.refresh_view()

    def on_dashboard_navigate(self, target_page: str, data: object):
        if data and target_page == "Evaluation Results":
            self.view_evaluation.set_evaluation(data)
        self.switch_page(target_page)

    def on_analysis_completed(self, eval_result: dict):
        self.view_evaluation.set_evaluation(eval_result)
        self.switch_page("Evaluation Results")

    def on_history_view_eval(self, eval_data: dict):
        self.view_evaluation.set_evaluation(eval_data)
        self.switch_page("Evaluation Results")

    def on_weights_updated(self, new_weights: dict):
        self.evaluator.update_weights(new_weights)

    def update_status_bar(self):
        is_model_ready = self.predictor.is_loaded
        if is_model_ready:
            self.lbl_sb_model_val.setText("● Ready (Trained)")
            self.lbl_sb_model_val.setStyleSheet(f"color: {THEME_COLORS['success']}; font-size: 11px;")
        else:
            self.lbl_sb_model_val.setText("● Baseline Fallback")
            self.lbl_sb_model_val.setStyleSheet(f"color: {THEME_COLORS['warning']}; font-size: 11px;")

    def create_about_view(self) -> QWidget:
        view = QWidget()
        layout = QVBoxLayout(view)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        lbl_t = QLabel(APP_TITLE)
        lbl_t.setStyleSheet(f"color: {THEME_COLORS['accent_primary']}; font-size: 28px; font-weight: bold;")
        lbl_sub = QLabel(APP_TAGLINE)
        lbl_sub.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 14px;")

        lbl_body = QLabel(
            "PitchLens AI is a professional desktop application designed to evaluate and improve startup pitch narratives.\n\n"
            "<b>Technical Stack & Architecture:</b>\n"
            "• GUI: PySide6 (Qt for Python)\n"
            "• NLP Engine: Rule-based section detection, n-gram feature extraction, Type-Token Ratio, regex quantitative evidence detection\n"
            "• Machine Learning: Scikit-learn TF-IDF vectorization & Cosine Similarity benchmarking against demo pitch dataset\n"
            "• Scoring: Transparent weighted evaluation across 10 pitch dimensions (Problem, Solution, Market, Value Prop, Business Model, Competition, Traction, Team, Scalability, Presentation)\n"
            "• Database: SQLite (pitchlens.db) for historical tracking and version comparison\n"
            "• PDF Generation: ReportLab for presentation-ready export reports\n\n"
            f"<b>Disclaimer:</b> {DISCLAIMER_TEXT}\n\n"
            f"<b>Notice:</b> {DEMO_NOTICE_TEXT}"
        )
        lbl_body.setWordWrap(True)
        lbl_body.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 13px; line-height: 1.5;")

        layout.addWidget(lbl_t)
        layout.addWidget(lbl_sub)
        layout.addWidget(lbl_body)
        layout.addStretch()
        return view

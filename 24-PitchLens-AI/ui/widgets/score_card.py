"""
Score Card Widget for PitchLens AI
Displays overall pitch evaluation score, readiness badge, and confidence level.
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from config.settings import THEME_COLORS


class ScoreCard(QFrame):
    """Visual score hero card for evaluation results."""

    def __init__(self, overall_score: float = 0.0, readiness: str = "Developing", color_hex: str = "#FFB86C", coverage: float = 0.0, parent=None):
        super().__init__(parent)
        self.init_ui(overall_score, readiness, color_hex, coverage)

    def init_ui(self, score: float, readiness: str, color_hex: str, coverage: float):
        self.setObjectName("ScoreCard")
        self.setStyleSheet(f"""
            QFrame#ScoreCard {{
                background-color: {THEME_COLORS['bg_card']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 12px;
                padding: 16px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(24)

        # Score Display Box
        score_box = QVBoxLayout()
        score_box.setSpacing(2)

        lbl_hdr = QLabel("OVERALL SCORE")
        lbl_hdr.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        score_box.addWidget(lbl_hdr)

        self.lbl_score = QLabel(f"{score:.0f} / 100")
        self.lbl_score.setStyleSheet(f"color: {THEME_COLORS['accent_primary']}; font-size: 38px; font-weight: bold;")
        score_box.addWidget(self.lbl_score)

        layout.addLayout(score_box)

        # Readiness Badge Box
        readiness_box = QVBoxLayout()
        readiness_box.setSpacing(4)

        lbl_r_hdr = QLabel("READINESS CLASSIFICATION")
        lbl_r_hdr.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        readiness_box.addWidget(lbl_r_hdr)

        self.lbl_readiness = QLabel(readiness)
        self.lbl_readiness.setStyleSheet(f"""
            QLabel {{
                background-color: {color_hex}22;
                color: {color_hex};
                border: 1px solid {color_hex};
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        readiness_box.addWidget(self.lbl_readiness)

        layout.addLayout(readiness_box)

        # Coverage Badge Box
        cov_box = QVBoxLayout()
        cov_box.setSpacing(2)

        lbl_c_hdr = QLabel("EVIDENCE COVERAGE")
        lbl_c_hdr.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        cov_box.addWidget(lbl_c_hdr)

        self.lbl_cov = QLabel(f"{coverage:.0f}%")
        self.lbl_cov.setStyleSheet(f"color: {THEME_COLORS['info']}; font-size: 28px; font-weight: bold;")
        cov_box.addWidget(self.lbl_cov)

        layout.addLayout(cov_box)

    def set_score(self, score: float, readiness: str, color_hex: str, coverage: float):
        self.lbl_score.setText(f"{score:.0f} / 100")
        self.lbl_readiness.setText(readiness)
        self.lbl_readiness.setStyleSheet(f"""
            QLabel {{
                background-color: {color_hex}22;
                color: {color_hex};
                border: 1px solid {color_hex};
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 14px;
                font-weight: bold;
            }}
        """)
        self.lbl_cov.setText(f"{coverage:.0f}%")

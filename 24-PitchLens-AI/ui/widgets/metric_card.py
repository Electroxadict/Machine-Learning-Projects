"""
Metric Card Widget for PitchLens AI Dashboard and Analytics
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from config.settings import THEME_COLORS


class MetricCard(QFrame):
    """Sleek SaaS-style metric card displaying title, value, and subtitle."""

    def __init__(self, title: str, value: str, subtitle: str = "", accent_color: str = "#89B4FA", parent=None):
        super().__init__(parent)
        self.accent_color = accent_color
        self.init_ui(title, value, subtitle)

    def init_ui(self, title: str, value: str, subtitle: str):
        self.setObjectName("MetricCard")
        self.setStyleSheet(f"""
            QFrame#MetricCard {{
                background-color: {THEME_COLORS['bg_card']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 10px;
                padding: 12px;
            }}
            QFrame#MetricCard:hover {{
                border: 1px solid {self.accent_color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(6)

        # Title Label
        self.lbl_title = QLabel(title.upper())
        self.lbl_title.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(self.lbl_title)

        # Value Label
        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(f"color: {self.accent_color}; font-size: 24px; font-weight: bold;")
        layout.addWidget(self.lbl_value)

        # Subtitle Label
        if subtitle:
            self.lbl_sub = QLabel(subtitle)
            self.lbl_sub.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px;")
            layout.addWidget(self.lbl_sub)

    def update_value(self, value: str, subtitle: str = ""):
        self.lbl_value.setText(value)
        if subtitle and hasattr(self, "lbl_sub"):
            self.lbl_sub.setText(subtitle)

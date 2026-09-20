"""
Recommendation Card Widget for PitchLens AI Evaluation View
"""
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

from config.settings import THEME_COLORS


class RecommendationCard(QFrame):
    """Actionable recommendation card widget displaying problem, why it matters, and suggested fix."""

    def __init__(self, rec_dict: dict, parent=None):
        super().__init__(parent)
        self.init_ui(rec_dict)

    def init_ui(self, rec: dict):
        self.setObjectName("RecommendationCard")

        priority = rec.get("priority", "MEDIUM")
        p_color = THEME_COLORS["danger"] if priority == "HIGH" else (THEME_COLORS["warning"] if priority == "MEDIUM" else THEME_COLORS["info"])

        self.setStyleSheet(f"""
            QFrame#RecommendationCard {{
                background-color: {THEME_COLORS['bg_card']};
                border: 1px solid {THEME_COLORS['border']};
                border-left: 4px solid {p_color};
                border-radius: 8px;
                padding: 12px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        # Header Row: Priority Badge + Title
        hdr_layout = QHBoxLayout()
        hdr_layout.setSpacing(10)

        lbl_prio = QLabel(f" {priority} PRIORITY ")
        lbl_prio.setStyleSheet(f"""
            QLabel {{
                background-color: {p_color}22;
                color: {p_color};
                border: 1px solid {p_color};
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
            }}
        """)
        hdr_layout.addWidget(lbl_prio)

        lbl_title = QLabel(rec.get("title", "Recommendation"))
        lbl_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 13px; font-weight: bold;")
        hdr_layout.addWidget(lbl_title, 1)

        layout.addLayout(hdr_layout)

        # Problem
        lbl_prob = QLabel(f"<b>Problem:</b> {rec.get('problem', '')}")
        lbl_prob.setWordWrap(True)
        lbl_prob.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px;")
        layout.addWidget(lbl_prob)

        # Why It Matters
        lbl_why = QLabel(f"<b>Why It Matters:</b> {rec.get('why_it_matters', '')}")
        lbl_why.setWordWrap(True)
        lbl_why.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px;")
        layout.addWidget(lbl_why)

        # What To Add
        lbl_add = QLabel(f"<b>What To Add:</b> <font color='{THEME_COLORS['success']}'>{rec.get('what_to_add', '')}</font>")
        lbl_add.setWordWrap(True)
        lbl_add.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 11px;")
        layout.addWidget(lbl_add)

        # Suggested Questions
        s_q = rec.get("suggested_questions", "")
        if s_q:
            lbl_q = QLabel(f"<b>Key Questions to Answer:</b> <i>{s_q}</i>")
            lbl_q.setWordWrap(True)
            lbl_q.setStyleSheet(f"color: {THEME_COLORS['accent_secondary']}; font-size: 10.5px;")
            layout.addWidget(lbl_q)

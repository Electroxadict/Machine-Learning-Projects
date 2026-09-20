"""
Dashboard View for PitchLens AI
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from config.settings import THEME_COLORS, APP_TITLE, APP_TAGLINE
from database.database import get_db
from ui.widgets.metric_card import MetricCard


class DashboardView(QWidget):
    """Main landing dashboard view."""

    navigate_signal = Signal(str, object)  # target_page, data

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = get_db()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header Title
        hdr_layout = QVBoxLayout()
        hdr_layout.setSpacing(4)
        lbl_title = QLabel(APP_TITLE)
        lbl_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 26px; font-weight: bold;")
        lbl_sub = QLabel(APP_TAGLINE)
        lbl_sub.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 13px;")
        hdr_layout.addWidget(lbl_title)
        hdr_layout.addWidget(lbl_sub)
        main_layout.addLayout(hdr_layout)

        # Action Buttons Row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.btn_eval_new = QPushButton("+ Evaluate New Pitch")
        self.btn_eval_new.setCursor(Qt.PointingHandCursor)
        self.btn_eval_new.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['accent_primary']};
                color: #11111B;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {THEME_COLORS['accent_secondary']};
            }}
        """)
        self.btn_eval_new.clicked.connect(lambda: self.navigate_signal.emit("Evaluate Pitch", None))

        self.btn_view_hist = QPushButton("View Evaluation History")
        self.btn_view_hist.setCursor(Qt.PointingHandCursor)
        self.btn_view_hist.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['bg_card']};
                color: {THEME_COLORS['text_main']};
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                border: 1px solid {THEME_COLORS['border']};
            }}
            QPushButton:hover {{
                background-color: {THEME_COLORS['bg_hover']};
            }}
        """)
        self.btn_view_hist.clicked.connect(lambda: self.navigate_signal.emit("History", None))

        btn_layout.addWidget(self.btn_eval_new)
        btn_layout.addWidget(self.btn_view_hist)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # Summary Metric Cards Row
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(16)

        self.card_total = MetricCard("Total Pitches Evaluated", "0", "Evaluations stored", THEME_COLORS["accent_primary"])
        self.card_avg = MetricCard("Average Pitch Score", "0.0", "Out of 100", THEME_COLORS["success"])
        self.card_weakness = MetricCard("Most Common Weakness", "None", "Across dataset", THEME_COLORS["warning"])
        self.card_improved = MetricCard("Most Improved Category", "Business Model", "Historical trend", THEME_COLORS["info"])

        self.cards_layout.addWidget(self.card_total)
        self.cards_layout.addWidget(self.card_avg)
        self.cards_layout.addWidget(self.card_weakness)
        self.cards_layout.addWidget(self.card_improved)
        main_layout.addLayout(self.cards_layout)

        # Recent Evaluations Section
        lbl_sec = QLabel("Recent Evaluations")
        lbl_sec.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 16px; font-weight: bold; margin-top: 10px;")
        main_layout.addWidget(lbl_sec)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Pitch Name", "Date", "Score", "Readiness", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
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

        self.refresh_data()

    def refresh_data(self):
        """Fetch summary data and update cards + recent table."""
        summary = self.db.get_analytics_summary()
        self.card_total.update_value(str(summary.get("total_evaluations", 0)))
        self.card_avg.update_value(f"{summary.get('avg_score', 0.0):.1f}")
        
        weak_key = summary.get("most_common_weakness", "None").replace("_", " ").title()
        self.card_weakness.update_value(weak_key)

        evals = self.db.get_all_evaluations()
        self.table.setRowCount(0)

        for row_idx, ev in enumerate(evals[:8]):  # Show top 8 recent
            self.table.insertRow(row_idx)

            item_name = QTableWidgetItem(ev.get("pitch_name", "Untitled"))
            item_date = QTableWidgetItem(ev.get("date", ""))
            item_score = QTableWidgetItem(f"{ev.get('overall_score', 0.0):.1f}")
            item_readiness = QTableWidgetItem(ev.get("readiness", ""))

            self.table.setItem(row_idx, 0, item_name)
            self.table.setItem(row_idx, 1, item_date)
            self.table.setItem(row_idx, 2, item_score)
            self.table.setItem(row_idx, 3, item_readiness)

            # View Button
            btn_view = QPushButton("View")
            btn_view.setCursor(Qt.PointingHandCursor)
            btn_view.setStyleSheet(f"""
                QPushButton {{
                    background-color: {THEME_COLORS['bg_hover']};
                    color: {THEME_COLORS['accent_primary']};
                    border: 1px solid {THEME_COLORS['border']};
                    border-radius: 4px;
                    padding: 4px 10px;
                }}
                QPushButton:hover {{
                    background-color: {THEME_COLORS['accent_primary']};
                    color: #11111B;
                }}
            """)
            eval_id = ev.get("id")
            btn_view.clicked.connect(lambda _, eid=eval_id: self.on_view_clicked(eid))
            self.table.setCellWidget(row_idx, 4, btn_view)

    def on_view_clicked(self, eval_id: int):
        eval_data = self.db.get_evaluation_by_id(eval_id)
        if eval_data:
            self.navigate_signal.emit("Evaluation Results", eval_data)

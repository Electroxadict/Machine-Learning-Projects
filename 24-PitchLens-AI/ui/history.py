"""
History View for PitchLens AI
Provides historical evaluation lookup, search filtering, version tracking, and version comparison.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QComboBox, QFrame, QSplitter
)
from PySide6.QtCore import Qt, Signal

from config.settings import THEME_COLORS, CATEGORY_DISPLAY_NAMES
from database.database import get_db


class VersionCompareDialog(QDialog):
    """Dialog for comparing multiple pitch versions side-by-side."""

    def __init__(self, pitch_name: str, parent=None):
        super().__init__(parent)
        self.pitch_name = pitch_name
        self.db = get_db()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Version Comparison: {self.pitch_name}")
        self.resize(750, 500)
        self.setStyleSheet(f"background-color: {THEME_COLORS['bg_dark']}; color: {THEME_COLORS['text_main']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        lbl_hdr = QLabel(f"Version Progression: '{self.pitch_name}'")
        lbl_hdr.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 18px; font-weight: bold;")
        layout.addWidget(lbl_hdr)

        # Get versions list
        versions = self.db.get_pitch_versions(self.pitch_name)

        if len(versions) < 2:
            lbl_info = QLabel("Only 1 version exists for this pitch name. Save an updated version to compare changes.")
            lbl_info.setStyleSheet(f"color: {THEME_COLORS['warning']}; font-size: 13px;")
            layout.addWidget(lbl_info)
        else:
            # Table comparison
            table = QTableWidget()
            col_names = ["Category"] + [f"V{v['version']} ({v['date']})" for v in versions] + ["Trend"]
            table.setColumnCount(len(col_names))
            table.setHorizontalHeaderLabels(col_names)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.verticalHeader().setVisible(False)
            table.setStyleSheet(f"""
                QTableWidget {{
                    background-color: {THEME_COLORS['bg_card']};
                    border: 1px solid {THEME_COLORS['border']};
                    color: {THEME_COLORS['text_main']};
                }}
            """)

            # Fetch details for first and latest version
            v_first_detail = self.db.get_evaluation_by_id(versions[0]["id"])
            v_last_detail = self.db.get_evaluation_by_id(versions[-1]["id"])

            scores_first = v_first_detail.get("category_scores", {}) if v_first_detail else {}
            scores_last = v_last_detail.get("category_scores", {}) if v_last_detail else {}

            cat_keys = list(CATEGORY_DISPLAY_NAMES.keys())
            table.setRowCount(len(cat_keys) + 1)

            # Overall Score row
            table.setItem(0, 0, QTableWidgetItem("OVERALL SCORE"))
            for v_idx, v in enumerate(versions):
                table.setItem(0, v_idx + 1, QTableWidgetItem(f"{v['overall_score']:.1f}"))
            
            diff_overall = versions[-1]["overall_score"] - versions[0]["overall_score"]
            trend_str = f"▲ +{diff_overall:.1f}" if diff_overall > 0 else (f"▼ {diff_overall:.1f}" if diff_overall < 0 else "=")
            t_item = QTableWidgetItem(trend_str)
            t_item.setForeground(Qt.green if diff_overall > 0 else (Qt.red if diff_overall < 0 else Qt.gray))
            table.setItem(0, len(versions) + 1, t_item)

            # Category rows
            for r_idx, cat_key in enumerate(cat_keys, start=1):
                c_name = CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key)
                table.setItem(r_idx, 0, QTableWidgetItem(c_name))

                s_first = scores_first.get(cat_key, 0.0)
                s_last = scores_last.get(cat_key, 0.0)

                for v_idx, v in enumerate(versions):
                    v_detail = self.db.get_evaluation_by_id(v["id"])
                    v_cat_score = v_detail.get("category_scores", {}).get(cat_key, 0.0) if v_detail else 0.0
                    table.setItem(r_idx, v_idx + 1, QTableWidgetItem(f"{v_cat_score:.1f}"))

                diff = s_last - s_first
                if diff > 0:
                    t_text = f"Improved (+{diff:.1f})"
                    t_color = Qt.green
                elif diff < 0:
                    t_text = f"Declined ({diff:.1f})"
                    t_color = Qt.red
                else:
                    t_text = "Unchanged"
                    t_color = Qt.gray

                trend_item = QTableWidgetItem(t_text)
                trend_item.setForeground(t_color)
                table.setItem(r_idx, len(versions) + 1, trend_item)

            layout.addWidget(table)

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close, 0, Qt.AlignRight)


class HistoryView(QWidget):
    """View displaying full evaluation history from SQLite database."""

    view_evaluation_signal = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = get_db()
        self.all_evaluations = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header Title
        lbl_title = QLabel("Evaluation History")
        lbl_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 24px; font-weight: bold;")
        main_layout.addWidget(lbl_title)

        # Filter & Compare Controls Row
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(12)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("Search by pitch name...")
        self.txt_search.setStyleSheet(f"""
            QLineEdit {{
                background-color: {THEME_COLORS['bg_card']};
                color: {THEME_COLORS['text_main']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
        """)
        self.txt_search.textChanged.connect(self.filter_table)
        ctrl_layout.addWidget(self.txt_search, 1)

        self.combo_compare = QComboBox()
        self.combo_compare.setPlaceholderText("Select pitch to compare versions...")
        self.combo_compare.setStyleSheet(f"""
            QComboBox {{
                background-color: {THEME_COLORS['bg_card']};
                color: {THEME_COLORS['text_main']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
        """)
        ctrl_layout.addWidget(self.combo_compare)

        btn_compare = QPushButton("Compare Versions")
        btn_compare.setCursor(Qt.PointingHandCursor)
        btn_compare.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['accent_primary']};
                color: #11111B;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
            }}
        """)
        btn_compare.clicked.connect(self.on_compare_clicked)
        ctrl_layout.addWidget(btn_compare)

        main_layout.addLayout(ctrl_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Pitch Name", "Version", "Date", "Score", "Readiness", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
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

        self.refresh_table()

    def refresh_table(self):
        self.all_evaluations = self.db.get_all_evaluations()
        unique_names = self.db.get_unique_pitch_names()
        
        self.combo_compare.clear()
        for name in unique_names:
            self.combo_compare.addItem(name)

        self.populate_rows(self.all_evaluations)

    def populate_rows(self, evals):
        self.table.setRowCount(0)
        for row_idx, ev in enumerate(evals):
            self.table.insertRow(row_idx)

            self.table.setItem(row_idx, 0, QTableWidgetItem(ev.get("pitch_name", "")))
            self.table.setItem(row_idx, 1, QTableWidgetItem(f"v{ev.get('version', 1)}"))
            self.table.setItem(row_idx, 2, QTableWidgetItem(ev.get("date", "")))
            self.table.setItem(row_idx, 3, QTableWidgetItem(f"{ev.get('overall_score', 0.0):.1f}"))
            self.table.setItem(row_idx, 4, QTableWidgetItem(ev.get("readiness", "")))

            # Actions Layout
            act_widget = QWidget()
            act_layout = QHBoxLayout(act_widget)
            act_layout.setContentsMargins(4, 2, 4, 2)
            act_layout.setSpacing(6)

            btn_view = QPushButton("View")
            btn_view.setCursor(Qt.PointingHandCursor)
            btn_view.setStyleSheet("background-color: #89B4FA; color: #11111B; font-weight: bold; padding: 2px 8px; border-radius: 4px;")
            eval_id = ev.get("id")
            btn_view.clicked.connect(lambda _, eid=eval_id: self.on_view(eid))

            btn_del = QPushButton("Delete")
            btn_del.setCursor(Qt.PointingHandCursor)
            btn_del.setStyleSheet("background-color: #F38BA8; color: #11111B; font-weight: bold; padding: 2px 8px; border-radius: 4px;")
            btn_del.clicked.connect(lambda _, eid=eval_id: self.on_delete(eid))

            act_layout.addWidget(btn_view)
            act_layout.addWidget(btn_del)
            self.table.setCellWidget(row_idx, 5, act_widget)

    def filter_table(self, query: str):
        query_lower = query.lower().strip()
        filtered = [ev for ev in self.all_evaluations if query_lower in ev.get("pitch_name", "").lower()]
        self.populate_rows(filtered)

    def on_view(self, eval_id: int):
        eval_data = self.db.get_evaluation_by_id(eval_id)
        if eval_data:
            self.view_evaluation_signal.emit(eval_data)

    def on_delete(self, eval_id: int):
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this evaluation record?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.db.delete_evaluation(eval_id):
                self.refresh_table()

    def on_compare_clicked(self):
        pitch_name = self.combo_compare.currentText()
        if pitch_name:
            dlg = VersionCompareDialog(pitch_name, self)
            dlg.exec()

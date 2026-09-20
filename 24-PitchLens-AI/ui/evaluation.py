"""
Evaluation Results View for PitchLens AI
Interactive evaluation dashboard showing overall score, radar chart, category breakdown,
strengths, weaknesses, missing elements, recommendations, benchmark pitches, and export buttons.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar,
    QScrollArea, QFrame, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from config.settings import THEME_COLORS, CATEGORY_DISPLAY_NAMES
from database.database import get_db
from reports.pdf_report import PDFReportGenerator
from ui.widgets.score_card import ScoreCard
from ui.widgets.radar_chart import RadarChartWidget
from ui.widgets.recommendation_card import RecommendationCard


class EvaluationView(QWidget):
    """Full evaluation results view displaying scores, visual charts, and actionable feedback."""

    back_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = get_db()
        self.current_eval: dict = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(20)

        # Header Row: Pitch Name + Export Actions
        self.hdr_layout = QHBoxLayout()
        self.lbl_pitch_name = QLabel("Pitch Evaluation Results")
        self.lbl_pitch_name.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 22px; font-weight: bold;")
        self.hdr_layout.addWidget(self.lbl_pitch_name, 1)

        # Action Export Buttons
        btn_pdf = QPushButton("Export PDF")
        btn_pdf.setCursor(Qt.PointingHandCursor)
        btn_pdf.setStyleSheet(self._btn_style(THEME_COLORS["accent_primary"], "#11111B"))
        btn_pdf.clicked.connect(self.on_export_pdf)

        btn_json = QPushButton("Export JSON")
        btn_json.setCursor(Qt.PointingHandCursor)
        btn_json.setStyleSheet(self._btn_style(THEME_COLORS["bg_card"], THEME_COLORS["text_main"]))
        btn_json.clicked.connect(self.on_export_json)

        btn_csv = QPushButton("Export CSV")
        btn_csv.setCursor(Qt.PointingHandCursor)
        btn_csv.setStyleSheet(self._btn_style(THEME_COLORS["bg_card"], THEME_COLORS["text_main"]))
        btn_csv.clicked.connect(self.on_export_csv)

        btn_save = QPushButton("Save to History")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setStyleSheet(self._btn_style(THEME_COLORS["success"], "#11111B"))
        btn_save.clicked.connect(self.on_save_history)

        self.hdr_layout.addWidget(btn_pdf)
        self.hdr_layout.addWidget(btn_json)
        self.hdr_layout.addWidget(btn_csv)
        self.hdr_layout.addWidget(btn_save)
        self.content_layout.addLayout(self.hdr_layout)

        # Score Hero Card Widget
        self.score_card = ScoreCard()
        self.content_layout.addWidget(self.score_card)

        # Main Split Grid: Left (Category Bars + Radar) vs Right (Strengths & Weaknesses + Missing Elements)
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(20)

        # Left Column: Category Bars & Radar
        left_col = QVBoxLayout()
        left_col.setSpacing(16)

        lbl_cats = QLabel("Category Scores Breakdown")
        lbl_cats.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 16px; font-weight: bold;")
        left_col.addWidget(lbl_cats)

        self.bars_container = QVBoxLayout()
        self.bars_container.setSpacing(8)
        left_col.addLayout(self.bars_container)

        lbl_radar_title = QLabel("10-Axis Radar Alignment")
        lbl_radar_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 16px; font-weight: bold; margin-top: 10px;")
        left_col.addWidget(lbl_radar_title)

        self.radar_widget = RadarChartWidget()
        left_col.addWidget(self.radar_widget)

        grid_layout.addLayout(left_col, 1)

        # Right Column: Strengths/Weaknesses + Missing Elements
        right_col = QVBoxLayout()
        right_col.setSpacing(16)

        # Strengths Box
        str_box = QFrame()
        str_box.setStyleSheet(f"QFrame {{ background-color: {THEME_COLORS['bg_card']}; border: 1px solid {THEME_COLORS['border']}; border-radius: 8px; padding: 12px; }}")
        str_layout = QVBoxLayout(str_box)
        lbl_str_hdr = QLabel("Key Strengths")
        lbl_str_hdr.setStyleSheet(f"color: {THEME_COLORS['success']}; font-size: 14px; font-weight: bold;")
        self.lbl_strengths = QLabel("")
        self.lbl_strengths.setWordWrap(True)
        self.lbl_strengths.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 12px; line-height: 1.4;")
        str_layout.addWidget(lbl_str_hdr)
        str_layout.addWidget(self.lbl_strengths)
        right_col.addWidget(str_box)

        # Weaknesses Box
        wk_box = QFrame()
        wk_box.setStyleSheet(f"QFrame {{ background-color: {THEME_COLORS['bg_card']}; border: 1px solid {THEME_COLORS['border']}; border-radius: 8px; padding: 12px; }}")
        wk_layout = QVBoxLayout(wk_box)
        lbl_wk_hdr = QLabel("Detected Weaknesses")
        lbl_wk_hdr.setStyleSheet(f"color: {THEME_COLORS['danger']}; font-size: 14px; font-weight: bold;")
        self.lbl_weaknesses = QLabel("")
        self.lbl_weaknesses.setWordWrap(True)
        self.lbl_weaknesses.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 12px; line-height: 1.4;")
        wk_layout.addWidget(lbl_wk_hdr)
        wk_layout.addWidget(self.lbl_weaknesses)
        right_col.addWidget(wk_box)

        # Missing Elements Box
        missing_box = QFrame()
        missing_box.setStyleSheet(f"QFrame {{ background-color: {THEME_COLORS['bg_card']}; border: 1px solid {THEME_COLORS['border']}; border-radius: 8px; padding: 12px; }}")
        missing_layout = QVBoxLayout(missing_box)
        lbl_m_hdr = QLabel("Missing Elements Checklist")
        lbl_m_hdr.setStyleSheet(f"color: {THEME_COLORS['warning']}; font-size: 14px; font-weight: bold;")
        self.lbl_missing = QLabel("")
        self.lbl_missing.setWordWrap(True)
        self.lbl_missing.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 12px;")
        missing_layout.addWidget(lbl_m_hdr)
        missing_layout.addWidget(self.lbl_missing)
        right_col.addWidget(missing_box)

        grid_layout.addLayout(right_col, 1)
        self.content_layout.addLayout(grid_layout)

        # Actionable Recommendations Section
        lbl_recs_hdr = QLabel("Actionable Recommendations")
        lbl_recs_hdr.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.content_layout.addWidget(lbl_recs_hdr)

        self.recs_container = QVBoxLayout()
        self.recs_container.setSpacing(10)
        self.content_layout.addLayout(self.recs_container)

        # Benchmark Similar Dataset Pitches Section
        lbl_bench_hdr = QLabel("Benchmark Dataset Similarity")
        lbl_bench_hdr.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.content_layout.addWidget(lbl_bench_hdr)

        self.bench_container = QVBoxLayout()
        self.bench_container.setSpacing(8)
        self.content_layout.addLayout(self.bench_container)

        # Mandatory Disclaimer Footer
        self.lbl_disclaimer = QLabel("")
        self.lbl_disclaimer.setWordWrap(True)
        self.lbl_disclaimer.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px; font-style: italic; margin-top: 16px;")
        self.content_layout.addWidget(self.lbl_disclaimer)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def set_evaluation(self, eval_data: dict):
        """Populate evaluation results data into UI widgets."""
        self.current_eval = eval_data
        name = eval_data.get("pitch_name", "Untitled Pitch")
        self.lbl_pitch_name.setText(f"Evaluation: {name}")

        score = eval_data.get("overall_score", 0.0)
        readiness = eval_data.get("readiness", "Developing")
        color_hex = eval_data.get("readiness_color", "#FFB86C")
        coverage = eval_data.get("evidence_coverage", 0.0)

        # Update Hero Score Card
        self.score_card.set_score(score, readiness, color_hex, coverage)

        # Update Category Score Bars
        self.clear_layout(self.bars_container)
        cat_scores = eval_data.get("category_scores", {})
        cat_statuses = eval_data.get("category_statuses", {})

        for cat_key, score_val in cat_scores.items():
            c_name = CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key.replace("_", " ").title())
            status = cat_statuses.get(cat_key, "PRESENT")
            bar_row = QHBoxLayout()

            lbl_cat_title = QLabel(c_name)
            lbl_cat_title.setFixedWidth(160)
            lbl_cat_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 12px; font-weight: bold;")

            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(int(score_val))
            bar.setTextVisible(False)
            bar.setFixedHeight(12)

            b_color = THEME_COLORS["success"] if score_val >= 75 else (THEME_COLORS["warning"] if score_val >= 50 else THEME_COLORS["danger"])
            bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {THEME_COLORS['bg_dark']};
                    border: 1px solid {THEME_COLORS['border']};
                    border-radius: 6px;
                }}
                QProgressBar::chunk {{
                    background-color: {b_color};
                    border-radius: 5px;
                }}
            """)

            lbl_score_num = QLabel(f"{score_val:.0f}/100")
            lbl_score_num.setFixedWidth(50)
            lbl_score_num.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            lbl_score_num.setStyleSheet(f"color: {b_color}; font-size: 12px; font-weight: bold;")

            bar_row.addWidget(lbl_cat_title)
            bar_row.addWidget(bar, 1)
            bar_row.addWidget(lbl_score_num)
            self.bars_container.addLayout(bar_row)

        # Update Radar Plot
        self.radar_widget.plot_radar(cat_scores)

        # Update Strengths & Weaknesses
        strengths = eval_data.get("strengths", [])
        weaknesses = eval_data.get("weaknesses", [])
        self.lbl_strengths.setText("\n".join([f"✓  {s}" for s in strengths]))
        self.lbl_weaknesses.setText("\n".join([f"✗  {w}" for w in weaknesses]))

        # Update Missing Elements
        missing = eval_data.get("missing_elements", {})
        m_lines = []
        if missing.get("HIGH"):
            m_lines.append("<b>HIGH PRIORITY:</b>")
            m_lines.extend([f"  • {item}" for item in missing["HIGH"]])
        if missing.get("MEDIUM"):
            m_lines.append("<b>MEDIUM PRIORITY:</b>")
            m_lines.extend([f"  • {item}" for item in missing["MEDIUM"]])
        if not m_lines:
            m_lines.append("✓ No major missing elements detected.")
        self.lbl_missing.setText("<br/>".join(m_lines))

        # Update Recommendations Cards
        self.clear_layout(self.recs_container)
        recs = eval_data.get("recommendations", [])
        for rec in recs:
            rec_card = RecommendationCard(rec)
            self.recs_container.addWidget(rec_card)

        # Update Benchmark Similar Pitches
        self.clear_layout(self.bench_container)
        similar = eval_data.get("similar_pitches", [])
        for s in similar:
            s_card = QFrame()
            s_card.setStyleSheet(f"QFrame {{ background-color: {THEME_COLORS['bg_card']}; border: 1px solid {THEME_COLORS['border']}; border-radius: 8px; padding: 10px; }}")
            s_layout = QVBoxLayout(s_card)
            s_layout.setSpacing(4)
            lbl_s_title = QLabel(f"<b>{s.get('pitch_name')}</b>  |  Industry: {s.get('industry')}  |  <font color='{THEME_COLORS['accent_primary']}'>Similarity: {s.get('similarity_percentage')}%</font>")
            lbl_s_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 12px;")
            lbl_s_sol = QLabel(f"Solution: {s.get('solution_summary')}")
            lbl_s_sol.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px;")
            s_layout.addWidget(lbl_s_title)
            s_layout.addWidget(lbl_s_sol)
            self.bench_container.addWidget(s_card)

        # Set Disclaimer Text
        disc = eval_data.get("disclaimer", "")
        demo = eval_data.get("demo_notice", "")
        self.lbl_disclaimer.setText(f"<b>Disclaimer:</b> {disc}<br/><b>Dataset Note:</b> {demo}")

    def on_export_pdf(self):
        if not self.current_eval:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export PDF Report", f"{self.current_eval.get('pitch_name', 'pitch')}_Report.pdf", "PDF Files (*.pdf)")
        if path:
            try:
                out_path = PDFReportGenerator.generate_pdf(self.current_eval, Path(path))
                QMessageBox.information(self, "PDF Export Complete", f"PDF report successfully saved to:\n{out_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export PDF:\n{str(e)}")

    def on_export_json(self):
        if not self.current_eval:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export JSON Data", f"{self.current_eval.get('pitch_name', 'pitch')}_Evaluation.json", "JSON Files (*.json)")
        if path:
            try:
                out_path = PDFReportGenerator.export_json(self.current_eval, Path(path))
                QMessageBox.information(self, "JSON Export Complete", f"JSON data successfully saved to:\n{out_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export JSON:\n{str(e)}")

    def on_export_csv(self):
        if not self.current_eval:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export CSV Summary", f"{self.current_eval.get('pitch_name', 'pitch')}_Evaluation.csv", "CSV Files (*.csv)")
        if path:
            try:
                out_path = PDFReportGenerator.export_csv(self.current_eval, Path(path))
                QMessageBox.information(self, "CSV Export Complete", f"CSV summary successfully saved to:\n{out_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export CSV:\n{str(e)}")

    def on_save_history(self):
        if not self.current_eval:
            return
        try:
            eval_id = self.db.save_evaluation(self.current_eval)
            QMessageBox.information(self, "Saved to Database", f"Evaluation for '{self.current_eval.get('pitch_name')}' saved to SQLite database (ID: {eval_id}).")
        except Exception as e:
            QMessageBox.critical(self, "Save Failed", f"Failed to save to database:\n{str(e)}")

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _btn_style(self, bg_color: str, fg_color: str) -> str:
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {fg_color};
                font-size: 12px;
                font-weight: bold;
                padding: 6px 14px;
                border-radius: 6px;
                border: 1px solid {THEME_COLORS['border']};
            }}
            QPushButton:hover {{
                opacity: 0.85;
            }}
        """

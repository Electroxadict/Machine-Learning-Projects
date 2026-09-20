"""
Analytics View for PitchLens AI
Provides aggregate score metrics and Matplotlib visualizations.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame
import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from config.settings import THEME_COLORS, CATEGORY_DISPLAY_NAMES
from database.database import get_db
from ui.widgets.metric_card import MetricCard


class AnalyticsView(QWidget):
    """Analytics view featuring aggregate charts and performance metrics."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = get_db()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header Title
        lbl_title = QLabel("Analytics & Aggregate Insights")
        lbl_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 24px; font-weight: bold;")
        layout.addWidget(lbl_title)

        # Metric Cards Row
        summary = self.db.get_analytics_summary()

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        card_total = MetricCard("Total Evaluations", str(summary.get("total_evaluations", 0)), "Recorded in database", THEME_COLORS["accent_primary"])
        card_avg = MetricCard("Aggregate Avg Score", f"{summary.get('avg_score', 0.0):.1f}", "Out of 100", THEME_COLORS["success"])
        card_weak = MetricCard("Top Weakness Area", summary.get("most_common_weakness", "None").replace("_", " ").title(), "Lowest scoring category", THEME_COLORS["warning"])

        cards_row.addWidget(card_total)
        cards_row.addWidget(card_avg)
        cards_row.addWidget(card_weak)
        layout.addLayout(cards_row)

        # Chart Grid: 2x2 layout
        grid_row1 = QHBoxLayout()
        grid_row1.setSpacing(20)

        # Chart 1: Category Averages Bar Chart
        fig1 = Figure(figsize=(5, 3.5), facecolor=THEME_COLORS["bg_card"])
        canvas1 = FigureCanvas(fig1)
        ax1 = fig1.add_subplot(111, facecolor=THEME_COLORS["bg_card"])

        cat_avgs = summary.get("category_averages", {})
        if cat_avgs:
            keys = [CATEGORY_DISPLAY_NAMES.get(k, k)[:10] for k in cat_avgs.keys()]
            vals = list(cat_avgs.values())
            ax1.barh(keys, vals, color=THEME_COLORS["accent_primary"])
            ax1.set_xlim(0, 100)
            ax1.set_title("Average Category Performance", color=THEME_COLORS["text_main"], fontsize=10, fontweight="bold")
            ax1.tick_params(colors=THEME_COLORS["text_muted"], labelsize=8)
            ax1.spines["bottom"].set_color(THEME_COLORS["border"])
            ax1.spines["left"].set_color(THEME_COLORS["border"])
            ax1.spines["top"].set_visible(False)
            ax1.spines["right"].set_visible(False)

        fig1.tight_layout()
        canvas1.draw()
        grid_row1.addWidget(canvas1)

        # Chart 2: Readiness Distribution Pie/Bar
        fig2 = Figure(figsize=(5, 3.5), facecolor=THEME_COLORS["bg_card"])
        canvas2 = FigureCanvas(fig2)
        ax2 = fig2.add_subplot(111, facecolor=THEME_COLORS["bg_card"])

        read_dist = summary.get("readiness_distribution", {})
        if read_dist:
            labels = list(read_dist.keys())
            counts = list(read_dist.values())
            ax2.pie(counts, labels=labels, autopct="%1.0f%%", textprops={"color": THEME_COLORS["text_main"], "fontsize": 8})
            ax2.set_title("Readiness Tier Distribution", color=THEME_COLORS["text_main"], fontsize=10, fontweight="bold")

        fig2.tight_layout()
        canvas2.draw()
        grid_row1.addWidget(canvas2)

        layout.addLayout(grid_row1)

        # Chart Grid Row 2: Missing Elements Frequency & Historical Trend
        grid_row2 = QHBoxLayout()
        grid_row2.setSpacing(20)

        # Chart 3: Missing Elements Frequency
        fig3 = Figure(figsize=(5, 3.5), facecolor=THEME_COLORS["bg_card"])
        canvas3 = FigureCanvas(fig3)
        ax3 = fig3.add_subplot(111, facecolor=THEME_COLORS["bg_card"])

        missing_freq = summary.get("missing_frequency", {})
        if missing_freq:
            m_keys = [CATEGORY_DISPLAY_NAMES.get(k, k)[:12] for k in missing_freq.keys()]
            m_vals = list(missing_freq.values())
            ax3.bar(m_keys, m_vals, color=THEME_COLORS["danger"])
            ax3.set_title("Missing Section Frequency", color=THEME_COLORS["text_main"], fontsize=10, fontweight="bold")
            ax3.tick_params(colors=THEME_COLORS["text_muted"], labelsize=8)
            ax3.spines["bottom"].set_color(THEME_COLORS["border"])
            ax3.spines["left"].set_color(THEME_COLORS["border"])
            ax3.spines["top"].set_visible(False)
            ax3.spines["right"].set_visible(False)

        fig3.tight_layout()
        canvas3.draw()
        grid_row2.addWidget(canvas3)

        # Chart 4: Historical Evaluation Trend Line
        fig4 = Figure(figsize=(5, 3.5), facecolor=THEME_COLORS["bg_card"])
        canvas4 = FigureCanvas(fig4)
        ax4 = fig4.add_subplot(111, facecolor=THEME_COLORS["bg_card"])

        evals = self.db.get_all_evaluations()
        if evals:
            evals_sorted = sorted(evals, key=lambda x: x["id"])
            ids = [e["id"] for e in evals_sorted]
            scores = [e["overall_score"] for e in evals_sorted]
            ax4.plot(ids, scores, marker="o", color=THEME_COLORS["success"], linewidth=2)
            ax4.set_ylim(0, 100)
            ax4.set_title("Historical Score Sequence Trend", color=THEME_COLORS["text_main"], fontsize=10, fontweight="bold")
            ax4.tick_params(colors=THEME_COLORS["text_muted"], labelsize=8)
            ax4.spines["bottom"].set_color(THEME_COLORS["border"])
            ax4.spines["left"].set_color(THEME_COLORS["border"])
            ax4.spines["top"].set_visible(False)
            ax4.spines["right"].set_visible(False)

        fig4.tight_layout()
        canvas4.draw()
        grid_row2.addWidget(canvas4)

        layout.addLayout(grid_row2)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

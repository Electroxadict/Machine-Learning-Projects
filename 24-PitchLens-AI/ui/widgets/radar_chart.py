"""
Radar Chart Widget for PitchLens AI
Embeds a Matplotlib Radar Chart in PySide6 for visualizing 10 category scores.
"""
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout
import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from config.settings import THEME_COLORS, CATEGORY_DISPLAY_NAMES


class RadarChartWidget(QWidget):
    """Matplotlib Radar Chart widget formatted for dark theme UI."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(4.5, 4.5), facecolor=THEME_COLORS["bg_card"])
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        
        self.plot_radar({})

    def plot_radar(self, category_scores: dict):
        """Render 10-axis radar plot with category scores."""
        self.figure.clear()

        if not category_scores:
            labels = list(CATEGORY_DISPLAY_NAMES.values())
            scores = [0] * len(labels)
        else:
            labels = [CATEGORY_DISPLAY_NAMES.get(k, k.replace("_", " ").title()) for k in category_scores.keys()]
            scores = list(category_scores.values())

        num_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        # Complete the loop
        scores_loop = scores + [scores[0]]
        angles_loop = angles + [angles[0]]

        ax = self.figure.add_subplot(111, polar=True, facecolor=THEME_COLORS["bg_card"])

        # Draw axis lines and labels
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)

        ax.set_xticks(angles)
        ax.set_xticklabels(labels, color=THEME_COLORS["text_muted"], fontsize=8)

        # Y-ticks
        ax.set_rlabel_position(0)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(["20", "40", "60", "80", "100"], color=THEME_COLORS["text_muted"], fontsize=7)
        ax.set_ylim(0, 100)

        # Customize gridlines
        ax.grid(color=THEME_COLORS["border"], linestyle="--", linewidth=0.8)
        ax.spines["polar"].set_color(THEME_COLORS["border"])

        # Plot Data Polygon
        ax.plot(angles_loop, scores_loop, color=THEME_COLORS["accent_primary"], linewidth=2, linestyle="solid")
        ax.fill(angles_loop, scores_loop, color=THEME_COLORS["accent_primary"], alpha=0.25)

        self.figure.tight_layout()
        self.canvas.draw()

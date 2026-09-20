"""
Settings View for PitchLens AI
Allows modifying category weights, themes, and restoring defaults.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider,
    QFormLayout, QMessageBox, QGroupBox, QScrollArea
)
from PySide6.QtCore import Qt, Signal

from config.settings import DEFAULT_CATEGORY_WEIGHTS, CATEGORY_DISPLAY_NAMES, THEME_COLORS


class SettingsView(QWidget):
    """View for adjusting evaluation category weights and system preferences."""

    weights_updated_signal = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sliders = {}
        self.labels = {}
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
        lbl_title = QLabel("Settings & Weight Customization")
        lbl_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 24px; font-weight: bold;")
        lbl_sub = QLabel("Customize evaluation category weights. Total weight sum must equal 100%.")
        lbl_sub.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 13px;")
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_sub)

        # Total Weight Sum Status Indicator
        self.lbl_sum = QLabel("Total Weight: 100%")
        self.lbl_sum.setStyleSheet(f"color: {THEME_COLORS['success']}; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.lbl_sum)

        # Weights Group Box
        group_box = QGroupBox("Evaluation Category Weights")
        group_box.setStyleSheet(f"""
            QGroupBox {{
                background-color: {THEME_COLORS['bg_card']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 8px;
                color: {THEME_COLORS['text_main']};
                font-weight: bold;
                padding-top: 16px;
            }}
        """)
        form_layout = QFormLayout(group_box)
        form_layout.setContentsMargins(16, 20, 16, 16)
        form_layout.setSpacing(12)

        for cat_key, default_w in DEFAULT_CATEGORY_WEIGHTS.items():
            display_name = CATEGORY_DISPLAY_NAMES.get(cat_key, cat_key)
            lbl_cat = QLabel(display_name + ":")
            lbl_cat.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-weight: bold;")

            row_layout = QHBoxLayout()
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, 50)
            slider.setValue(int(default_w * 100))
            slider.setStyleSheet(f"""
                QSlider::groove:horizontal {{
                    height: 6px;
                    background: {THEME_COLORS['bg_dark']};
                    border-radius: 3px;
                }}
                QSlider::handle:horizontal {{
                    background: {THEME_COLORS['accent_primary']};
                    width: 14px;
                    margin-top: -4px;
                    margin-bottom: -4px;
                    border-radius: 7px;
                }}
            """)

            lbl_val = QLabel(f"{int(default_w * 100)}%")
            lbl_val.setFixedWidth(40)
            lbl_val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            lbl_val.setStyleSheet(f"color: {THEME_COLORS['accent_primary']}; font-weight: bold;")

            slider.valueChanged.connect(lambda val, k=cat_key: self.on_slider_changed(k, val))

            row_layout.addWidget(slider, 1)
            row_layout.addWidget(lbl_val)

            form_layout.addRow(lbl_cat, row_layout)
            self.sliders[cat_key] = slider
            self.labels[cat_key] = lbl_val

        layout.addWidget(group_box)

        # Action Buttons Row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        btn_save = QPushButton("Save Weights")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.setStyleSheet(f"background-color: {THEME_COLORS['accent_primary']}; color: #11111B; font-weight: bold; padding: 10px 20px; border-radius: 6px;")
        btn_save.clicked.connect(self.on_save_clicked)

        btn_reset = QPushButton("Restore Default Weights")
        btn_reset.setCursor(Qt.PointingHandCursor)
        btn_reset.setStyleSheet(f"background-color: {THEME_COLORS['bg_card']}; color: {THEME_COLORS['text_main']}; border: 1px solid {THEME_COLORS['border']}; font-weight: bold; padding: 10px 20px; border-radius: 6px;")
        btn_reset.clicked.connect(self.on_reset_clicked)

        btn_row.addWidget(btn_save)
        btn_row.addWidget(btn_reset)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

    def on_slider_changed(self, cat_key: str, value: int):
        self.labels[cat_key].setText(f"{value}%")
        total_sum = sum(s.value() for s in self.sliders.values())
        if total_sum == 100:
            self.lbl_sum.setText("Total Weight: 100%  (Valid)")
            self.lbl_sum.setStyleSheet(f"color: {THEME_COLORS['success']}; font-size: 16px; font-weight: bold;")
        else:
            self.lbl_sum.setText(f"Total Weight: {total_sum}%  (Must equal 100%)")
            self.lbl_sum.setStyleSheet(f"color: {THEME_COLORS['danger']}; font-size: 16px; font-weight: bold;")

    def on_save_clicked(self):
        total_sum = sum(s.value() for s in self.sliders.values())
        if total_sum != 100:
            QMessageBox.warning(self, "Invalid Weight Sum", f"The sum of category weights is currently {total_sum}%. It must equal exactly 100%.")
            return

        new_weights = {k: s.value() / 100.0 for k, s in self.sliders.items()}
        self.weights_updated_signal.emit(new_weights)
        QMessageBox.information(self, "Settings Saved", "Successfully updated evaluation category weights.")

    def on_reset_clicked(self):
        for k, default_w in DEFAULT_CATEGORY_WEIGHTS.items():
            val = int(default_w * 100)
            self.sliders[k].setValue(val)
            self.labels[k].setText(f"{val}%")
        self.lbl_sum.setText("Total Weight: 100%  (Valid)")
        self.lbl_sum.setStyleSheet(f"color: {THEME_COLORS['success']}; font-size: 16px; font-weight: bold;")
        self.weights_updated_signal.emit(DEFAULT_CATEGORY_WEIGHTS.copy())

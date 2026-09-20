"""
Pitch Input View for PitchLens AI
Supports text pasting, file import (TXT, PDF, DOCX), preset sample selection,
optional structured breakdown fields, and input validation.
"""
from pathlib import Path
import pandas as pd
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit,
    QPushButton, QTabWidget, QFileDialog, QMessageBox, QComboBox,
    QGroupBox, QFormLayout, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal

from config.settings import THEME_COLORS, SAMPLE_PITCHES_PATH
from core.text_processor import TextProcessor
from core.evaluator import PitchEvaluator


class PitchInputView(QWidget):
    """View for uploading or entering pitch text and initiating evaluation."""

    analysis_completed_signal = Signal(dict)

    def __init__(self, evaluator: PitchEvaluator, parent=None):
        super().__init__(parent)
        self.evaluator = evaluator
        self.init_ui()
        self.load_sample_pitches()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header Title
        hdr_layout = QVBoxLayout()
        hdr_layout.setSpacing(4)
        lbl_title = QLabel("Evaluate Pitch")
        lbl_title.setStyleSheet(f"color: {THEME_COLORS['text_main']}; font-size: 24px; font-weight: bold;")
        lbl_sub = QLabel("Paste pitch content or upload document (TXT, PDF, DOCX) for automated evaluation.")
        lbl_sub.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 13px;")
        hdr_layout.addWidget(lbl_title)
        hdr_layout.addWidget(lbl_sub)
        main_layout.addLayout(hdr_layout)

        # Quick Load Sample Pitch Dropdown Row
        sample_row = QHBoxLayout()
        sample_row.setSpacing(10)
        lbl_sample = QLabel("Quick Load Demo Sample:")
        lbl_sample.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-weight: bold;")
        self.combo_sample = QComboBox()
        self.combo_sample.setStyleSheet(f"""
            QComboBox {{
                background-color: {THEME_COLORS['bg_card']};
                color: {THEME_COLORS['text_main']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 6px;
                padding: 6px 12px;
            }}
        """)
        self.combo_sample.currentIndexChanged.connect(self.on_sample_selected)
        sample_row.addWidget(lbl_sample)
        sample_row.addWidget(self.combo_sample, 1)
        main_layout.addLayout(sample_row)

        # Pitch Title Field
        title_row = QHBoxLayout()
        lbl_p_title = QLabel("Pitch Title:")
        lbl_p_title.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-weight: bold;")
        self.txt_pitch_name = QLineEdit()
        self.txt_pitch_name.setPlaceholderText("e.g., CloudPulse Analytics")
        self.txt_pitch_name.setStyleSheet(f"""
            QLineEdit {{
                background-color: {THEME_COLORS['bg_card']};
                color: {THEME_COLORS['text_main']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
        """)
        title_row.addWidget(lbl_p_title)
        title_row.addWidget(self.txt_pitch_name, 1)
        main_layout.addLayout(title_row)

        # Tabs for Input Method: Paste Text vs Upload File vs Structured Fields
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {THEME_COLORS['border']};
                background-color: {THEME_COLORS['bg_card']};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {THEME_COLORS['bg_dark']};
                color: {THEME_COLORS['text_muted']};
                padding: 10px 20px;
                font-weight: bold;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            QTabBar::tab:selected {{
                background-color: {THEME_COLORS['bg_card']};
                color: {THEME_COLORS['accent_primary']};
                border-bottom: 2px solid {THEME_COLORS['accent_primary']};
            }}
        """)

        # Tab 1: Direct Text Paste
        tab_paste = QWidget()
        layout_paste = QVBoxLayout(tab_paste)
        layout_paste.setContentsMargins(16, 16, 16, 16)

        self.txt_pitch_body = QTextEdit()
        self.txt_pitch_body.setPlaceholderText("Paste pitch narrative or transcript text here...")
        self.txt_pitch_body.setStyleSheet(f"""
            QTextEdit {{
                background-color: {THEME_COLORS['bg_dark']};
                color: {THEME_COLORS['text_main']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 6px;
                font-size: 13px;
                padding: 10px;
            }}
        """)
        self.txt_pitch_body.textChanged.connect(self.update_char_count)
        layout_paste.addWidget(self.txt_pitch_body)

        self.lbl_stats = QLabel("Words: 0 | Characters: 0")
        self.lbl_stats.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 11px;")
        layout_paste.addWidget(self.lbl_stats)

        self.tabs.addTab(tab_paste, "Method 1: Paste Text")

        # Tab 2: Upload File (TXT, PDF, DOCX)
        tab_upload = QWidget()
        layout_upload = QVBoxLayout(tab_upload)
        layout_upload.setContentsMargins(24, 24, 24, 24)
        layout_upload.setSpacing(16)

        lbl_up_desc = QLabel("Select a document file from your computer (.txt, .pdf, .docx):")
        lbl_up_desc.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-size: 13px;")
        layout_upload.addWidget(lbl_up_desc)

        up_btn_row = QHBoxLayout()
        self.txt_file_path = QLineEdit()
        self.txt_file_path.setReadOnly(True)
        self.txt_file_path.setPlaceholderText("No file selected...")
        self.txt_file_path.setStyleSheet(f"""
            QLineEdit {{
                background-color: {THEME_COLORS['bg_dark']};
                color: {THEME_COLORS['text_main']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 6px;
                padding: 8px 12px;
            }}
        """)

        btn_browse = QPushButton("Browse File...")
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['bg_hover']};
                color: {THEME_COLORS['text_main']};
                border: 1px solid {THEME_COLORS['border']};
                border-radius: 6px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {THEME_COLORS['accent_primary']};
                color: #11111B;
            }}
        """)
        btn_browse.clicked.connect(self.on_browse_file)

        up_btn_row.addWidget(self.txt_file_path, 1)
        up_btn_row.addWidget(btn_browse)
        layout_upload.addLayout(up_btn_row)

        self.lbl_file_preview = QLabel("")
        self.lbl_file_preview.setWordWrap(True)
        self.lbl_file_preview.setStyleSheet(f"color: {THEME_COLORS['success']}; font-size: 12px;")
        layout_upload.addWidget(self.lbl_file_preview)
        layout_upload.addStretch()

        self.tabs.addTab(tab_upload, "Method 2: Upload File")

        # Tab 3: Structured Fields (Optional Detailed Breakdown)
        tab_struct = QWidget()
        layout_struct_wrap = QVBoxLayout(tab_struct)

        scroll_struct = QScrollArea()
        scroll_struct.setWidgetResizable(True)
        scroll_struct.setStyleSheet("QScrollArea { border: none; }")

        struct_content = QWidget()
        form_layout = QFormLayout(struct_content)
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_layout.setSpacing(10)

        self.struct_fields = {}
        field_list = [
            ("problem", "Problem Statement"),
            ("solution", "Solution & Product"),
            ("market", "Target Market"),
            ("business_model", "Business / Monetization Model"),
            ("competition", "Competitive Advantage"),
            ("traction", "Traction & Metrics"),
            ("team", "Team & Credentials"),
            ("financial", "Financial Model & Projections"),
            ("roadmap", "Roadmap & Scalability"),
        ]

        for f_key, f_label in field_list:
            lbl = QLabel(f_label + ":")
            lbl.setStyleSheet(f"color: {THEME_COLORS['text_muted']}; font-weight: bold;")
            txt = QTextEdit()
            txt.setMaximumHeight(60)
            txt.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {THEME_COLORS['bg_dark']};
                    color: {THEME_COLORS['text_main']};
                    border: 1px solid {THEME_COLORS['border']};
                    border-radius: 4px;
                }}
            """)
            form_layout.addRow(lbl, txt)
            self.struct_fields[f_key] = txt

        scroll_struct.setWidget(struct_content)
        layout_struct_wrap.addWidget(scroll_struct)

        self.tabs.addTab(tab_struct, "Structured Fields (Optional)")

        main_layout.addWidget(self.tabs, 1)

        # Primary Action Button: ANALYZE PITCH
        self.btn_analyze = QPushButton("ANALYZE PITCH")
        self.btn_analyze.setCursor(Qt.PointingHandCursor)
        self.btn_analyze.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME_COLORS['accent_primary']};
                color: #11111B;
                font-size: 16px;
                font-weight: bold;
                padding: 14px 28px;
                border-radius: 8px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {THEME_COLORS['accent_secondary']};
            }}
        """)
        self.btn_analyze.clicked.connect(self.on_analyze_clicked)
        main_layout.addWidget(self.btn_analyze)

    def load_sample_pitches(self):
        """Populate sample pitches dropdown."""
        self.combo_sample.addItem("-- Select Demo Sample Pitch --", None)
        if SAMPLE_PITCHES_PATH.exists():
            try:
                df_samples = pd.read_csv(SAMPLE_PITCHES_PATH)
                for idx, row in df_samples.iterrows():
                    self.combo_sample.addItem(row["title"], dict(row))
            except Exception as e:
                print(f"Error loading sample pitches: {e}")

    def on_sample_selected(self, index: int):
        data = self.combo_sample.currentData()
        if data and isinstance(data, dict):
            self.txt_pitch_name.setText(data.get("title", "").split("(")[0].strip())
            self.txt_pitch_body.setText(data.get("pitch_text", ""))
            self.tabs.setCurrentIndex(0)

    def update_char_count(self):
        text = self.txt_pitch_body.toPlainText()
        words = len(text.split())
        chars = len(text)
        self.lbl_stats.setText(f"Words: {words} | Characters: {chars}")

    def on_browse_file(self):
        file_filter = "Supported Files (*.txt *.pdf *.docx *.doc);;Text Files (*.txt);;PDF Files (*.pdf);;Word Files (*.docx)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Pitch File", "", file_filter)
        if file_path:
            self.txt_file_path.setText(file_path)
            try:
                extracted_text = TextProcessor.extract_text_from_file(file_path)
                self.txt_pitch_body.setText(extracted_text)
                filename = Path(file_path).name
                self.txt_pitch_name.setText(Path(file_path).stem)
                self.lbl_file_preview.setText(f"✓ Successfully extracted text from '{filename}' ({len(extracted_text.split())} words)")
                self.tabs.setCurrentIndex(0)  # Switch to paste tab to show text
            except Exception as e:
                QMessageBox.critical(self, "File Extraction Error", f"Could not extract text from file:\n{str(e)}")

    def on_analyze_clicked(self):
        pitch_name = self.txt_pitch_name.text().strip() or "Untitled Pitch"
        pitch_text = self.txt_pitch_body.toPlainText().strip()

        # Collect structured fields if available
        structured_data = {}
        for k, widget in self.struct_fields.items():
            val = widget.toPlainText().strip()
            if val:
                structured_data[k] = val

        try:
            # Execute evaluation
            eval_result = self.evaluator.evaluate(
                pitch_text=pitch_text,
                pitch_name=pitch_name,
                structured_fields=structured_data
            )
            # Emit signal to show results page
            self.analysis_completed_signal.emit(eval_result)
        except ValueError as ve:
            QMessageBox.warning(self, "Input Validation Error", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Evaluation Error", f"An unexpected error occurred during evaluation:\n{str(e)}")

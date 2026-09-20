"""
PDF Report Generator Module for PitchLens AI
Uses ReportLab to create visual, presentation-ready PDF evaluation reports.
"""
import logging
import json
import csv
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from config.settings import REPORTS_DIR, DISCLAIMER_TEXT, DEMO_NOTICE_TEXT, APP_TITLE, APP_TAGLINE

logger = logging.getLogger("PitchLens.PDFReport")


class PDFReportGenerator:
    """Generates styled PDF, JSON, and CSV export files for pitch evaluations."""

    @classmethod
    def generate_pdf(cls, eval_result: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
        """
        Generate a multi-page professional PDF report using ReportLab.
        Returns the absolute Path of the generated PDF.
        """
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        if output_path is None:
            safe_name = "".join(c if c.isalnum() else "_" for c in eval_result.get("pitch_name", "pitch"))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = REPORTS_DIR / f"{safe_name}_Evaluation_{timestamp}.pdf"

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()

        # Custom Palette & Typography
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            textColor=colors.HexColor("#1E1E2E"),
            leading=26,
        )

        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=11,
            textColor=colors.HexColor("#585B70"),
            leading=14,
        )

        h2_style = ParagraphStyle(
            "SectionH2",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=colors.HexColor("#181825"),
            spaceBefore=12,
            spaceAfter=6,
        )

        body_style = ParagraphStyle(
            "BodyTextCustom",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            textColor=colors.HexColor("#313244"),
            leading=13,
        )

        disclaimer_style = ParagraphStyle(
            "DisclaimerCustom",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            textColor=colors.HexColor("#6C6D7D"),
            leading=11,
        )

        story = []

        # 1. Header Banner
        header_data = [
            [
                Paragraph(f"<b>{APP_TITLE}</b>", title_style),
                Paragraph(f"Date: <b>{eval_result.get('date', '')}</b>", body_style)
            ],
            [
                Paragraph(f"{APP_TAGLINE}", subtitle_style),
                Paragraph(f"Pitch: <b>{eval_result.get('pitch_name', 'Untitled')}</b>", body_style)
            ]
        ]
        header_table = Table(header_data, colWidths=[3.5 * inch, 3.5 * inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#89B4FA"), spaceAfter=12))

        # 2. Executive Summary Score Card
        score_val = eval_result.get("overall_score", 0.0)
        readiness_val = eval_result.get("readiness", "Developing")
        coverage_val = eval_result.get("evidence_coverage", 0.0)

        summary_data = [
            [
                Paragraph("<b>OVERALL PITCH SCORE</b>", body_style),
                Paragraph("<b>READINESS CLASSIFICATION</b>", body_style),
                Paragraph("<b>EVIDENCE COVERAGE</b>", body_style)
            ],
            [
                Paragraph(f"<font size=20 color='#1E1E2E'><b>{score_val:.1f} / 100</b></font>", body_style),
                Paragraph(f"<font size=12 color='#2E7D32'><b>{readiness_val}</b></font>", body_style),
                Paragraph(f"<font size=12 color='#1565C0'><b>{coverage_val:.1f}%</b></font>", body_style)
            ]
        ]
        summary_table = Table(summary_data, colWidths=[2.3 * inch, 2.7 * inch, 2.0 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F5F5FA")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 14))

        # 3. Category Scores Table
        story.append(Paragraph("Category Scores Breakdown", h2_style))
        cat_scores = eval_result.get("category_scores", {})
        cat_statuses = eval_result.get("category_statuses", {})
        cat_explanations = eval_result.get("category_explanations", {})

        cat_rows = [["Category", "Score", "Status", "Explanation"]]
        for cat_key, s_val in cat_scores.items():
            c_name = cat_key.replace("_", " ").title()
            c_status = cat_statuses.get(cat_key, "PRESENT")
            c_exp = cat_explanations.get(cat_key, "")
            cat_rows.append([
                Paragraph(f"<b>{c_name}</b>", body_style),
                Paragraph(f"{s_val:.1f}", body_style),
                Paragraph(c_status, body_style),
                Paragraph(c_exp, body_style)
            ])

        cat_table = Table(cat_rows, colWidths=[1.8 * inch, 0.7 * inch, 1.2 * inch, 3.3 * inch])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E1E2E")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(cat_table)
        story.append(Spacer(1, 14))

        # 4. Strengths & Weaknesses
        story.append(Paragraph("Key Strengths & Weaknesses", h2_style))
        strengths = eval_result.get("strengths", [])
        weaknesses = eval_result.get("weaknesses", [])

        str_text = "<br/>".join([f"• {s}" for s in strengths]) if strengths else "• None noted."
        wk_text = "<br/>".join([f"• {w}" for w in weaknesses]) if weaknesses else "• None noted."

        sw_data = [
            [Paragraph("<b>STRENGTHS</b>", body_style), Paragraph("<b>WEAKNESSES</b>", body_style)],
            [Paragraph(str_text, body_style), Paragraph(wk_text, body_style)]
        ]
        sw_table = Table(sw_data, colWidths=[3.5 * inch, 3.5 * inch])
        sw_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#E8F5E9")),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#FFEBEE")),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(sw_table)
        story.append(Spacer(1, 14))

        # 5. Priority Recommendations
        story.append(Paragraph("Actionable Recommendations", h2_style))
        recs = eval_result.get("recommendations", [])
        for rec in recs[:4]:
            p_color = "#D32F2F" if rec.get("priority") == "HIGH" else "#F57C00"
            rec_content = [
                Paragraph(f"<font color='{p_color}'><b>[{rec.get('priority')}] {rec.get('title')}</b></font>", body_style),
                Paragraph(f"<b>Issue:</b> {rec.get('problem')}", body_style),
                Paragraph(f"<b>Action to Add:</b> {rec.get('what_to_add')}", body_style),
                Spacer(1, 4)
            ]
            story.append(KeepTogether(rec_content))

        # 6. Benchmark Similar Pitches
        similar = eval_result.get("similar_pitches", [])
        if similar:
            story.append(Spacer(1, 8))
            story.append(Paragraph("Benchmark Dataset Similarity", h2_style))
            sim_rows = [["Pitch Name", "Industry", "Similarity %", "Key Highlights"]]
            for s in similar:
                sim_rows.append([
                    Paragraph(f"<b>{s.get('pitch_name')}</b>", body_style),
                    Paragraph(s.get("industry", ""), body_style),
                    Paragraph(f"<b>{s.get('similarity_percentage')}%</b>", body_style),
                    Paragraph(s.get("solution_summary", ""), body_style)
                ])
            sim_table = Table(sim_rows, colWidths=[1.8 * inch, 1.2 * inch, 1.0 * inch, 3.0 * inch])
            sim_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#263238")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(sim_table)

        # 7. Disclaimers Footer
        story.append(Spacer(1, 16))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=6))
        story.append(Paragraph(f"<b>Disclaimer:</b> {DISCLAIMER_TEXT}", disclaimer_style))
        story.append(Paragraph(f"<b>Data Note:</b> {DEMO_NOTICE_TEXT}", disclaimer_style))

        # Build document
        doc.build(story)
        logger.info(f"Generated PDF evaluation report at {output_path}")
        return output_path

    @classmethod
    def export_json(cls, eval_result: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
        """Export evaluation data as formatted JSON file."""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        if output_path is None:
            safe_name = "".join(c if c.isalnum() else "_" for c in eval_result.get("pitch_name", "pitch"))
            output_path = REPORTS_DIR / f"{safe_name}_Evaluation.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(eval_result, f, indent=2)

        return output_path

    @classmethod
    def export_csv(cls, eval_result: Dict[str, Any], output_path: Optional[Path] = None) -> Path:
        """Export evaluation score summary as CSV file."""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        if output_path is None:
            safe_name = "".join(c if c.isalnum() else "_" for c in eval_result.get("pitch_name", "pitch"))
            output_path = REPORTS_DIR / f"{safe_name}_Evaluation.csv"

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Field", "Value"])
            writer.writerow(["Pitch Name", eval_result.get("pitch_name")])
            writer.writerow(["Date", eval_result.get("date")])
            writer.writerow(["Overall Score", eval_result.get("overall_score")])
            writer.writerow(["Readiness", eval_result.get("readiness")])
            writer.writerow(["Evidence Coverage %", eval_result.get("evidence_coverage")])
            writer.writerow([])
            writer.writerow(["Category", "Score (0-100)", "Status"])
            for cat_key, score_val in eval_result.get("category_scores", {}).items():
                status_val = eval_result.get("category_statuses", {}).get(cat_key, "")
                writer.writerow([cat_key.replace("_", " ").title(), score_val, status_val])

        return output_path

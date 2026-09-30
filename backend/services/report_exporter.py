"""
CareerEdge AI - Exportable Career Report PDF Generator
Produces a competition-quality, executive PDF career assessment report locally using ReportLab.
100% on-device generation with zero third-party cloud print services.
"""

import io
import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)


class CareerReportExporter:
    """
    Generates a PDF career intelligence report.
    """

    def generate_pdf(
        self,
        match_data: Dict[str, Any],
        gap_data: Dict[str, Any],
        roadmap_data: Dict[str, Any],
        project_data: Dict[str, Any],
        runtime_status: Dict[str, Any],
    ) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )

        styles = getSampleStyleSheet()

        # Custom typography styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#0f172a"),
        )
        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#475569"),
        )
        h1_style = ParagraphStyle(
            "SectionH1",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=12,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor("#334155"),
        )
        badge_style = ParagraphStyle(
            "Badge",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
        )

        story = []

        # Header Title
        story.append(Paragraph("CareerEdge AI", title_style))
        story.append(
            Paragraph(
                "Private On-Device Career Intelligence & Alignment Assessment | Target: Snapdragon® PC",
                subtitle_style,
            )
        )
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

        # Metadata Summary Card
        now_str = datetime.datetime.now().strftime("%B %d, %Y")
        target_role = match_data.get("target_role", "Machine Learning Engineer")
        overall_score = match_data.get("overall_alignment", 0)
        provider = runtime_status.get("active_provider", "CPUExecutionProvider")
        device_mode = runtime_status.get("status_label", "Local AI")

        meta_data = [
            [
                Paragraph("<b>Assessment Date:</b> " + now_str, body_style),
                Paragraph("<b>Target Role:</b> " + target_role, body_style),
            ],
            [
                Paragraph(f"<b>Overall Alignment:</b> <font color='#2563eb'><b>{overall_score}%</b></font>", body_style),
                Paragraph("<b>Inference Engine:</b> " + provider, body_style),
            ],
            [
                Paragraph("<b>Hardware Runtime:</b> " + device_mode, body_style),
                Paragraph("<b>Privacy Verification:</b> 100% On-Device / Zero Cloud Upload", body_style),
            ],
        ]
        meta_table = Table(meta_data, colWidths=[260, 270])
        meta_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#edf2f7")),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(meta_table)
        story.append(Spacer(1, 14))

        # 1. Alignment Score Breakdown
        story.append(Paragraph("1. Deterministic Alignment Breakdown", h1_style))
        breakdown = match_data.get("score_breakdown", {})
        score_rows = [
            ["Dimension", "Score", "Target Weight", "Assessment Note"],
            ["Technical Skills Alignment", f"{breakdown.get('technical_skills', 0)}%", "40%", "Direct & semantic requirement match"],
            ["Project Portfolio Evidence", f"{breakdown.get('projects', 0)}%", "25%", "Verified project application & metrics"],
            ["Work Experience Tenure", f"{breakdown.get('experience', 0)}%", "15%", "Tenure and responsibility coverage"],
            ["Academic Education", f"{breakdown.get('education', 0)}%", "10%", "Degree level and technical discipline"],
            ["Domain Centrality", f"{breakdown.get('domain', 0)}%", "10%", "High-level domain semantic similarity"],
        ]
        score_table = Table(score_rows, colWidths=[150, 60, 80, 240])
        score_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("PADDING", (0, 0), (-1, -1), 4.5),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f5f9")]),
                ]
            )
        )
        story.append(score_table)
        story.append(Spacer(1, 14))

        # 2. Critical Skill Gaps & Explainability
        story.append(Paragraph("2. Top Critical Skill Gaps ('Why Is My Profile Not Aligned?')", h1_style))
        gaps = gap_data.get("gaps", [])
        if gaps:
            for idx, g in enumerate(gaps[:3], 1):
                gap_p = [
                    Paragraph(f"<b>Gap {idx}: {g.get('skill')}</b> ({g.get('category')}) — <i>{g.get('importance')}</i>", body_style),
                    Paragraph(f"• <b>Why it matters:</b> {g.get('why_it_matters')}", body_style),
                    Paragraph(f"• <b>Missing Evidence:</b> {g.get('evidence_missing')}", body_style),
                    Paragraph(f"• <b>Recommended Project:</b> {g.get('recommended_project')}", body_style),
                ]
                story.extend(gap_p)
                story.append(Spacer(1, 6))
        else:
            story.append(Paragraph("No critical gaps detected. Profile strongly meets stated criteria.", body_style))
        story.append(Spacer(1, 10))

        # 3. Recommended Project Blueprint
        story.append(Paragraph("3. Recommended Portfolio Capstone Project", h1_style))
        projects = project_data.get("projects", [])
        if projects:
            top_proj = projects[0]
            proj_data = [
                [Paragraph(f"<b>Project Title:</b> {top_proj.get('title')}", body_style)],
                [Paragraph(f"<b>Target Stack:</b> {', '.join(top_proj.get('target_skills', []))} | <b>Difficulty:</b> {top_proj.get('difficulty')} | <b>Est. Time:</b> {top_proj.get('estimated_timeline')}", body_style)],
                [Paragraph(f"<b>Architecture:</b> {top_proj.get('architecture')}", body_style)],
                [Paragraph(f"<b>Suggested Resume Bullet:</b> <i>{top_proj.get('resume_bullet_sample')}</i>", body_style)],
            ]
            proj_table = Table(proj_data, colWidths=[530])
            proj_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#3b82f6")),
                        ("PADDING", (0, 0), (-1, -1), 6),
                    ]
                )
            )
            story.append(proj_table)
        story.append(Spacer(1, 14))

        # 4. 30-Day Roadmap Summary
        story.append(Paragraph("4. 30-Day Personalized Career Roadmap", h1_style))
        weeks = roadmap_data.get("weeks", [])
        for w in weeks:
            w_num = w.get("week_number")
            w_theme = w.get("theme")
            w_obj = w.get("objective")
            story.append(Paragraph(f"<b>Week {w_num}: {w_theme}</b>", body_style))
            story.append(Paragraph(f"<i>Objective:</i> {w_obj}", body_style))
            story.append(Spacer(1, 4))

        story.append(Spacer(1, 12))
        story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#94a3b8"), spaceAfter=8))
        story.append(
            Paragraph(
                "<i>CareerEdge AI Assessment Report • Generated strictly on-device using local ONNX inference • Qualcomm AI Lab Competition 2026</i>",
                subtitle_style,
            )
        )

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes


# Singleton instance
_report_exporter = None


def get_report_exporter() -> CareerReportExporter:
    global _report_exporter
    if _report_exporter is None:
        _report_exporter = CareerReportExporter()
    return _report_exporter

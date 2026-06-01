"""
pdf_generator.py - PDF Report Generation for MedAssist AI
Generates professional health reports using ReportLab.
"""

import os
from datetime import datetime
from pathlib import Path


def generate_health_report(profile: dict, diseases: list, medications: list,
                           analyses: list, reports_dir: str) -> dict:
    """
    Generate a comprehensive PDF health report.
    Returns: dict with 'success', 'filename', 'file_path', 'error'
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import HexColor, white, black
        from reportlab.lib.units import cm, mm
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                        Table, TableStyle, HRFlowable, PageBreak)
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

        # Ensure reports directory exists
        os.makedirs(reports_dir, exist_ok=True)

        # Generate filename
        name = profile.get("name", "Patient").replace(" ", "_") if profile else "Patient"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"MedAssist_Report_{name}_{timestamp}.pdf"
        file_path = os.path.join(reports_dir, filename)

        # Colors
        TEAL = HexColor("#0d9488")
        TEAL_LIGHT = HexColor("#e6f7f5")
        DARK = HexColor("#1e293b")
        GRAY = HexColor("#64748b")
        LIGHT_GRAY = HexColor("#f8fafc")
        DANGER = HexColor("#ef4444")
        WARNING = HexColor("#f59e0b")
        SUCCESS = HexColor("#22c55e")

        # Document setup
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=white,
            alignment=TA_CENTER,
            spaceAfter=4,
            fontName='Helvetica-Bold'
        )
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=HexColor("#ccfbf1"),
            alignment=TA_CENTER,
            spaceAfter=2
        )
        section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading1'],
            fontSize=14,
            textColor=TEAL,
            spaceBefore=16,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=10,
            textColor=DARK,
            spaceAfter=4,
            leading=16
        )
        label_style = ParagraphStyle(
            'Label',
            parent=styles['Normal'],
            fontSize=9,
            textColor=GRAY,
            fontName='Helvetica-Bold'
        )

        story = []

        # ── HEADER BANNER ──────────────────────────────────────────────────────
        header_data = [[
            Paragraph("🏥 MedAssist AI", title_style),
        ]]
        header_table = Table(header_data, colWidths=[17*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), TEAL),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('ROUNDEDCORNERS', [8]),
        ]))
        story.append(header_table)

        sub_data = [[Paragraph("AI-Powered Personal Health Report", subtitle_style)]]
        sub_table = Table(sub_data, colWidths=[17*cm])
        sub_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor("#0f766e")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(sub_table)
        story.append(Spacer(1, 0.5*cm))

        # Report date
        date_para = Paragraph(
            f"<font color='#94a3b8'>Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}</font>",
            ParagraphStyle('date', parent=styles['Normal'], fontSize=9, alignment=TA_RIGHT)
        )
        story.append(date_para)
        story.append(Spacer(1, 0.3*cm))

        # ── PATIENT PROFILE ────────────────────────────────────────────────────
        story.append(Paragraph("Patient Profile", section_header_style))
        story.append(HRFlowable(width="100%", thickness=1, color=TEAL_LIGHT))
        story.append(Spacer(1, 0.3*cm))

        if profile:
            profile_data = [
                ["Field", "Value", "Field", "Value"],
                ["Name", profile.get("name", "—"), "Age", str(profile.get("age", "—"))],
                ["Gender", profile.get("gender", "—"), "Blood Group", profile.get("blood_group", "—")],
                ["Weight", f"{profile.get('weight', '—')} kg", "Height", f"{profile.get('height', '—')} cm"],
            ]
        else:
            profile_data = [["Field", "Value"], ["No profile data available", ""]]

        profile_table = Table(profile_data, colWidths=[4*cm, 5*cm, 4*cm, 4*cm])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), TEAL),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        story.append(profile_table)
        story.append(Spacer(1, 0.5*cm))

        # ── DISEASES ───────────────────────────────────────────────────────────
        story.append(Paragraph("Medical Conditions", section_header_style))
        story.append(HRFlowable(width="100%", thickness=1, color=TEAL_LIGHT))
        story.append(Spacer(1, 0.3*cm))

        if diseases:
            disease_data = [["#", "Condition", "Severity", "Notes"]]
            for i, d in enumerate(diseases, 1):
                disease_data.append([
                    str(i),
                    d.get("disease_name", "—"),
                    d.get("severity", "—") or "—",
                    (d.get("notes", "") or "")[:60]
                ])
            disease_table = Table(disease_data, colWidths=[1*cm, 5.5*cm, 3.5*cm, 7*cm])
            disease_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), TEAL),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(disease_table)
        else:
            story.append(Paragraph("No medical conditions recorded.", body_style))
        story.append(Spacer(1, 0.5*cm))

        # ── MEDICATIONS ────────────────────────────────────────────────────────
        story.append(Paragraph("Current Medications", section_header_style))
        story.append(HRFlowable(width="100%", thickness=1, color=TEAL_LIGHT))
        story.append(Spacer(1, 0.3*cm))

        if medications:
            med_data = [["#", "Medicine", "Dosage", "Frequency", "Notes"]]
            for i, m in enumerate(medications, 1):
                med_data.append([
                    str(i),
                    m.get("medicine_name", "—"),
                    m.get("dosage", "—") or "—",
                    m.get("frequency", "—") or "—",
                    (m.get("notes", "") or "")[:40]
                ])
            med_table = Table(med_data, colWidths=[0.8*cm, 4.5*cm, 3*cm, 3.5*cm, 5.2*cm])
            med_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), TEAL),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#e2e8f0")),
                ('PADDING', (0, 0), (-1, -1), 7),
            ]))
            story.append(med_table)
        else:
            story.append(Paragraph("No medications recorded.", body_style))
        story.append(Spacer(1, 0.5*cm))

        # ── ANALYSIS HISTORY ───────────────────────────────────────────────────
        if analyses:
            story.append(Paragraph("Recent Analyses", section_header_style))
            story.append(HRFlowable(width="100%", thickness=1, color=TEAL_LIGHT))
            story.append(Spacer(1, 0.3*cm))

            for analysis in analyses[:5]:  # Show last 5
                atype = analysis.get("analysis_type", "Analysis").replace("_", " ").title()
                created = analysis.get("created_at", "")[:16]
                story.append(Paragraph(f"<b>{atype}</b> — {created}", body_style))

                import json
                try:
                    result = json.loads(analysis.get("result", "{}"))
                    if isinstance(result, dict):
                        summary = result.get("summary", result.get("disclaimer", str(result)[:200]))
                        story.append(Paragraph(summary[:300], ParagraphStyle(
                            'analysis_body', parent=styles['Normal'],
                            fontSize=9, textColor=GRAY, leftIndent=10
                        )))
                except Exception:
                    story.append(Paragraph(str(analysis.get("result", ""))[:200], body_style))
                story.append(Spacer(1, 0.2*cm))

        # ── DISCLAIMER ─────────────────────────────────────────────────────────
        story.append(Spacer(1, 0.5*cm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY))
        story.append(Spacer(1, 0.3*cm))

        disclaimer_data = [[Paragraph(
            "⚠️ <b>Disclaimer:</b> This report is generated by an AI assistant for informational purposes only. "
            "It is NOT a substitute for professional medical advice, diagnosis, or treatment. "
            "Always consult a qualified healthcare provider for medical decisions.",
            ParagraphStyle('disclaimer', parent=styles['Normal'], fontSize=8.5,
                          textColor=GRAY, alignment=TA_CENTER)
        )]]
        disclaimer_table = Table(disclaimer_data, colWidths=[17*cm])
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), HexColor("#fefce8")),
            ('PADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#fde047")),
        ]))
        story.append(disclaimer_table)

        # Build PDF
        doc.build(story)

        return {
            "success": True,
            "filename": filename,
            "file_path": file_path,
            "error": None
        }

    except ImportError:
        return {
            "success": False,
            "filename": None,
            "file_path": None,
            "error": "ReportLab not installed. Run: pip install reportlab"
        }
    except Exception as e:
        return {
            "success": False,
            "filename": None,
            "file_path": None,
            "error": f"PDF generation failed: {str(e)}"
        }
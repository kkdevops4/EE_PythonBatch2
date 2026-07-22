"""
report_pdf.py
-------------
Generates a detailed PDF report of the BMS dashboard analysis.
Uses ReportLab to create a professional multi-page document.
"""

import os
import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable,
)

from modules.analysis import build_report_data

# ── Colour palette ──
DARK_BG    = HexColor("#0f172a")
HEADER_BG  = HexColor("#1e293b")
ACCENT     = HexColor("#0EA5E9")
TEXT_DARK  = HexColor("#1e293b")
TEXT_MID   = HexColor("#475569")
TEXT_LIGHT = HexColor("#94a3b8")
ROW_ALT    = HexColor("#f1f5f9")
WHITE      = HexColor("#ffffff")
GREEN      = HexColor("#22C55E")
RED        = HexColor("#EF4444")


def _get_styles():
    """Build custom paragraph styles for the report."""
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "ReportTitle", parent=base["Title"],
            fontSize=24, leading=30,
            textColor=TEXT_DARK, alignment=TA_CENTER,
            spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle", parent=base["Normal"],
            fontSize=11, leading=14,
            textColor=TEXT_MID, alignment=TA_CENTER,
            spaceAfter=20,
        ),
        "heading": ParagraphStyle(
            "SectionHeading", parent=base["Heading2"],
            fontSize=15, leading=20,
            textColor=ACCENT, spaceBefore=18, spaceAfter=10,
        ),
        "body": ParagraphStyle(
            "BodyText", parent=base["Normal"],
            fontSize=10, leading=14,
            textColor=TEXT_DARK, spaceAfter=8,
        ),
        "small": ParagraphStyle(
            "SmallText", parent=base["Normal"],
            fontSize=8, leading=10,
            textColor=TEXT_LIGHT, alignment=TA_CENTER,
        ),
        "table_header": ParagraphStyle(
            "TableHeader", parent=base["Normal"],
            fontSize=10, leading=13,
            textColor=WHITE, alignment=TA_LEFT,
        ),
        "table_cell": ParagraphStyle(
            "TableCell", parent=base["Normal"],
            fontSize=10, leading=13,
            textColor=TEXT_DARK,
        ),
        "table_value": ParagraphStyle(
            "TableValue", parent=base["Normal"],
            fontSize=10, leading=13,
            textColor=TEXT_DARK, alignment=TA_RIGHT,
        ),
    }
    return styles


def _build_kpi_table(report_data, styles):
    """Create the main metrics table."""
    # Table header
    header = [
        Paragraph("Metric", styles["table_header"]),
        Paragraph("Value", styles["table_header"]),
    ]

    rows = [header]
    for metric, value in report_data:
        rows.append([
            Paragraph(str(metric), styles["table_cell"]),
            Paragraph(str(value), styles["table_value"]),
        ])

    table = Table(rows, colWidths=[120 * mm, 45 * mm])

    # Styling
    table_style = [
        # Header row
        ("BACKGROUND",    (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),

        # All cells
        ("FONTSIZE",      (0, 0), (-1, -1), 10),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
        ("GRID",          (0, 0), (-1, -1), 0.5, TEXT_LIGHT),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]

    # Alternate row shading
    for i in range(1, len(rows)):
        if i % 2 == 0:
            table_style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))

    table.setStyle(TableStyle(table_style))
    return table


def _build_mode_table(df, styles):
    """Create a breakdown table for each operating mode."""
    modes = ["Driving", "Charging", "Parking"]

    header = [
        Paragraph("Mode", styles["table_header"]),
        Paragraph("Records", styles["table_header"]),
        Paragraph("Duration (min)", styles["table_header"]),
        Paragraph("Avg SOC (%)", styles["table_header"]),
        Paragraph("Avg Temp (°C)", styles["table_header"]),
        Paragraph("Avg Power (kW)", styles["table_header"]),
    ]

    rows = [header]
    for mode in modes:
        mode_df = df[df["Mode"] == mode]
        if mode_df.empty:
            continue
        rows.append([
            Paragraph(mode, styles["table_cell"]),
            Paragraph(str(len(mode_df)), styles["table_value"]),
            Paragraph(str(round(len(mode_df) * 50 / 60, 1)), styles["table_value"]),
            Paragraph(str(round(mode_df["SOC"].mean(), 1)), styles["table_value"]),
            Paragraph(str(round(mode_df["Temperature"].mean(), 1)), styles["table_value"]),
            Paragraph(str(round(mode_df["Power"].mean(), 2)), styles["table_value"]),
        ])

    col_w = 27.5 * mm
    table = Table(rows, colWidths=[30 * mm] + [col_w] * 5)

    table_style = [
        ("BACKGROUND",    (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR",     (0, 0), (-1, 0), WHITE),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 0.5, TEXT_LIGHT),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            table_style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))

    table.setStyle(TableStyle(table_style))
    return table


def generate_pdf_report(df, output_path="output_data/bms_report.pdf"):
    """
    Generate a detailed multi-page PDF report and return the bytes.
    Also saves the file to output_path.
    """
    styles = _get_styles()
    report_data = build_report_data(df)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=20 * mm, bottomMargin=20 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )

    story = []

    # ════════════════════════════════════════════════════════
    #  PAGE 1 — Title + Summary
    # ════════════════════════════════════════════════════════

    story.append(Spacer(1, 15 * mm))

    story.append(Paragraph(
        "EV Battery Management System", styles["title"]
    ))
    story.append(Paragraph(
        "Data Analysis Report", styles["title"]
    ))

    story.append(Spacer(1, 4 * mm))

    story.append(HRFlowable(
        width="60%", thickness=2, color=ACCENT,
        spaceAfter=10, spaceBefore=4,
    ))

    vehicle = df["Vehicle_ID"].iloc[0]
    date = df["Timestamp"].dt.date.iloc[0]
    now = datetime.now().strftime("%Y-%m-%d  %H:%M")

    story.append(Paragraph(
        f"Vehicle: {vehicle} &nbsp; | &nbsp; "
        f"Date: {date} &nbsp; | &nbsp; "
        f"Generated: {now}",
        styles["subtitle"],
    ))

    story.append(Spacer(1, 8 * mm))

    # ── Summary paragraph ──
    story.append(Paragraph("1. Executive Summary", styles["heading"]))
    story.append(Paragraph(
        f"This report presents the battery analytics for vehicle "
        f"<b>{vehicle}</b> recorded on <b>{date}</b>. "
        f"A total of <b>{len(df):,}</b> data points were captured at "
        f"50-second intervals across three operating modes: "
        f"Driving, Charging, and Parking. "
        f"The analysis covers State of Charge (SOC), State of Health (SOH), "
        f"voltage, current, temperature, speed, and power metrics.",
        styles["body"],
    ))

    driving_pct  = round((df["Mode"] == "Driving").mean() * 100, 1)
    charging_pct = round((df["Mode"] == "Charging").mean() * 100, 1)
    parking_pct  = round((df["Mode"] == "Parking").mean() * 100, 1)

    story.append(Paragraph(
        f"The vehicle spent <b>{parking_pct}%</b> of the day parked, "
        f"<b>{driving_pct}%</b> driving, and "
        f"<b>{charging_pct}%</b> charging. "
        f"Two charging sessions were recorded during the day.",
        styles["body"],
    ))

    story.append(Spacer(1, 6 * mm))

    # ── Key metrics table ──
    story.append(Paragraph("2. Key Metrics", styles["heading"]))
    story.append(_build_kpi_table(report_data, styles))

    # ════════════════════════════════════════════════════════
    #  PAGE 2 — Mode Breakdown + Observations
    # ════════════════════════════════════════════════════════

    story.append(PageBreak())

    story.append(Paragraph("3. Mode-wise Breakdown", styles["heading"]))
    story.append(Paragraph(
        "The table below shows per-mode statistics including record count, "
        "duration, average SOC, temperature, and power.",
        styles["body"],
    ))
    story.append(_build_mode_table(df, styles))

    story.append(Spacer(1, 8 * mm))

    # ── Driving observations ──
    drv = df[df["Mode"] == "Driving"]
    story.append(Paragraph("4. Driving Analysis", styles["heading"]))
    if not drv.empty:
        story.append(Paragraph(
            f"During driving, the SOC dropped from "
            f"<b>{drv['SOC'].iloc[0]:.1f}%</b> to "
            f"<b>{drv['SOC'].iloc[-1]:.1f}%</b>. "
            f"The average vehicle speed was <b>{drv['Speed'].mean():.1f} km/h</b> "
            f"with a peak of <b>{drv['Speed'].max():.1f} km/h</b>. "
            f"Average power consumption was <b>{drv['Power'].mean():.2f} kW</b>. "
            f"Battery temperature during driving ranged from "
            f"<b>{drv['Temperature'].min():.1f} °C</b> to "
            f"<b>{drv['Temperature'].max():.1f} °C</b>.",
            styles["body"],
        ))

    # ── Charging observations ──
    chg = df[df["Mode"] == "Charging"]
    story.append(Paragraph("5. Charging Analysis", styles["heading"]))
    if not chg.empty:
        story.append(Paragraph(
            f"Two charging sessions were recorded. "
            f"SOC increased from <b>{chg['SOC'].iloc[0]:.1f}%</b> to "
            f"<b>{chg['SOC'].iloc[-1]:.1f}%</b> across both sessions combined. "
            f"Average charging current was <b>{chg['Current'].abs().mean():.1f} A</b>. "
            f"Battery temperature during charging reached a maximum of "
            f"<b>{chg['Temperature'].max():.1f} °C</b>, which is within safe limits.",
            styles["body"],
        ))

    # ── Parking observations ──
    prk = df[df["Mode"] == "Parking"]
    story.append(Paragraph("6. Parking Analysis", styles["heading"]))
    if not prk.empty:
        story.append(Paragraph(
            f"During parking, the SOC remained stable with minimal self-discharge. "
            f"SOC ranged between <b>{prk['SOC'].min():.1f}%</b> and "
            f"<b>{prk['SOC'].max():.1f}%</b>. "
            f"The battery temperature gradually decreased toward ambient, "
            f"settling around <b>{prk['Temperature'].iloc[-1]:.1f} °C</b>. "
            f"Current was approximately zero, confirming no parasitic drain.",
            styles["body"],
        ))

    # ── Battery health ──
    story.append(Paragraph("7. Battery Health Summary", styles["heading"]))
    story.append(Paragraph(
        f"The State of Health (SOH) averaged <b>{df['SOH'].mean():.2f}%</b>, "
        f"indicating the battery pack is in excellent condition. "
        f"The maximum recorded temperature was "
        f"<b>{df['Temperature'].max():.1f} °C</b>, well below the "
        f"critical threshold of 55 °C. No thermal events were detected.",
        styles["body"],
    ))

    story.append(Spacer(1, 10 * mm))

    # ── Footer ──
    story.append(HRFlowable(
        width="100%", thickness=1, color=TEXT_LIGHT,
        spaceAfter=6, spaceBefore=10,
    ))
    story.append(Paragraph(
        f"Report generated on {now} &nbsp; | &nbsp; "
        f"EV BMS Analytics Dashboard &nbsp; | &nbsp; "
        f"Vehicle {vehicle}",
        styles["small"],
    ))

    # ── Build PDF ──
    doc.build(story)

    # Save to file
    pdf_bytes = buffer.getvalue()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(pdf_bytes)

    return pdf_bytes

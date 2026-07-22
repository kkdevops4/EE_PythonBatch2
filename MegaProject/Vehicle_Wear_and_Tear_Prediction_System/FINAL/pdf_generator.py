import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    KeepTogether,
    ListFlowable,
    ListItem
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

from recommendation import generate_summary_paragraphs


def generate_pdf(
    vehicle_id,
    owner_info,
    vehicle_info,
    service_info,
    score,
    recommendations,
    results=None,
    thresholds_df=None
):

    os.makedirs("reports", exist_ok=True)

    pdf = SimpleDocTemplate(
        f"reports/{vehicle_id}.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(
        Paragraph(
            "Vehicle Health Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 15))

    # Vehicle Information
    content.append(
        Paragraph(
            f"<b>Vehicle ID:</b> {vehicle_id}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Owner Name:</b> {owner_info['Owner_Name']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Contact Number:</b> {owner_info['Contact_Number']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Address:</b> {owner_info['Address']}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 10))

    # Vehicle Details
    content.append(
        Paragraph(
            f"<b>Vehicle Number:</b> {vehicle_info['Vehicle_Number']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Make:</b> {vehicle_info['Make']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Model:</b> {vehicle_info['Model']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Health Score:</b> {score}%",
            styles["Normal"]
        )
    )

    # Service Information
    if service_info is not None:

        content.append(Spacer(1, 10))

        content.append(
            Paragraph(
                f"<b>Last Service Date:</b> {service_info['Service_Date']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Next Service Due:</b> {service_info['Next_Service_Due']}",
                styles["Normal"]
            )
        )

    content.append(Spacer(1, 20))

    # Sensor Comparison Table: Standard Ranges vs This Vehicle's Reading
    if results is not None and thresholds_df is not None:

        table_heading = Paragraph("<b>Sensor Readings vs. Standard Values</b>", styles["Heading2"])

        # Build a quick lookup: Parameter name -> (Green, Yellow, Red) range strings
        range_lookup = {}
        for _, row in thresholds_df.iterrows():
            range_lookup[row["Parameter"]] = (
                row["Green Range"],
                row["Yellow Range"],
                row["Red Range"]
            )

        status_colors = {
            "GREEN": colors.HexColor("#2E7D32"),
            "YELLOW": colors.HexColor("#F9A825"),
            "RED": colors.HexColor("#C62828"),
            "UNKNOWN": colors.HexColor("#9E9E9E"),
        }

        table_data = [[
            "Sensor", "Healthy", "Warning", "Critical",
            "Vehicle Reading"
        ]]

        for sensor_name, detail in results.items():
            green_r, yellow_r, red_r = range_lookup.get(sensor_name, ("-", "-", "-"))
            table_data.append([
                sensor_name,
                str(green_r),
                str(yellow_r),
                str(red_r),
                str(detail["value"])
            ])

        sensor_table = Table(
            table_data,
            colWidths=[145, 75, 75, 65, 90],
            repeatRows=1
        )

        table_style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9D9D9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F6F7")]),
        ]

        # Color-code the Vehicle Reading cell to match its GREEN/YELLOW/RED status
        for i, sensor_name in enumerate(results.keys(), start=1):
            status = results[sensor_name]["status"]
            table_style_cmds.append(
                ("TEXTCOLOR", (4, i), (4, i), status_colors.get(status, colors.black))
            )
            table_style_cmds.append(("FONTNAME", (4, i), (4, i), "Helvetica-Bold"))

        sensor_table.setStyle(TableStyle(table_style_cmds))
        content.append(KeepTogether([table_heading, Spacer(1, 8), sensor_table]))
        content.append(Spacer(1, 20))

    # Pie chart (generated by visualization.generate_pie_chart)
    chart_path = "charts/pie_chart.png"
    if os.path.exists(chart_path):
        content.append(KeepTogether([
            Paragraph("<b>Sensor Status Distribution</b>", styles["Heading2"]),
            Spacer(1, 8),
            Image(chart_path, width=420, height=280),
        ]))

    # Vehicle Condition Summary (narrative intro + bulleted breakdown)
    content.append(Spacer(1, 15))

    justified = ParagraphStyle(
        "Justified", parent=styles["Normal"], alignment=TA_JUSTIFY, leading=14
    )

    if results is not None:
        summary_paragraphs = generate_summary_paragraphs(vehicle_id, score, results)
        summary_heading = Paragraph("<b>Vehicle Condition Summary</b>", styles["Heading2"])
        first_para = Paragraph(summary_paragraphs[0], justified) if summary_paragraphs else None
        heading_block = [summary_heading, Spacer(1, 8)]
        if first_para is not None:
            heading_block.append(first_para)
            heading_block.append(Spacer(1, 10))
        content.append(KeepTogether(heading_block))

        bullet_items = [
            ListItem(Paragraph(para, justified), spaceBefore=4, spaceAfter=4)
            for para in summary_paragraphs[1:]
        ]
        if bullet_items:
            content.append(
                ListFlowable(
                    bullet_items,
                    bulletType="bullet",
                    start="circle",
                    leftIndent=16,
                )
            )
    else:
        content.append(Paragraph("<b>Vehicle Condition Summary</b>", styles["Heading2"]))
        content.append(Spacer(1, 8))
        bullet_items = [
            ListItem(Paragraph(rec, styles["Normal"]), spaceBefore=4, spaceAfter=4)
            for rec in recommendations
        ]
        content.append(
            ListFlowable(bullet_items, bulletType="bullet", start="circle", leftIndent=16)
        )

    pdf.build(content)
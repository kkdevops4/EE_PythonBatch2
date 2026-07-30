from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from datetime import datetime


def generate_pdf_report(
        vehicle_info,
        sensor_values,
        sensor_statuses,
        recommendations,
        final_status,
        vehicle_alert):

    pdf = SimpleDocTemplate(
        f"reports/{vehicle_info['Vehicle Number']}.pdf"
    )

    styles = getSampleStyleSheet()

    elements = []

    # ==================================================
    # TITLE
    # ==================================================

    elements.append(
        Paragraph(
            "VEHICLE HEALTH REPORT",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    # ==================================================
    # VEHICLE INFORMATION
    # ==================================================

    elements.append(
        Paragraph(
            "1. Vehicle Information",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    vehicle_text = f"""
    <b>Vehicle Number :</b> {vehicle_info["Vehicle Number"]}<br/>
    <b>Owner Name :</b> {vehicle_info["Owner Name"]}<br/>
    <b>Contact Number :</b> {vehicle_info["Contact Number"]}<br/>
    <b>Model :</b> {vehicle_info["Model"]}<br/>
    <b>Fuel Type :</b> {vehicle_info["Fuel Type"]}<br/>
    <b>Color :</b> {vehicle_info["Color"]}<br/>
    <b>Manufacturing Year :</b> {vehicle_info["Manufacturing Year"]}<br/>
    <b>Registration Date :</b> {vehicle_info["Registration Date"]}<br/>
    """

    elements.append(
        Paragraph(
            vehicle_text,
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # ==================================================
    # OVERALL VEHICLE HEALTH
    # ==================================================

    elements.append(
        Paragraph(
            "2. Overall Vehicle Health",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    if final_status == "GREEN":

        status_text = (
            '<font color="green"><b>Healthy</b></font>'
        )

    elif final_status == "YELLOW":

        status_text = (
            '<font color="orange"><b>Warning</b></font>'
        )

    else:

        status_text = (
            '<font color="red"><b>Critical</b></font>'
        )

    elements.append(
        Paragraph(
            f"<b>Status :</b> {status_text}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            f"<b>Alert :</b> {vehicle_alert}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    # ==================================================
    # SENSOR HEALTH DETAILS
    # ==================================================

    elements.append(
        Paragraph(
            "3. Sensor Health Details",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    table_data = [
        ["Sensor", "Value", "Status"]
    ]

    status_display = {
        "GREEN": "Healthy",
        "YELLOW": "Warning",
        "RED": "Critical"
    }

    for sensor in sensor_values:

        table_data.append([
            sensor,
            str(sensor_values[sensor]),
            status_display.get(
                sensor_statuses[sensor],
                sensor_statuses[sensor]
            )
        ])

    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ("GRID",
             (0, 0),
             (-1, -1),
             1,
             colors.black),

            ("BACKGROUND",
             (0, 0),
             (-1, 0),
             colors.lightgrey),

            ("FONTNAME",
             (0, 0),
             (-1, 0),
             "Helvetica-Bold"),

            ("ALIGN",
             (0, 0),
             (-1, -1),
             "CENTER"),

            ("BOTTOMPADDING",
             (0, 0),
             (-1, 0),
             8)

        ])
    )

    elements.append(table)

    # ==================================================
    # PAGE BREAK
    # ==================================================

    elements.append(PageBreak())

    # ==================================================
    # VEHICLE ANALYTICS
    # ==================================================

    elements.append(
        Paragraph(
            "4. Vehicle Analytics",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Paragraph(
            "Sensor Health Distribution",
            styles["Heading3"]
        )
    )

    elements.append(Spacer(1, 10))

    elements.append(
        Image(
            "graphs/pie_chart.png",
            width=350,
            height=260
        )
    )

    elements.append(Spacer(1, 20))

    # ==================================================
    # RECOMMENDED ACTIONS
    # ==================================================

    elements.append(
        Paragraph(
            "5. Recommended Actions",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 10))

    for item in recommendations:

        text = item.lower()

        if (
            "immediate" in text
            or "replace" in text
            or "overdue" in text
        ):

            color = "red"

        elif (
            "schedule" in text
            or "monitor" in text
            or "plan" in text
            or "check" in text
            or "inspect" in text
        ):

            color = "orange"

        else:

            color = "green"

        elements.append(

            Paragraph(

                f'<font color="{color}">• {item}</font>',

                styles["Normal"]

            )

        )

    elements.append(Spacer(1, 20))

    # ==================================================
    # REPORT GENERATED TIME
    # ==================================================

    generated_time = datetime.now().strftime(
        "%d-%b-%Y %I:%M %p"
    )

    elements.append(
        Paragraph(
            f"<b>Generated On :</b> {generated_time}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 10))

    # ==================================================
    # FOOTER
    # ==================================================

    elements.append(
        Paragraph(
            "<b>Vehicle Wear & Tear Prediction System</b>",
            styles["Normal"]
        )
    )

    pdf.build(elements)

    print("PDF Report Generated Successfully!")

    
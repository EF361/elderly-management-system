import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from datetime import datetime
import io
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from tempfile import NamedTemporaryFile
from io import BytesIO


# Function to connect to the PostgreSQL database
def connect_to_db():
    return psycopg2.connect(
        dbname="elderlymanagement",
        user="postgres",
        password="12345",
        host="localhost",
        port="5432",
    )


# Function to fetch residents and staff for dropdown selection
def get_residents_staff():
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("SELECT resident_id, name FROM Resident")
    residents = cur.fetchall()
    cur.execute("SELECT staff_id, name FROM Staff")
    staff = cur.fetchall()
    conn.close()
    return residents, staff


# Function to create and save charts as images
def create_charts(data):
    event_types = [entry["event_type"] for entry in data]
    frequencies = {event: event_types.count(event) for event in set(event_types)}

    bar_chart_buffer = BytesIO()
    plt.figure(figsize=(8, 4))
    plt.bar(frequencies.keys(), frequencies.values(), color="skyblue")
    plt.xlabel("Event Type")
    plt.ylabel("Frequency")
    plt.title("Event Frequency by Type")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        bar_chart_buffer, format="PNG", bbox_inches="tight"
    )  # Ensure nothing is cut
    bar_chart_buffer.seek(0)

    # Create a line chart for events over time
    event_dates = [entry["event_date"] for entry in data]
    date_frequencies = {
        date: event_dates.count(date) for date in sorted(set(event_dates))
    }

    line_chart_buffer = BytesIO()
    plt.figure(figsize=(8, 4))
    plt.plot(
        date_frequencies.keys(), date_frequencies.values(), marker="o", color="orange"
    )
    plt.xlabel("Date")
    plt.ylabel("Number of Events")
    plt.title("Events Over Time")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(line_chart_buffer, format="PNG", bbox_inches="tight")
    line_chart_buffer.seek(0)

    return bar_chart_buffer, line_chart_buffer


# Inside the generate_pdf_report function
def generate_pdf_report(data, entity_type, entity_name, date_range):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    logo_y_position = height - 150
    logo_width, logo_height = 100, 100

    border_padding = 10
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    c.roundRect(
        width / 2 - (logo_width / 2) - border_padding,
        logo_y_position - border_padding,
        logo_width + (border_padding * 2),
        logo_height + (border_padding * 2),
        10,
    )

    logo_path = "images/logo.png"
    c.drawImage(
        logo_path,
        width / 2 - (logo_width / 2),
        logo_y_position,
        width=logo_width,
        height=logo_height,
    )

    # Title and meta information
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, logo_y_position - 50, f"{entity_type} Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, logo_y_position - 80, f"Name: {entity_name}")
    c.drawString(
        50,
        logo_y_position - 100,
        f"Date Range: {date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}",
    )
    c.drawString(
        50,
        logo_y_position - 120,
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    )

    # Table Headers
    c.setFont("Helvetica-Bold", 10)
    y_position = logo_y_position - 160
    headers = ["Event Date", "Start Time", "End Time", "Event Type", "Description"]
    col_positions = [50, 120, 190, 260, 370]
    for i, header in enumerate(headers):
        c.drawString(col_positions[i], y_position, header)
    y_position -= 15

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.wordWrap = "CJK"

    c.setFont("Helvetica", 10)
    row_height = 30
    max_description_length = 100

    for entry in data:
        if y_position < 50:
            c.showPage()
            y_position = height - 100
            for i, header in enumerate(headers):
                c.drawString(col_positions[i], y_position, header)
            y_position -= row_height

        c.drawString(
            col_positions[0], y_position, entry["event_date"].strftime("%Y-%m-%d")
        )
        c.drawString(
            col_positions[1], y_position, entry["start_time"].strftime("%H:%M")
        )
        c.drawString(col_positions[2], y_position, entry["end_time"].strftime("%H:%M"))
        c.drawString(col_positions[3], y_position, entry["event_type"])

        truncated_description = (
            entry["description"][:max_description_length] + "..."
            if len(entry["description"]) > max_description_length
            else entry["description"]
        )
        c.drawString(col_positions[4], y_position, truncated_description)
        y_position -= row_height

    c.showPage()
    bar_chart, line_chart = create_charts(data)

    with NamedTemporaryFile(delete=False, suffix=".png") as temp_bar_chart:
        temp_bar_chart.write(bar_chart.getvalue())
        bar_chart_path = temp_bar_chart.name

    with NamedTemporaryFile(delete=False, suffix=".png") as temp_line_chart:
        temp_line_chart.write(line_chart.getvalue())
        line_chart_path = temp_line_chart.name

    x_margin = 50
    chart_width = width - 2 * x_margin
    chart_max_height = 200

    c.drawImage(
        bar_chart_path,
        x_margin,
        height - 300,
        width=chart_width,
        height=chart_max_height,
        preserveAspectRatio=True,
        anchor="c",
    )
    c.drawString(x_margin, height - 320, "Figure 1: Event Frequency by Type")

    c.drawImage(
        line_chart_path,
        x_margin,
        height - 550,
        width=chart_width,
        height=chart_max_height,
        preserveAspectRatio=True,
        anchor="c",
    )
    c.drawString(x_margin, height - 570, "Figure 2: Events Over Time")

    c.save()
    buffer.seek(0)

    return buffer


st.title("Report Generation")

st.write("### Report Criteria")
date_range = st.date_input(
    "Date Range", value=(datetime.now().date(), datetime.now().date())
)
entity_type = st.selectbox("Select Type", ["Resident", "Staff"])

residents, staff = get_residents_staff()
if entity_type == "Resident":
    selected_entity = st.selectbox(
        "Select Resident", residents, format_func=lambda x: x[1]
    )
else:
    selected_entity = st.selectbox("Select Staff", staff, format_func=lambda x: x[1])

if st.button("Generate Report"):
    conn = connect_to_db()
    cur = conn.cursor()

    if entity_type == "Resident":
        query = """
            SELECT event_date, start_time, end_time, event_type, description
            FROM Schedule
            WHERE resident_id = %s AND event_date BETWEEN %s AND %s
            ORDER BY event_date;
        """
    else:
        query = """
            SELECT event_date, start_time, end_time, event_type, description
            FROM Schedule
            WHERE staff_id = %s AND event_date BETWEEN %s AND %s
            ORDER BY event_date;
        """
    cur.execute(query, (selected_entity[0], date_range[0], date_range[1]))
    results = cur.fetchall()
    conn.close()

    report_data = [
        {
            "event_date": row[0],
            "start_time": row[1],
            "end_time": row[2],
            "event_type": row[3],
            "description": row[4],
        }
        for row in results
    ]

    pdf_buffer = generate_pdf_report(
        report_data, entity_type, selected_entity[1], date_range
    )

    st.download_button(
        label="Download Report",
        data=pdf_buffer,
        file_name=f"{entity_type}_Report_{selected_entity[1]}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
    )

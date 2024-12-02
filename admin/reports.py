import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import psycopg2
from reportlab.platypus import Image


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
    # Fetch residents
    cur.execute("SELECT resident_id, name FROM Resident")
    residents = cur.fetchall()
    # Fetch staff
    cur.execute("SELECT staff_id, name FROM Staff")
    staff = cur.fetchall()
    conn.close()
    return residents, staff


# Generate PDF report function
def generate_pdf_report(data, entity_type, entity_name, date_range):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Add logo
    logo_path = "images/logo.png"
    c.drawImage(logo_path, width / 2 - 50, height - 100, width=100, height=100)

    # Title and meta information
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 130, f"{entity_type} Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 160, f"Name: {entity_name}")
    c.drawString(
        50,
        height - 180,
        f"Date Range: {date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}",
    )
    c.drawString(
        50,
        height - 200,
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    )

    # Table Headers
    c.setFont("Helvetica-Bold", 10)
    y_position = height - 240
    headers = ["Event Date", "Start Time", "End Time", "Event Type", "Description"]
    col_positions = [50, 120, 190, 260, 330]
    for i, header in enumerate(headers):
        c.drawString(col_positions[i], y_position, header)
    y_position -= 15

    # Table Content
    c.setFont("Helvetica", 10)
    for entry in data:
        if y_position < 50:  # Create a new page if there is not enough space
            c.showPage()
            y_position = height - 100
            for i, header in enumerate(headers):
                c.drawString(col_positions[i], y_position, header)
            y_position -= 15
        c.drawString(
            col_positions[0], y_position, entry["event_date"].strftime("%Y-%m-%d")
        )
        c.drawString(
            col_positions[1], y_position, entry["start_time"].strftime("%H:%M")
        )
        c.drawString(col_positions[2], y_position, entry["end_time"].strftime("%H:%M"))
        c.drawString(col_positions[3], y_position, entry["event_type"])
        c.drawString(col_positions[4], y_position, entry["description"])
        y_position -= 15

    c.save()
    buffer.seek(0)
    return buffer


# Streamlit app layout
st.title("Report Generation")

st.write("### Report Criteria")
date_range = st.date_input(
    "Date Range", value=(datetime.now().date(), datetime.now().date())
)
entity_type = st.selectbox("Select Type", ["Resident", "Staff"])

# Fetch and display relevant selection options based on entity type
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

    # Query based on entity type
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

    # Execute query and fetch data
    cur.execute(query, (selected_entity[0], date_range[0], date_range[1]))
    results = cur.fetchall()
    conn.close()

    # Format the fetched data into a list of dictionaries for PDF generation
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

    # Generate the PDF
    pdf_buffer = generate_pdf_report(
        report_data, entity_type, selected_entity[1], date_range
    )

    # Streamlit download button for the PDF
    st.download_button(
        label="Download Report",
        data=pdf_buffer,
        file_name=f"{entity_type}_Report_{selected_entity[1]}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
    )

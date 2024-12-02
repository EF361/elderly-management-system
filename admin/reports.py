import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import psycopg2


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

    # Title and meta information
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, f"{entity_type} Report: {entity_name}")
    c.setFont("Helvetica", 12)
    c.drawString(
        100,
        height - 120,
        f"Date Range: {date_range[0].strftime('%Y-%m-%d')} to {date_range[1].strftime('%Y-%m-%d')}",
    )
    c.drawString(
        100,
        height - 140,
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    )

    # Table Headers
    c.setFont("Helvetica-Bold", 10)
    y_position = height - 180
    for header in ["Date", "Description", "Details"]:
        c.drawString(100, y_position, header)
        y_position -= 15

    # Table Content
    c.setFont("Helvetica", 10)
    y_position -= 10
    for entry in data:
        if y_position < 100:  # Create a new page if there is not enough space
            c.showPage()
            y_position = height - 100
        c.drawString(100, y_position, entry["date"].strftime("%Y-%m-%d"))
        c.drawString(200, y_position, entry["description"])
        c.drawString(300, y_position, entry["details"])
        y_position -= 15

    c.showPage()
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
            SELECT event_date AS date, event_type AS description, description AS details
            FROM Schedule
            WHERE resident_id = %s AND event_date BETWEEN %s AND %s
            ORDER BY event_date;
        """
    else:
        query = """
            SELECT event_date AS date, event_type AS description, description AS details
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
        {"date": row[0], "description": row[1], "details": row[2]} for row in results
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

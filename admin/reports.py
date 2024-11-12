import streamlit as st
from sqlalchemy import create_engine, text
from datetime import date
from fpdf import FPDF

# Database connection setup
engine = create_engine("postgresql://postgres:12345@localhost:5432/elderlymanagement")

st.title("Report Generation")

# Report Criteria
st.write("## Report Criteria")
date_range = st.date_input("Select Date Range", [date.today(), date.today()])
entity_type = st.selectbox("Choose Report Type", ["Resident", "Staff"])

# Fetch entity options from database
with engine.connect() as conn:
    if entity_type == "Resident":
        query = text("SELECT resident_id, resident_name FROM resident")
        result = conn.execute(query)
        entity_options = {row[1]: row[0] for row in result}  # Access fields by index
    else:
        query = text("SELECT staff_id, staff_name FROM staff")
        result = conn.execute(query)
        entity_options = {row[1]: row[0] for row in result}  # Access fields by index

selected_entity = st.selectbox(f"Select {entity_type}", list(entity_options.keys()))

# Generate Report
if st.button("Generate Report"):
    start_date, end_date = date_range
    entity_id = entity_options[selected_entity]

    # Fetch data for the report
    with engine.connect() as conn:
        if entity_type == "Resident":
            data_query = text("""
                SELECT * FROM activities 
                WHERE resident_id = :entity_id AND date BETWEEN :start_date AND :end_date
            """)
        else:
            data_query = text("""
                SELECT * FROM schedule
                WHERE staff_id = :entity_id AND date BETWEEN :start_date AND :end_date
            """)

        data_result = conn.execute(
            data_query,
            {"entity_id": entity_id, "start_date": start_date, "end_date": end_date},
        ).fetchall()

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"{entity_type} Report", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Name: {selected_entity}", 0, 1)
    pdf.cell(0, 10, f"Date Range: {start_date} to {end_date}", 0, 1)
    pdf.ln(10)

    # Report Content
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Activity Summary", 0, 1)
    pdf.set_font("Arial", "", 12)
    if data_result:
        for row in data_result:
            pdf.cell(
                0, 10, f"- {row[1]}: {row[2]}", 0, 1
            )  # Assuming date and activity fields are at index 1 and 2
    else:
        pdf.cell(0, 10, "No activities recorded in this date range.", 0, 1)

    # Save PDF to a file
    pdf_filename = (
        f"{entity_type}_Report_{selected_entity}_{start_date}_to_{end_date}.pdf"
    )
    pdf.output(pdf_filename)

    # Download link
    with open(pdf_filename, "rb") as f:
        st.download_button(
            label="Download Report",
            data=f,
            file_name=pdf_filename,
            mime="application/pdf",
        )

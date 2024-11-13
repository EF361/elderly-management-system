import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Database connection setup
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

# Dashboard Title
st.title("Admin Dashboard")
st.subheader("Overview")


# Retrieve Data from Database
def get_total_residents():
    with engine.connect() as conn:
        query = text("SELECT COUNT(*) FROM Resident")
        result = conn.execute(query)
        return result.scalar()


def get_staff_on_duty():
    with engine.connect() as conn:
        query = text("SELECT COUNT(*) FROM Staff WHERE role != 'Other'")
        result = conn.execute(query)
        return result.scalar()


# Summary Metrics
total_residents = get_total_residents()
staff_on_duty = get_staff_on_duty()

# Summary Cards
st.write("---")
col1, col2 = st.columns(2)
col1.metric("Total Residents", total_residents)
col2.metric("Staff on Duty", staff_on_duty)

# Analytics Charts
st.write("---")
st.subheader("Analytics and Statistics")

# Resident Gender Distribution Pie Chart
with engine.connect() as conn:
    residents_df = pd.read_sql("SELECT gender FROM Resident", conn)
gender_counts = residents_df["gender"].value_counts()
fig_gender = px.pie(
    values=gender_counts.values,
    names=gender_counts.index,
    title="Resident Gender Distribution",
)
st.plotly_chart(fig_gender)

# Staff Role Distribution Bar Chart
with engine.connect() as conn:
    staff_df = pd.read_sql("SELECT role FROM Staff", conn)
role_counts = staff_df["role"].value_counts()
fig_role = px.bar(
    role_counts,
    x=role_counts.index,
    y=role_counts.values,
    title="Staff Role Distribution",
)
st.plotly_chart(fig_role)

# Medication Frequency Distribution Bar Chart
with engine.connect() as conn:
    medication_df = pd.read_sql("SELECT frequency FROM Medication", conn)
frequency_counts = medication_df["frequency"].value_counts()
fig_frequency = px.bar(
    frequency_counts,
    x=frequency_counts.index,
    y=frequency_counts.values,
    title="Medication Frequency Distribution",
)
st.plotly_chart(fig_frequency)

# Average Medications per Resident Bar Chart
with engine.connect() as conn:
    med_per_resident_df = pd.read_sql(
        text("""
        SELECT resident_id, COUNT(*) AS med_count
        FROM Medication
        GROUP BY resident_id
    """),
        conn,
    )
fig_med_per_resident = px.bar(
    med_per_resident_df,
    x="resident_id",
    y="med_count",
    title="Average Medications per Resident",
)
st.plotly_chart(fig_med_per_resident)

# Top Prescribers in the System
with engine.connect() as conn:
    prescriber_df = pd.read_sql(
        text("""
        SELECT Staff.staff_name, COUNT(Medication.medication_id) AS prescriptions
        FROM Medication
        JOIN Staff ON Medication.prescribed_by = Staff.staff_id
        GROUP BY Staff.staff_name
        ORDER BY prescriptions DESC
        LIMIT 5
    """),
        conn,
    )
fig_top_prescribers = px.bar(
    prescriber_df, x="staff_name", y="prescriptions", title="Top 5 Prescribers"
)
st.plotly_chart(fig_top_prescribers)

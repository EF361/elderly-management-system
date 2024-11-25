import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Database connection setup
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

# Check if user is logged in
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title(f"Welcome, {user_name}!")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

st.subheader("Dashboard Overview")


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

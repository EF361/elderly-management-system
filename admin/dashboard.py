import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Database connection setup
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

# Check if user is logged in, if yes, display title
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title(f"{user_name}'s Dashboard")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Fetch admin profile data (for the sake of example, just assume admin has a name)
admin_info = {
    "name": user_name,
    "role": "Admin",
}

# Fetch contact number for the admin from the database
try:
    with engine.connect() as connection:
        query = text("""
            SELECT contact_number
            FROM admin
            WHERE name = :name
        """)
        result = connection.execute(query, {"name": user_name}).fetchone()

        if result:
            # Access the contact_number value from the tuple using index
            admin_info["contact_number"] = result[
                0
            ]  # Assuming contact_number is the first column
        else:
            st.warning("No contact number found for the admin. Please verify the name.")
except Exception as e:
    st.error(f"Error fetching admin contact data: {e}")
    st.stop()


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

# Analytics Charts
st.write("---")
col1, col2 = st.columns([2, 1])

# Profile Information
with col1:
    st.markdown(
        f"""
        <div style='background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);'>
        <h3 style='color: #333;'>Profile Information</h3>
        <ul style='line-height: 2; font-size: 18px; list-style-type: none;'>
            <li><b>Name:</b> {admin_info["name"]}</li>
            <li><b>Role:</b> {admin_info["role"]}</li>
            <li><b>Contact Number:</b> {admin_info["contact_number"]}</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.metric("Total Residents", total_residents)
    st.write("---")
    st.metric("Staff on Duty", staff_on_duty)

# Analytics and Charts Section
st.write("---")
st.subheader("Staff Demographics")

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

# Resident Demographics Section
st.write("---")
st.subheader("Resident Demographics")

# Resident Age Distribution
with engine.connect() as conn:
    age_data = pd.read_sql(
        "SELECT EXTRACT(YEAR FROM age(date_of_birth)) AS age FROM Resident", conn
    )

if not age_data.empty:
    age_chart = px.histogram(
        age_data,
        x="age",
        nbins=10,
        title="Resident Age Distribution",
        labels={"age": "Age (Years)"},
    )
    st.plotly_chart(age_chart)
else:
    st.info("No resident age data available.")

# Gender Distribution
gender_data = pd.read_sql(
    "SELECT gender, COUNT(*) AS count FROM Resident GROUP BY gender", engine
)
if not gender_data.empty:
    gender_chart = px.pie(
        gender_data,
        names="gender",
        values="count",
        title="Resident Gender Distribution",
    )
    st.plotly_chart(gender_chart)
else:
    st.info("No resident gender data available.")

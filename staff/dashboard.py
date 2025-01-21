import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
import plotly.express as px
from datetime import date

# Database connection setup
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

# Check if user is logged in
if "user_name" in st.session_state:
    staff_name = st.session_state["user_name"]
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Fetch staff profile data
staff_info = None
try:
    with engine.connect() as connection:
        query = text("""
            SELECT name, role, contact_number, hire_date
            FROM Staff
            WHERE name = :name
        """)
        result = connection.execute(query, {"name": staff_name}).mappings().first()

        if result:
            staff_info = dict(result)
        else:
            st.warning("No data found for the logged-in staff. Please verify the name.")
except Exception as e:
    st.error(f"Error fetching staff data: {e}")
    st.stop()

# Fetch tasks assigned today
today_date = date.today()
tasks_assigned_today = 0
try:
    with engine.connect() as connection:
        query = text("""
            SELECT COUNT(*)
            FROM Schedule
            WHERE event_date = :today_date AND staff_id = (
                SELECT staff_id FROM Staff WHERE name = :name
            )
        """)
        tasks_assigned_today = connection.execute(
            query, {"today_date": today_date, "name": staff_name}
        ).scalar()
except Exception as e:
    st.error(f"Error fetching tasks: {e}")
    st.stop()

# Fetch resident demographic data
age_data = gender_data = None
try:
    with engine.connect() as connection:
        # Resident age data
        age_query = text("""
            SELECT EXTRACT(YEAR FROM age(date_of_birth)) AS age FROM Resident
        """)
        age_data = connection.execute(age_query).fetchall()

        # Resident gender data
        gender_query = text("""
            SELECT gender, COUNT(*) AS count FROM Resident GROUP BY gender
        """)
        gender_data = connection.execute(gender_query).fetchall()
except Exception as e:
    st.error(f"Error fetching resident demographic data: {e}")
    st.stop()

# Display the dashboard
st.markdown(
    f"<h1 style='text-align: center;'>Welcome, {staff_info['name']}!</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Staff Profile Section
if staff_info:
    col1, col2 = st.columns([2, 1])

    with col1:
        # Profile details
        st.markdown(
            f"""
            <div style='background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: #333;'>Profile Information</h3>
            <ul style='line-height: 2; font-size: 18px; list-style-type: none;'>
                <li><b>Name:</b> {staff_info["name"]}</li>
                <li><b>Role:</b> {staff_info["role"]}</li>
                <li><b>Contact Number:</b> {staff_info["contact_number"]}</li>
                <li><b>Hire Date:</b> {staff_info["hire_date"]}</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.metric("Tasks Assigned Today", tasks_assigned_today)


st.markdown("---")

# Resident Demographics
st.markdown("<h2>Resident Demographics</h2>", unsafe_allow_html=True)

# Age Demographics
if age_data:
    age_df = pd.DataFrame(age_data, columns=["Age"])
    age_chart = px.histogram(
        age_df,
        x="Age",
        nbins=10,
        title="Resident Age Distribution",
        labels={"Age": "Age (Years)"},
        template="plotly_white",
    )
    st.plotly_chart(age_chart)
else:
    st.info("No resident age data available.")

# Gender Distribution
if gender_data:
    gender_df = pd.DataFrame(gender_data, columns=["Gender", "Count"])
    gender_chart = px.pie(
        gender_df,
        names="Gender",
        values="Count",
        title="Resident Gender Distribution",
        template="plotly_white",
    )
    st.plotly_chart(gender_chart)
else:
    st.info("No resident gender data available.")

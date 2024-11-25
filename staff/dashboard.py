import streamlit as st
from sqlalchemy import create_engine, text
import pandas as pd
import plotly.express as px
from datetime import date

# Set up database connection
engine = create_engine("postgresql://postgres:12345@localhost:5432/elderlymanagement")


# Fetch data function
def fetch_data(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return result.fetchall()


# Dashboard title
st.title("Staff Dashboard")
st.subheader("Daily Overview and Insights")

# Summary Cards
today_date = date.today()
tasks_assigned = fetch_data(
    f"SELECT COUNT(*) FROM Schedule WHERE event_date = '{today_date}' AND event_type IN ('Shift', 'Medical Appointment', 'Social Activity')"
)[0][0]
tasks_completed = fetch_data(
    f"SELECT COUNT(*) FROM Schedule WHERE event_date = '{today_date}' AND description LIKE '%Completed%'"
)[0][0]
staff_shifts = fetch_data(
    f"SELECT COUNT(*) FROM Schedule WHERE event_date = '{today_date}' AND event_type = 'Shift'"
)[0][0]

col1, col2, col3 = st.columns(3)
col1.metric("Tasks Assigned", tasks_assigned)
col2.metric("Tasks Completed", tasks_completed)
col3.metric("Staff Shifts", staff_shifts)

# Task Completion Progress Bar
if tasks_assigned > 0:
    progress = (tasks_completed / tasks_assigned) * 100
else:
    progress = 0
st.progress(int(progress))
st.caption(f"Task Completion: {int(progress)}%")

# Upcoming Shifts Section
st.subheader("Upcoming Shifts")
shift_data = fetch_data(
    f"""
    SELECT s.start_time, s.end_time, r.name AS resident_name, s.event_type
    FROM Schedule s
    LEFT JOIN Resident r ON s.resident_id = r.resident_id
    WHERE s.event_date = '{today_date}' AND s.event_type = 'Shift'
    ORDER BY s.start_time
    """
)
if shift_data:
    shift_df = pd.DataFrame(
        shift_data, columns=["Start Time", "End Time", "Resident", "Event Type"]
    )
    st.dataframe(shift_df, use_container_width=True)
else:
    st.info("No shifts scheduled for today.")

# Resident Interaction Overview
st.subheader("Resident Interaction Metrics")
gender_interaction = fetch_data(
    """
    SELECT r.gender, COUNT(*) 
    FROM Schedule s 
    JOIN Resident r ON s.resident_id = r.resident_id 
    WHERE s.event_date = CURRENT_DATE 
    GROUP BY r.gender
    """
)
if gender_interaction:
    gender_interaction_df = pd.DataFrame(
        gender_interaction, columns=["Gender", "Count"]
    )
    gender_chart = px.pie(
        gender_interaction_df,
        values="Count",
        names="Gender",
        title="Interactions by Gender",
    )
    st.plotly_chart(gender_chart)
else:
    st.info("No interaction data available for today.")


# Resident Age Overview
st.subheader("Resident Age Overview")
age_data = fetch_data(
    "SELECT EXTRACT(YEAR FROM age(date_of_birth)) AS age FROM Resident"
)
if age_data:
    age_df = pd.DataFrame(age_data, columns=["Age"])
    age_histogram = px.histogram(
        age_df, x="Age", nbins=10, title="Resident Age Distribution"
    )
    st.plotly_chart(age_histogram)
else:
    st.info("No age data available.")

# Task Summary Section
st.subheader("Task Summary")
task_summary_data = fetch_data(
    f"""
    SELECT s.event_type, COUNT(*) 
    FROM Schedule s 
    WHERE s.event_date = '{today_date}' 
    GROUP BY s.event_type
    """
)
if task_summary_data:
    task_summary_df = pd.DataFrame(task_summary_data, columns=["Task Type", "Count"])
    task_bar_chart = px.bar(
        task_summary_df, x="Task Type", y="Count", title="Task Breakdown for Today"
    )
    st.plotly_chart(task_bar_chart)
else:
    st.info("No task data available for today.")

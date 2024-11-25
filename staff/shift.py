import streamlit as st
from sqlalchemy import create_engine, text
from datetime import date

# Database connection setup
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

# Check if user is logged in
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title(f"{user_name}'s Schedule")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

staff_id = None
try:
    with engine.connect() as connection:
        query = text("""
            SELECT staff_id 
            FROM staff 
            WHERE name = :name
        """)
        result = connection.execute(query, {"name": user_name}).fetchone()

        if result:
            staff_id = result[0]  # Get the resident_id (first element of the tuple)
        else:
            st.warning("No data found for the logged-in user. Please verify the name.")
            st.stop()
except Exception as e:
    st.error(f"Error fetching staff ID: {e}")
    st.stop()

# Schedule display
# Date picker for schedule selection, defaulting to today's date
selected_date = st.date_input("Select a date", value=date.today())

# Fetch schedule for the selected date
schedule_data = None
try:
    with engine.connect() as connection:
        query = text("""
            SELECT s.event_type, s.event_date, s.start_time, s.end_time, s.description
            FROM schedule s
            WHERE s.staff_id = :staff_id
            AND s.event_date = :event_date
            ORDER BY s.start_time
        """)
        result = connection.execute(
            query, {"staff_id": staff_id, "event_date": selected_date}
        ).fetchall()

        if result:
            schedule_data = result
        else:
            st.write("No events scheduled for this date.")
except Exception as e:
    st.error(f"Error fetching schedule data: {e}")

# Display schedule data if available
if schedule_data:
    for event in schedule_data:
        event_type = event[0]
        event_date = event[1]
        start_time = event[2]
        end_time = event[3]
        description = event[4]

        # Display each event in a readable format
        st.write(f"### {event_type}")
        st.write(f"**Date:** {event_date}")
        st.write(f"**Time:** {start_time} - {end_time}")
        st.write(f"**Description:** {description}")
        st.write("---")

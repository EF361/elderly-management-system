import streamlit as st
from sqlalchemy import create_engine, text
from datetime import date

DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

st.markdown(
    """
    <style>
        body {
            background-color: #f9f9f9;
        }
        .main-container {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0);
        }
        .title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .event-card {
            background-color: #f1f1f1;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid ;
        }
        .event-title {
            font-size: 20px;
            font-weight: bold;
        }
        .event-details {
            font-size: 16px;
            color: #555;
        }
    </style>
""",
    unsafe_allow_html=True,
)

with st.container():
    if "user_name" in st.session_state:
        user_name = st.session_state["user_name"]
        st.markdown(
            f"<div class='title'>{user_name}'s Schedule</div>", unsafe_allow_html=True
        )
    else:
        st.error("You are not logged in. Please log in to access the dashboard.")
        st.stop()
    resident_id = None
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT resident_id 
                FROM resident 
                WHERE name = :name
            """)
            result = connection.execute(query, {"name": user_name}).fetchone()

            if result:
                resident_id = result[0]
            else:
                st.warning(
                    "No data found for the logged-in user. Please verify the name."
                )
                st.stop()
    except Exception as e:
        st.error(f"Error fetching resident ID: {e}")
        st.stop()

    selected_date = st.date_input("Select a date", value=date.today())

    schedule_data = None
    try:
        with engine.connect() as connection:
            query = text("""
                SELECT s.event_type, s.event_date, s.start_time, s.end_time, s.description
                FROM schedule s
                WHERE s.resident_id = :resident_id
                AND s.event_date = :event_date
                ORDER BY s.start_time
            """)
            result = connection.execute(
                query, {"resident_id": resident_id, "event_date": selected_date}
            ).fetchall()

            if result:
                schedule_data = result
            else:
                st.info("No events scheduled for this date.")
    except Exception as e:
        st.error(f"Error fetching schedule data: {e}")

    if schedule_data:
        for event in schedule_data:
            event_type = event[0]
            event_date = event[1]
            start_time = event[2]
            end_time = event[3]
            description = event[4]

            formatted_start_time = start_time.strftime("%H:%M")
            formatted_end_time = end_time.strftime("%H:%M")

            st.markdown(
                f"""
                <div class='event-card'>
                    <div class='event-title'>{event_type}</div>
                    <div class='event-details'>
                        <strong>Date:</strong> {event_date}<br>
                        <strong>Time:</strong> {formatted_start_time} - {formatted_end_time}<br>
                        <strong>Description:</strong> {description}
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

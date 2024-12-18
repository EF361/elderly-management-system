import streamlit as st
from openai import OpenAI
from sqlalchemy import create_engine, text
import re

# Database connection setup
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)


# Function to get resident_id from username
def get_resident_id(user_name):
    query = text("SELECT resident_id FROM Resident WHERE name = :name LIMIT 1;")
    with engine.connect() as conn:
        result = conn.execute(query, {"name": user_name}).fetchone()
    if result:
        return result[0]
    return None


# Function to query the database for resident's schedule
def get_schedule(resident_id):
    query = text("""
        SELECT event_type, event_date, start_time, end_time, description 
        FROM Schedule 
        WHERE resident_id = :resident_id
        ORDER BY event_date, start_time;
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"resident_id": resident_id}).fetchall()
    return result


# Function to query the database for resident's medication
def get_medication(resident_id):
    query = text("""
        SELECT m.medicine_name, m.usage, m.description 
        FROM Medical_Record r
        JOIN Medicine m ON r.medicine_id = m.medicine_id
        WHERE r.resident_id = :resident_id
        ORDER BY r.record_date DESC;
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"resident_id": resident_id}).fetchall()
    return result


# Function to detect relevant questions
def detect_relevant_question(prompt):
    schedule_keywords = re.compile(
        r"(schedule|appointment|event|activity|when|where)", re.IGNORECASE
    )
    medication_keywords = re.compile(
        r"(medicine|medication|pill|drug|treatment|dose)", re.IGNORECASE
    )

    if schedule_keywords.search(prompt):
        return "schedule"
    elif medication_keywords.search(prompt):
        return "medication"
    else:
        return "other"


# Function to get admin contact number
def get_admin_contact():
    query = text("SELECT contact_number FROM Admin LIMIT 1;")
    with engine.connect() as conn:
        result = conn.execute(query).fetchone()
    if result:
        return result[0]
    return (
        "123-456-7890"  # Fallback contact number if no admin is found in the database
    )


# Check if user is logged in
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title(f"{user_name}'s Chatbot")

    # Fetch resident_id based on user_name
    resident_id = get_resident_id(user_name)
    if not resident_id:
        st.error(
            "Could not find your details in the database. Please contact the admin."
        )
        admin_contact = get_admin_contact()
        st.write(
            f"If you have any issues, you can contact the admin at: {admin_contact}"
        )
        st.stop()
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# OpenAI API setup
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine the type of question
    question_type = detect_relevant_question(prompt)
    if question_type == "schedule":
        schedule = get_schedule(resident_id)
        if schedule:
            response = "Here is your schedule:\n" + "\n".join(
                f"- {event[0]} on {event[1]} from {event[2]} to {event[3]}: {event[4]}"
                for event in schedule
            )
        else:
            response = "You have no upcoming events in your schedule."
    elif question_type == "medication":
        medication = get_medication(resident_id)
        if medication:
            response = "Here is your medication information:\n" + "\n".join(
                f"- {med[0]}: {med[1]}. {med[2]}" for med in medication
            )
        else:
            response = "You have no medication records available."
    else:
        admin_contact = get_admin_contact()
        response = f"I can't answer that. Please contact the admin at: {admin_contact} for further assistance."

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

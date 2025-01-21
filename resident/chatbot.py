import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import openai
import difflib

# --- CONFIGURATION ---
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

# --- API KEYS ---
OPENAI_API_KEY = st.secrets["api_keys"]["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# --- COMMONLY USED TERMS ---
VALID_TERMS = ["schedule", "medication", "admin", "contact"]


def suggest_term(input_word):
    """Suggest the closest matching term for typos."""
    suggestions = difflib.get_close_matches(input_word, VALID_TERMS, n=1, cutoff=0.8)
    return suggestions[0] if suggestions else None


# --- DATABASE FUNCTIONS ---
def get_resident_info(user_name):
    """Fetch resident information from the database."""
    query = text(
        "SELECT resident_id, name, gender, contact_number, date_of_birth, address FROM Resident WHERE name = :name LIMIT 1;"
    )
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"name": user_name}).fetchone()
        if result:
            return {
                "resident_id": result[0],
                "name": result[1],
                "gender": result[2],
                "contact_number": result[3],
                "date_of_birth": result[4],
                "address": result[5],
            }
    except SQLAlchemyError as e:
        st.error("Database error. Please contact the admin.")
        print(e)
    return None


def get_emergency_contact(resident_id):
    """
    Fetch emergency contact information for a specific resident.
    Returns a list of dictionaries with emergency contact details.
    """
    query = text("""
        SELECT contact_id, contact_name, relationship, contact_number
        FROM Resident_Emergency_Contacts
        WHERE resident_id = :resident_id;
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"resident_id": resident_id}).fetchall()
        if result:
            emergency_contacts = []
            for row in result:
                emergency_contacts.append(
                    {
                        "contact_id": row[0],
                        "contact_name": row[1],
                        "relationship": row[2],
                        "contact_number": row[3],
                    }
                )
            return emergency_contacts
        else:
            return []
    except SQLAlchemyError as e:
        st.error("Database error. Please contact the admin.")
        print(e)
        return []


def get_schedule(resident_id, date=None):
    """
    Fetch schedule for a specific resident on a given date.
    Returns a list of dictionaries with schedule details.
    """
    if not date:
        date = datetime.today().date()

    query = text("""
        SELECT event_type, event_date, start_time, end_time, description 
        FROM Schedule 
        WHERE resident_id = :resident_id AND event_date = :date
        ORDER BY start_time;
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(
                query, {"resident_id": resident_id, "date": date}
            ).fetchall()

        if result:
            schedule = []
            for row in result:
                schedule.append(
                    {
                        "event_type": row[0],
                        "event_date": row[1],
                        "start_time": row[2],
                        "end_time": row[3],
                        "description": row[4],
                    }
                )
            return schedule
        else:
            return []
    except SQLAlchemyError as e:
        st.error("Database error. Please contact the admin.")
        print(e)
        return []


def get_medication(resident_id):
    """Fetch medication records for a resident."""
    query = text("""
        SELECT m.medicine_name, m.usage, m.description 
        FROM Medical_Record r
        JOIN Medicine m ON r.medicine_id = m.medicine_id
        WHERE r.resident_id = :resident_id
        ORDER BY r.record_date DESC;
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"resident_id": resident_id}).fetchall()
        return result
    except SQLAlchemyError as e:
        st.error("Database error. Please contact the admin.")
        print(e)
        return []


def get_admin_contact():
    """Fetch admin contact information."""
    query = text("SELECT name, contact_number FROM Admin LIMIT 1;")
    try:
        with engine.connect() as conn:
            result = conn.execute(query).fetchone()
        if result:
            return {"name": result[0], "contact_number": result[1]}
    except SQLAlchemyError as e:
        st.error("Database error. Please contact the admin.")
        print(e)
    return {"name": "Unknown", "contact_number": "123-456-7890"}


# --- CHATBOT FUNCTIONS ---


def generate_response(prompt, resident_info):
    """
    Generate chatbot responses using OpenAI, including schedule and medication details.
    Handle typo corrections for key terms like 'schedule' and 'medication'.
    """
    # Check for typos in key terms
    words = prompt.lower().split()
    for word in words:
        suggestion = suggest_term(word)
        if suggestion and word != suggestion:
            return f"It seems like you meant '{suggestion}'. Could you please type your query again?"

    try:
        # Fetch required details
        admin = get_admin_contact()
        emergency_contacts = get_emergency_contact(resident_info["resident_id"])
        schedule = get_schedule(resident_info["resident_id"])
        medications = get_medication(resident_info["resident_id"])

        # Format emergency contact details
        emergency_contact_info = (
            f"Their emergency contact name is {emergency_contacts[0]['contact_name']}.\n"
            f"Their emergency contact relationship is {emergency_contacts[0]['relationship']}.\n"
            f"Their emergency contact number is {emergency_contacts[0]['contact_number']}."
            if emergency_contacts
            else "No emergency contacts found."
        )

        # Format schedule details
        schedule_info = (
            "\n".join(
                [
                    f"- {event['event_type']} on {event['event_date']} from {event['start_time']} to {event['end_time']} ({event['description']})"
                    for event in schedule
                ]
            )
            if schedule
            else "No events scheduled."
        )

        # Format medication details
        medication_info = (
            "\n".join([f"- {med[0]}: {med[1]} ({med[2]})" for med in medications])
            if medications
            else "No medications recorded."
        )

        # Construct OpenAI messages
        messages = [
            {
                "role": "system",
                "content": """You are a helpful virtual assistant for an elderly care management system. 
                You are going to help with answering scheduling for the day (you do not plan schedule for the resident)""",
            },
            {
                "role": "system",
                "content": f"""The user's name is {resident_info["name"]} 
                (ID: {resident_info["resident_id"]}).
                Their gender is {resident_info["gender"]}.
                Their contact number is {resident_info["contact_number"]}.
                Their date of birth is {resident_info["date_of_birth"]}. 
                Their address is {resident_info["address"]}. 

                {emergency_contact_info}

                Admin contact is {admin["name"]} with their phone number {admin["contact_number"]}.

                Today's schedule:
                {schedule_info}

                Current medications:
                {medication_info}

                Do not generate data not found in the database.
                Do not answer questions that are not related to the elderly care management system: 
                Example out of range questions: What is the history of Malaysia.""",
            },
            {"role": "user", "content": prompt},
        ]

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", messages=messages, max_tokens=200, temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        st.error("Error generating response. Please contact the admin.")
        print(e)
        return "I'm having trouble processing your request. Please contact the admin for further assistance."


# --- MAIN APP LOGIC ---
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.header(f"{user_name}'s chatbot")

    resident_info = get_resident_info(user_name)
    if not resident_info:
        st.error("Your details could not be found. Contact the admin.")
        admin = get_admin_contact()
        st.write(f"Contact {admin['name']} at: {admin['contact_number']}")
        st.stop()
else:
    st.error("You are not logged in. Please log in to access the chatbot.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using OpenAI and resident info
    response = generate_response(prompt, resident_info)

    # Display response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

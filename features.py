import streamlit as st


def features_page():
    st.title("About CareLink")

    st.header("Company/Project Background")
    st.subheader("CareLink: Pioneering Elderly Care")
    st.write("""
        CareLink is an innovative AI-powered management system, crafted to enhance the operations of elderly care homes.
        Our platform streamlines various administrative tasks, ensuring that residents receive optimal care, staff schedules are efficiently managed, and families remain well-informed.
    """)

    st.header("Features")

    # Feature 1: AI Chatbot for Assistance
    st.subheader("AI Chatbot for Assistance")
    st.image("images/ai-chatbot-for-assistant.png", width=200)
    st.write("""
        - **Natural Language Processing** for understanding and responding to queries.
        - Seamless integration with other system features, such as scheduling and medication tracking.
        - Multilingual support for better accessibility.
    """)

    # Feature 2: Resident Management
    st.subheader("Resident Management")
    st.image("images/resident-management.png", width=200)
    st.write("""
        - Centralized database of resident profiles with health history, dietary preferences, and activity logs.
        - Customizable care plans and schedules.
        - Alerts and notifications for important updates or changes in a resident's status.
    """)

    # Feature 3: Staff Scheduling
    st.subheader("Staff Scheduling")
    st.image("images/staff-scheduling.png", width=200)
    st.write("""
        - Drag-and-drop interface for creating and adjusting schedules.
        - Automated conflict detection to avoid overlapping shifts.
        - Integration with resident care plans to match staff with the appropriate residents.
    """)

    # Feature 4: Medication Tracking
    st.subheader("Medication Tracking")
    st.image("images/medication-tracking.png", width=200)
    st.write("""
        - Automated reminders for medication times.
        - Logging of medication administration for accountability.
        - Alerts for missed doses or potential medication interactions.
    """)

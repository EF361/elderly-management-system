import streamlit as st
from sqlalchemy import create_engine, text

# Database connection setup
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

# Check if user is logged in
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Fetch resident data from the database
resident_info = None
try:
    with engine.connect() as connection:
        query = text("""
            SELECT r.name, r.date_of_birth, r.gender, r.contact_number, r.username, r.address,
                   rec.contact_name, rec.relationship, rec.contact_number AS emergency_contact
            FROM resident r
            LEFT JOIN resident_emergency_contacts rec ON r.resident_id = rec.resident_id
            WHERE r.name = :name
        """)
        result = connection.execute(query, {"name": user_name}).mappings().first()

        if result:
            resident_info = dict(result)
        else:
            st.warning("No data found for the logged-in user. Please verify the name.")
except Exception as e:
    st.error(f"Error fetching resident data: {e}")
    st.stop()

# Display profile information
if resident_info:
    st.markdown(
        f"<h1 style='text-align: center;'>Welcome, {resident_info['name']}!</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Create columns for layout
    col1, col2 = st.columns([1, 2])

    with col1:
        # Display gender-based profile picture
        if resident_info["gender"] == "Male":
            st.image("images/old_man_logo.png", width=200)
        elif resident_info["gender"] == "Female":
            st.image("images/old_women_logo.png", width=200)

    with col2:
        # Display resident details in an info box
        st.markdown(
            """
            <div style='background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);'>
            <h3 style='color: #333;'>Profile Information</h3>
            <ul style='line-height: 2; font-size: 18px; list-style-type: none;'>
                <li><b>Name:</b> {name}</li>
                <li><b>Date of Birth:</b> {dob}</li>
                <li><b>Gender:</b> {gender}</li>
                <li><b>Contact Number:</b> {contact}</li>
                <li><b>Username:</b> {username}</li>
                <li><b>Address:</b> {address}</li>
            </ul>
            </div>
        """.format(
                name=resident_info["name"],
                dob=resident_info["date_of_birth"],
                gender=resident_info["gender"],
                contact=resident_info["contact_number"],
                username=resident_info["username"],
                address=resident_info["address"],
            ),
            unsafe_allow_html=True,
        )

    # Emergency contact information
    st.markdown("---")
    st.markdown(
        """
        <div style='background-color: #ffebcd; padding: 20px; border-radius: 10px; box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);'>
        <h3 style='color: #d35400;'>Emergency Contact Information</h3>
        <ul style='line-height: 2; font-size: 18px; list-style-type: none;'>
            <li><b>Name:</b> {contact_name}</li>
            <li><b>Relationship:</b> {relationship}</li>
            <li><b>Contact Number:</b> {emergency_contact}</li>
        </ul>
        </div>
    """.format(
            contact_name=resident_info.get("contact_name", "N/A"),
            relationship=resident_info.get("relationship", "N/A"),
            emergency_contact=resident_info.get("emergency_contact", "N/A"),
        ),
        unsafe_allow_html=True,
    )

else:
    st.error("Unable to display resident information. Please contact support.")

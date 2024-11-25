import streamlit as st
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

# Fetch resident data from the database
resident_info = None
try:
    with engine.connect() as connection:
        query = text("""
            SELECT r.name, r.date_of_birth, r.gender, r.contact_number, r.email, r.address,
                   rec.contact_name, rec.relationship, rec.contact_number AS emergency_contact
            FROM resident r
            LEFT JOIN resident_emergency_contacts rec ON r.resident_id = rec.resident_id
            WHERE r.name = :name
        """)
        result = (
            connection.execute(query, {"name": user_name}).mappings().first()
        )  # Use mappings for better compatibility

        if result:
            resident_info = dict(result)  # Convert the mapping to a dictionary
        else:
            st.warning("No data found for the logged-in user. Please verify the name.")
except Exception as e:
    st.error(f"Error fetching resident data: {e}")
    st.stop()

# Display profile picture and details if data exists
if resident_info:
    # Display gender-based image
    if resident_info["gender"] == "Male":
        st.image("images/old_man_logo.png", width=150)
    elif resident_info["gender"] == "Female":
        st.image("images/old_women_logo.png", width=150)
    else:
        st.image("images/resident-placeholder.jpg", width=150)

    st.header("Profile Information")

    # Format data for display
    profile_markdown = f"""
    **Name:** {resident_info['name']}  
    **Date of Birth:** {resident_info['date_of_birth']}  
    **Gender:** {resident_info['gender']}  
    **Contact Number:** {resident_info['contact_number']}  
    **Email:** {resident_info['email']}  
    **Address:** {resident_info['address']}  

    ### Emergency Contact Information:
    **Name:** {resident_info.get('contact_name', 'N/A')}  
    **Relationship:** {resident_info.get('relationship', 'N/A')}  
    **Contact Number:** {resident_info.get('emergency_contact', 'N/A')}
    """
    st.markdown(profile_markdown)
else:
    st.error("Unable to display resident information. Please contact support.")

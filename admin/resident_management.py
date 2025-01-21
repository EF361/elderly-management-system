import streamlit as st
from datetime import datetime
from management import Management
from contact_number import ContactNumberInput

# Initialize the Resident Manager
resident_manager = Management(table_name="resident")
emergency_contact = Management(table_name="resident_emergency_contacts")

resident_contact_input = ContactNumberInput(
    label="Enter Resident Contact Number", placeholder="01122233345"
)
emergency_contact_input = ContactNumberInput(
    label="Enter Emergency Contact Number", placeholder="01133344455"
)

# Check if user is logged in
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title("Resident Management")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

st.subheader("Resident")
resident_manager.show_table()
st.subheader("Resident Emergency Contact")
emergency_contact.show_table()

# Fetch residents for dropdown selection
residents = resident_manager.fetch_options("Resident", "resident_id", "name")

# Operation Selection
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    with st.expander("Create Resident"):
        # Input fields for new resident
        name = st.text_input("Resident Name:")
        date_of_birth = st.date_input(
            "Date of Birth:",
            min_value=datetime(1930, 1, 1),
            max_value=datetime(2000, 12, 31),
        )
        gender = st.selectbox("Gender:", options=["Male", "Female"])
        contact_number = resident_contact_input.render()
        address = st.text_area("Address:")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        # Emergency Contact
        contact_name = st.text_input("Emergency Contact Name:")
        relationship = st.text_input("Relationship:")
        emergency_contact_number = emergency_contact_input.render()

        # Submit the data
        if st.button("Add Resident"):
            # Check if any required fields are empty
            if not name or not contact_number or not username or not password:
                st.error("Please fill in all required fields")
            elif not contact_name or not emergency_contact_number:
                st.error("Emergency contact information is required.")
            else:
                resident_data = {
                    "name": name,
                    "date_of_birth": date_of_birth,
                    "gender": gender,
                    "contact_number": contact_number,
                    "address": address,
                    "username": username,
                    "password": password,
                }
                emergency_contact = {
                    "contact_name": contact_name,
                    "relationship": relationship,
                    "contact_number": emergency_contact_number,
                }
                resident_manager.create_resident_with_contacts(
                    resident_data, [emergency_contact]
                )


elif option == "Update":
    with st.expander("Update Resident"):
        # Select a resident to update
        resident_name = st.selectbox("Select Resident:", options=list(residents.keys()))
        selected_resident_id = residents[resident_name]

        # Fields to update
        contact_number = resident_contact_input.render()
        address = st.text_area("Address:", placeholder="Optional")
        username = st.text_input("Username:", placeholder="Optional")
        password = st.text_input("Password:", type="password", placeholder="Optional")

        # Update emergency contact
        st.write("Emergency Contact:")
        contact_name = st.text_input("Contact Name:", key="update_contact_name")
        relationship = st.text_input("Relationship:", key="update_relationship")
        emergency_contact_number = emergency_contact_input.render(
            key="emergency_contact_number"
        )
        emergency_contact = {
            "contact_name": contact_name,
            "relationship": relationship,
            "contact_number": emergency_contact_number,
        }

        # Submit the update
        if st.button("Update Resident"):
            try:
                resident_manager.update_record(
                    user_id=selected_resident_id,
                    contact_number=contact_number,
                    address=address,
                    username=username,
                    password=password,
                    emergency_contacts=[
                        emergency_contact
                    ],  # Pass the emergency contact to update
                )
            except Exception as e:
                st.error(f"Error updating resident: {e}")


elif option == "Delete":
    with st.expander("Delete Resident"):
        # Select a resident to delete
        resident_name = st.selectbox(
            "Select Resident to Delete:", options=list(residents.keys())
        )
        selected_resident_id = residents[resident_name]

        # Confirm deletion
        st.write(f"Are you sure you want to delete '{resident_name}'?")
        if st.button("Delete Resident"):
            try:
                resident_manager.delete_resident(selected_resident_id)
                resident_manager.clean_up_null_entries()
            except Exception as e:
                st.error(f"Error deleting resident: {e}")

import streamlit as st
from management import Management

# Initialize the Resident Manager
resident_manager = Management(table_name="Resident")

# Check if user is logged in
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title("Resident Management")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Fetch the resident table with emergency contacts
residents_with_contacts = resident_manager.fetch_full_residents_with_contacts()

# Display resident table in a readable format
if residents_with_contacts:
    st.table(residents_with_contacts)
else:
    st.write("No resident records available.")

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
        date_of_birth = st.date_input("Date of Birth:")
        gender = st.selectbox("Gender:", options=["Male", "Female"])
        contact_number = st.text_input("Contact Number:")
        address = st.text_area("Address:")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        # Emergency Contacts
        emergency_contacts = []
        for i in range(2):  # Collect 2 emergency contacts
            contact_name = st.text_input(
                f"Emergency Contact {i + 1} Name:", key=f"ec_name_{i}"
            )
            relationship = st.text_input(
                f"Relationship {i + 1}:", key=f"ec_relationship_{i}"
            )
            emergency_contact_number = st.text_input(
                f"Contact Number {i + 1}:", key=f"ec_number_{i}"
            )
            if contact_name and emergency_contact_number:
                emergency_contacts.append(
                    {
                        "contact_name": contact_name,
                        "relationship": relationship,
                        "contact_number": emergency_contact_number,
                    }
                )

        # Submit the data
        if st.button("Add Resident"):
            if len(emergency_contacts) < 2:
                st.error("At least two emergency contacts are required.")
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
                resident_manager.create_resident_with_contacts(
                    resident_data, emergency_contacts
                )
                st.success("Resident added successfully.")

elif option == "Update":
    with st.expander("Update Resident"):
        # Select a resident to update
        resident_name = st.selectbox("Select Resident:", options=list(residents.keys()))
        selected_resident_id = residents[resident_name]

        # Fields to update
        contact_number = st.text_input("Contact Number:", placeholder="Optional")
        address = st.text_area("Address:", placeholder="Optional")
        username = st.text_input("Username:", placeholder="Optional")
        password = st.text_input("Password:", type="password", placeholder="Optional")

        # Update emergency contacts
        emergency_contacts = []
        for i in range(2):  # Allow updating the first 2 emergency contacts
            st.write(f"Emergency Contact {i + 1}:")
            contact_name = st.text_input(
                f"Contact Name {i + 1}:", key=f"update_contact_name_{i}"
            )
            relationship = st.text_input(
                f"Relationship {i + 1}:", key=f"update_relationship_{i}"
            )
            emergency_contact_number = st.text_input(
                f"Contact Number {i + 1}:", key=f"update_contact_number_{i}"
            )
            emergency_contacts.append(
                {
                    "contact_name": contact_name,
                    "relationship": relationship,
                    "contact_number": emergency_contact_number,
                }
            )

        # Submit the update
        if st.button("Update Resident"):
            try:
                resident_manager.update_record(
                    resident_id=selected_resident_id,
                    contact_number=contact_number,
                    address=address,
                    username=username,
                    password=password,
                    emergency_contacts=emergency_contacts,
                )
                st.success("Resident updated successfully.")
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
                resident_manager.delete_record(selected_resident_id)
                st.success(
                    f"Resident '{resident_name}' and their emergency contacts have been deleted."
                )
            except Exception as e:
                st.error(f"Error deleting resident: {e}")

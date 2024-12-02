import streamlit as st
from datetime import date
from management import Management

resident_manager = Management(table_name="Resident")

# Check if user is logged in, if yes, display title
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title("Resident Management")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()


# Display the resident table
residents_with_contacts = resident_manager.fetch_full_residents_with_contacts()
resident_manager.show_full_table(residents_with_contacts)


# Fetch residents for dropdown selections
residents = resident_manager.fetch_options("Resident", "resident_id", "name")

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

# Create resident with emergency contacts
if option == "Create":
    with st.expander("Create Resident"):
        name = st.text_input("Resident Name:")
        date_of_birth = st.date_input("Date of Birth:")
        gender = st.selectbox("Gender:", options=["Male", "Female"])
        contact_number = st.text_input("Contact Number:")
        address = st.text_area("Address:")
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")

        # Emergency contacts
        emergency_contacts = []
        for i in range(2):  # At least 2 emergency contacts
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

        if st.button("Add Resident"):
            if not emergency_contacts or len(emergency_contacts) < 2:
                st.error("At least two valid emergency contacts are required.")
            else:
                resident_data = {
                    "name": name,
                    "date_of_birth": date_of_birth,
                    "gender": gender,
                    "contact_number": contact_number,
                    "address": address,
                    "email": email,
                    "password": password,
                }
                resident_manager.create_resident_with_contacts(
                    resident_data, emergency_contacts
                )


elif option == "Update":
    with st.expander("Update Resident"):
        # Select a resident by name
        resident_name = st.selectbox("Select Resident:", options=list(residents.keys()))
        selected_resident_id = residents[resident_name]
        st.write(f"Selected Resident ID: {selected_resident_id}")

        # Input fields for resident update
        contact_number = st.text_input("Contact Number:", placeholder="Optional")
        address = st.text_area("Address:", placeholder="Optional")
        email = st.text_input("Email:", placeholder="Optional")
        password = st.text_input("Password:", type="password", placeholder="Optional")

        # Emergency contact update
        emergency_contacts = []
        for i in range(2):  # Allow updating the first two contacts
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

        if st.button("Update Resident"):
            try:
                # Update resident details and emergency contacts
                resident_manager.update_record(
                    resident_id=selected_resident_id,
                    contact_number=contact_number,
                    address=address,
                    email=email,
                    password=password,
                    emergency_contacts=emergency_contacts,
                )
            except Exception as e:
                st.error(f"There is an error: {e}")


elif option == "Delete":
    resident_name = st.selectbox(
        "Select Resident to Delete:", options=list(residents.keys())
    )
    selected_resident_id = residents[resident_name]

    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{resident_name}'?")
        if st.button("Delete Resident"):
            try:
                resident_manager.delete_record(selected_resident_id)
                st.success(
                    f"Resident '{resident_name}' and their emergency contacts have been deleted."
                )
            except Exception as e:
                st.error(f"There is an error: {e}")

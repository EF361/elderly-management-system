import streamlit as st
from datetime import date
from management import UserManagement

# Initialize UserManagement for the Resident table
user_management = UserManagement(table_name="Resident")

st.title("Resident Management")

# Display the resident table
user_management.show_table()

# Fetch residents for dropdown selections
residents = user_management.fetch_options("Resident", "resident_id", "name")

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    st.write("### Add New Resident")

    # Input fields for resident creation
    name = st.text_input("Resident Name:")
    date_of_birth = st.date_input("Date of Birth:", value=date(1970, 1, 1))
    gender = st.selectbox("Gender:", options=["Male", "Female"])
    contact_number = st.text_input("Contact Number:")
    address = st.text_area("Address:")
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if st.button("Add Resident"):
        try:
            # Create the resident record
            user_management.create_record(
                resident_name=name,
                date_of_birth=date_of_birth,
                gender=gender,
                contact_number=contact_number,
                address=address,
                email=email,
                password=password,
            )
        except Exception as e:
            st.error(f"There is an error: {e}")

elif option == "Update":
    st.write("### Update Resident")

    # Select a resident by name
    resident_name = st.selectbox("Select Resident:", options=list(residents.keys()))

    # Fetch the selected resident's details
    selected_resident_id = residents[resident_name]
    st.write(f"Selected Resident ID: {selected_resident_id}")

    # Input fields for updatable data
    contact_number = st.text_input("Contact Number:")
    address = st.text_area("Address:")
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if st.button("Update Resident"):
        # Update the resident record
        user_management.update_record(
            selected_resident_id,
            contact_number=contact_number,
            address=address,
            email=email,
            password=password,
        )

elif option == "Delete":
    st.write("### Delete Resident")

    # Select a resident by name for deletion
    resident_name = st.selectbox(
        "Select Resident to Delete:", options=list(residents.keys())
    )
    selected_resident_id = residents[resident_name]

    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{resident_name}'?")
        if st.button("Delete User"):
            user_management.delete_record(selected_resident_id)

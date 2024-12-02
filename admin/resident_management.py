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
resident_manager.show_table()

# Fetch residents for dropdown selections
residents = resident_manager.fetch_options("Resident", "resident_id", "name")

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    with st.expander("Create Resident"):
        # Input fields for resident creation
        name = st.text_input(
            "Resident Name:",
            placeholder="Timmy",
        )
        date_of_birth = st.date_input("Date of Birth:", value=date(1970, 1, 1))
        gender = st.selectbox("Gender:", options=["Male", "Female"])
        contact_number = st.text_input(
            "Contact Number:",
            placeholder="011-2345678",
        )
        address = st.text_area(
            "Address:",
            placeholder="1 Jalan Damai, Kuala Lumpur",
        )
        email = st.text_input(
            "Email:",
            placeholder="emma@resident.com",
        )
        password = st.text_input(
            "Password:",
            type="password",
            placeholder="resident123",
        )

        if st.button("Add Resident"):
            try:
                # Create the resident record
                resident_manager.create_record(
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
    with st.expander("Update Resident"):
        # Select a resident by name
        resident_name = st.selectbox("Select Resident:", options=list(residents.keys()))

        # Fetch the selected resident's details
        selected_resident_id = residents[resident_name]
        st.write(f"Selected Resident ID: {selected_resident_id}")

        # Input fields for updatable data
        contact_number = st.text_input(
            "Contact Number:",
            placeholder="Optional",
        )
        address = st.text_area(
            "Address:",
            placeholder="Optional",
        )
        email = st.text_input(
            "Email:",
            placeholder="Optional",
        )
        password = st.text_input(
            "Password:",
            type="password",
            placeholder="Optional",
        )

        if st.button("Update Resident"):
            # Update the resident record
            resident_manager.update_record(
                selected_resident_id,
                contact_number=contact_number,
                address=address,
                email=email,
                password=password,
            )

elif option == "Delete":
    # Select a resident by name for deletion
    resident_name = st.selectbox(
        "Select Resident to Delete:", options=list(residents.keys())
    )
    selected_resident_id = residents[resident_name]

    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{resident_name}'?")
        if st.button("Delete Resident"):
            resident_manager.delete_record(selected_resident_id)

import streamlit as st
from management import Management
from datetime import date
from contact_number import ContactNumberInput

staff_manager = Management(table_name="staff")
contact_input = ContactNumberInput(
    label="Enter Contact Number", placeholder="01122233345"
)

# Check if user is logged in, if yes, display title
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title("Staff Management")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Display the table
staff_manager.show_table()

# Fetch existing staff options
staff_options = staff_manager.fetch_options("Staff", "staff_id", "name")

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    with st.expander("Create Staff"):
        # Gather inputs for creating a new staff member
        name = st.text_input(
            "Enter Name:",
            placeholder="Exp. Jasmine",
        )
        role = st.selectbox("Select Role:", options=["Doctor", "Nurse", "Caregiver"])

        contact_number = contact_input.render()
        username = st.text_input(
            "Enter Username:",
            placeholder="jasmine",
        )
        password = st.text_input(
            "Enter Password:",
            type="password",
            placeholder="staff123",
        )
        hire_date = st.date_input("Select Hire Date:", value=date.today())

        if st.button("Add Staff"):
            # Check if any required fields are empty
            if (
                not name
                or not role
                or not username
                or not password
                or not contact_number
                or not hire_date
            ):
                st.error("Please fill in all required fields.")
            else:
                staff_manager.create_record(
                    name=name,
                    role=role,
                    contact_number=contact_number,
                    username=username,
                    password=password,
                    hire_date=hire_date,
                )

elif option == "Update":
    with st.expander("Update Staff"):
        # Select staff by name for updating
        selected_name = st.selectbox(
            "Select Staff to Update:", options=list(staff_options.keys())
        )
        staff_id = staff_options[selected_name]

        # Gather inputs for updatable fields
        contact_number = contact_input.render()
        username = st.text_input(
            "New Username:",
            placeholder="Optional",
        )
        password = st.text_input(
            "New Password:",
            type="password",
            placeholder="Optional",
        )

        if st.button("Update Staff"):
            staff_manager.update_record(
                staff_id,
                contact_number=contact_number,
                username=username,
                password=password,
            )

elif option == "Delete":
    # Select staff by name for deletion
    selected_name = st.selectbox(
        "Select Staff to Delete:", options=list(staff_options.keys())
    )
    staff_id = staff_options[selected_name]

    # Confirmation expander
    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{selected_name}'?")
        if st.button("Delete Staff"):
            staff_manager.delete_staff(staff_id)
            staff_manager.clean_up_null_entries()

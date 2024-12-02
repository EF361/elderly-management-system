import streamlit as st
from management import Management
from datetime import date

staff_manager = Management(table_name="Staff")

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
        role = st.selectbox(
            "Select Role:", options=["Doctor", "Nurse", "Caregiver", "Other"]
        )
        if role == "Other":
            role = st.text_input(
                label="Enter Role: ",
                placeholder="Exp. Janitor",
            )

        contact_number = st.text_input(
            "Enter Contact Number:",
            placeholder="011-2345678",
        )
        email = st.text_input(
            "Enter Email:",
            placeholder="edward@staff.com",
        )
        password = st.text_input(
            "Enter Password:",
            type="password",
            placeholder="staff123",
        )
        hire_date = st.date_input("Select Hire Date:", value=date.today())

        if st.button("Add Staff"):
            staff_manager.create_record(
                name=name,
                role=role,
                contact_number=contact_number,
                email=email,
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
        contact_number = st.text_input(
            "New Contact Number:",
            placeholder="Optional",
        )
        email = st.text_input(
            "New Email:",
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
                email=email,
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
            staff_manager.delete_record(staff_id)

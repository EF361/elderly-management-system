import streamlit as st
from management import Management
from datetime import date

user_management = Management(table_name="Staff")

st.title(f"{user_management.table_name.capitalize()} Management")

# Display the table
user_management.show_table()

# Fetch existing staff options
staff_options = user_management.fetch_options("Staff", "staff_id", "name")

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    # Gather inputs for creating a new staff member
    name = st.text_input("Enter Name:")
    role = st.selectbox(
        "Select Role:", options=["Doctor", "Nurse", "Caregiver", "Other"]
    )
    if role == "Other":
        role = st.text_input(label="Enter Role: ", placeholder="Exp. Janitor")

    contact_number = st.text_input("Enter Contact Number:")
    email = st.text_input("Enter Email:")
    password = st.text_input("Enter Password:", type="password")
    hire_date = st.date_input("Select Hire Date:", value=date.today())

    if st.button("Add Staff"):
        user_management.create_record(
            name=name,
            role=role,
            contact_number=contact_number,
            email=email,
            password=password,
            hire_date=hire_date,
        )

elif option == "Update":
    # Select staff by name for updating
    selected_name = st.selectbox(
        "Select Staff to Update:", options=list(staff_options.keys())
    )
    staff_id = staff_options[selected_name]

    # Gather inputs for updatable fields
    contact_number = st.text_input("New Contact Number:")
    email = st.text_input("New Email:")
    password = st.text_input("New Password:", type="password")

    if st.button("Update Staff"):
        user_management.update_record(
            staff_id,
            contact_number=contact_number,
            email=email,
            password=password,
        )

elif option == "Delete":
    st.write("### Delete Staff")

    # Select staff by name for deletion
    selected_name = st.selectbox(
        "Select Staff to Delete:", options=list(staff_options.keys())
    )
    staff_id = staff_options[selected_name]

    # Confirmation expander
    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{selected_name}'?")
        if st.button("Delete Staff"):
            user_management.delete_record(staff_id)

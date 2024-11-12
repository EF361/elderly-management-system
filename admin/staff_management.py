import streamlit as st
from management import UserManagement

user_management = UserManagement(table_name="Staff")

st.title(f"{user_management.table_name.capitalize()} Management")

# Display the table
user_management.show_table()

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    # Gather inputs based on table fields
    inputs = {
        field: st.text_input(
            f"Enter {field.replace('_', ' ').capitalize()}:",
            type="password" if "password" in field else "default",
        )
        for field in user_management.fields["fields"]
    }
    if st.button("Add User"):
        user_management.create_record(**inputs)

elif option == "Update":
    user_id = st.number_input("Enter User ID to Update:", min_value=1, step=1)
    inputs = {
        field: st.text_input(
            f"New {field.replace('_', ' ').capitalize()}:",
            type="password" if "password" in field else "default",
        )
        for field in user_management.fields["fields"]
    }
    if st.button("Update User"):
        user_management.update_record(user_id, **inputs)

elif option == "Delete":
    user_id = st.number_input("Enter User ID to Delete:", min_value=1, step=1)
    if st.button("Delete User"):
        user_management.delete_record(user_id)

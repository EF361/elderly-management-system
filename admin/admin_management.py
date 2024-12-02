import streamlit as st
from management import Management

user_management = Management(table_name="Admin")

st.title(f"{user_management.table_name.capitalize()} Management")

# Check if user is logged in
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Display the table
user_management.show_table()

# Fetch existing admin options
admin_options = user_management.fetch_options("Admin", "admin_id", "name")

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    with st.expander("Create Admin"):
        # Gather inputs for creating a new admin
        name = st.text_input("Enter Name:")
        email = st.text_input("Enter Email:")
        password = st.text_input("Enter Password:", type="password")
        contact_number = st.text_input("Enter Contact Number:")

        if st.button("Add Admin"):
            user_management.create_record(
                name=name,
                email=email,
                password=password,
                contact_number=contact_number,
            )

elif option == "Update":
    with st.expander("Update Admin"):
        # Select admin by name for updating
        selected_name = st.selectbox(
            "Select Admin to Update:", options=list(admin_options.keys())
        )
        admin_id = admin_options[selected_name]

        # Gather inputs for updatable fields
        email = st.text_input("New Email:")
        password = st.text_input("New Password:", type="password")
        contact_number = st.text_input("New Contact Number:")

        if st.button("Update Admin"):
            user_management.update_record(
                admin_id,
                email=email,
                password=password,
                contact_number=contact_number,
            )

elif option == "Delete":
    st.write("### Delete Admin")

    # Select admin by name for deletion
    selected_name = st.selectbox(
        "Select Admin to Delete:", options=list(admin_options.keys())
    )
    admin_id = admin_options[selected_name]

    # Confirmation expander
    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{selected_name}'?")
        if st.button("Delete Admin"):
            user_management.delete_record(admin_id)

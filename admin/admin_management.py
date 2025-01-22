import streamlit as st
from management import Management
from contact_number import ContactNumberInput

admin_manager = Management(table_name="admin")
contact_input = ContactNumberInput(
    label="Enter Contact Number", placeholder="01122233345"
)
update_contact_input = ContactNumberInput(
    label="Enter Contact Number", placeholder="01122233345"
)
# Check if user is logged in, if yes, display title
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title(f"{admin_manager.table_name.capitalize()} Management")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Display the table
admin_manager.show_table()

# Fetch existing admin options
admin_options = admin_manager.fetch_options("Admin", "admin_id", "name")

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    with st.expander("Create Admin"):
        # Gather inputs for creating a new admin
        name = st.text_input(
            "Enter Name:",
            placeholder="Alexander",
        )
        username = st.text_input(
            "Enter Username:",
            placeholder="alex",
        )
        password = st.text_input(
            "Enter Password:",
            type="password",
            placeholder="admin123",
        )
        contact_number = contact_input.render()

        if st.button("Add Admin"):
            # Check if any required fields are empty
            if not name or not contact_number or not username or not password:
                st.error("Please fill in all required fields.")
            else:
                admin_manager.create_record(
                    name=name,
                    username=username,
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
        username = st.text_input(
            label="New Username:",
            placeholder="Optional",
        )
        password = st.text_input(
            label="New Password:",
            type="password",
            placeholder="Optional",
        )

        contact_number = update_contact_input.render()

        if st.button("Update Admin"):
            try:
                admin_manager.update_record(
                    admin_id,
                    username=username,
                    password=password,
                    contact_number=contact_number,
                )
            except Exception as e:
                st.error(f"There is an error: {e}")

elif option == "Delete":
    # Select admin by name for deletion
    selected_name = st.selectbox(
        "Select Admin to Delete:", options=list(admin_options.keys())
    )
    admin_id = admin_options[selected_name]

    # Assume `current_admin_name` holds the name of the currently logged-in admin
    current_admin_name = st.session_state["user_name"]  # Replace with your logic

    # Confirmation expander
    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{selected_name}'?")
        if st.button("Delete Admin"):
            if selected_name == current_admin_name:
                # Delete admin and log out
                admin_manager.delete_admin(admin_id)
                st.warning("You have deleted yourself. Logging out...")
                st.session_state.clear()  # Clear the session state to log out
                st.stop()  # Stops execution to prevent further actions
            else:
                # Delete the selected admin
                admin_manager.delete_admin(admin_id)
                st.success(f"Admin '{selected_name}' has been deleted.")

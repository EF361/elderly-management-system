import streamlit as st
from management import Management

admin_manager = Management(table_name="Admin")

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
            placeholder="alex@admin.com",
        )
        password = st.text_input(
            "Enter Password:",
            type="password",
            placeholder="admin123",
        )
        contact_number = st.text_input(
            "Enter Contact Number:",
            placeholder="011-1234567",
        )

        if st.button("Add Admin"):
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
        contact_number = st.text_input(
            label="New Contact Number:",
            placeholder="Optional",
        )

        if st.button("Update Admin"):
            admin_manager.update_record(
                admin_id,
                username=username,
                password=password,
                contact_number=contact_number,
            )

elif option == "Delete":
    # Select admin by name for deletion
    selected_name = st.selectbox(
        "Select Admin to Delete:", options=list(admin_options.keys())
    )
    admin_id = admin_options[selected_name]

    # Confirmation expander
    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{selected_name}'?")
        if st.button("Delete Admin"):
            admin_manager.delete_record(admin_id)

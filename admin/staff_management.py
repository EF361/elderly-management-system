import streamlit as st

st.title("Staff Management")

# Search bar
search = st.text_input("Search Staff...")

# Display Staff List
staff_data = [
    {"name": "John Doe", "role": "Nurse", "contact": "john.doe@example.com"},
    {"name": "Jane Smith", "role": "Doctor", "contact": "jane.smith@example.com"},
]
for i, staff in enumerate(staff_data):
    with st.expander(f"{staff['name']} ({staff['role']})"):
        st.write(f"Contact Info: {staff['contact']}")
        st.button("View Staff", key=f"view-button-staff-{i}")
        st.button("Edit Staff", key=f"edit-button-staff-{i}")
        st.button("Delete Staff", key=f"delete-button-staff-{i}")

# Add Staff Button
st.button("Add Staff", key="add-button-3")

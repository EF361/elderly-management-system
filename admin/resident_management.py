import streamlit as st

st.title("Resident Management")

# Search bar
search = st.text_input("Search residents by name or ID...")

# Display Resident List
st.write("## Resident List")
resident_data = [
    {"name": "John Doe", "room": 101, "history": "Diabetes"},
    {"name": "Jane Smith", "room": 102, "history": "Hypertension"},
    {"name": "Michael Johnson", "room": 103, "history": "Heart Disease"},
    {"name": "Sarah Wilson", "room": 104, "history": "Stroke"},
]
for i, resident in enumerate(resident_data):
    with st.expander(f"{resident['name']} (Room {resident['room']})"):
        st.write(f"Medical History: {resident['history']}")
        st.button("View Resident", key=f"view-button-resident-{i}")
        st.button("Edit Resident", key=f"edit-button-resident-{i}")
        st.button("Delete Resident", key=f"delete-button-resident-{i}")

# Add Resident Button
st.button("Add Resident", key="add-button-2")

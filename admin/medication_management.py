import streamlit as st

st.title("Medication Management")

# Search bar
st.text_input("Search Medications...")

# Medication List Table
st.write("## Medication Schedule")
medication_data = [
    {
        "resident": "John Doe",
        "med": "Aspirin",
        "dose": "100mg",
        "time": "9:00 AM",
        "status": "Administered",
    },
    {
        "resident": "Jane Smith",
        "med": "Ibuprofen",
        "dose": "200mg",
        "time": "10:00 AM",
        "status": "Pending",
    },
]
for i, med in enumerate(medication_data):
    with st.expander(f"{med['resident']} - {med['med']}"):
        st.write(f"Dose: {med['dose']}")
        st.write(f"Time: {med['time']}")
        st.write(f"Status: {med['status']}")
        st.button("View Medication", key=f"view-button-medication-{i}")
        st.button("Edit Medication", key=f"edit-button-medication-{i}")
        st.button("Delete Medication", key=f"delete-button-medication-{i}")

# Add Medication Button
st.button("Add Medication Medication", key="add-button-1")

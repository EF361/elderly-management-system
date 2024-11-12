import streamlit as st

st.title("Medication Management")

# Medication Table
st.subheader("Medication List")
medications = [
    {
        "Resident": "John Doe",
        "Medication": "Metformin",
        "Dosage": "500mg",
        "Time": "08:00 AM",
        "Status": "Pending",
    },
    {
        "Resident": "Jane Smith",
        "Medication": "Aspirin",
        "Dosage": "100mg",
        "Time": "09:00 AM",
        "Status": "Completed",
    },
]
st.table(medications)

# Add/Edit Buttons
if st.button("Add Medication Record"):
    st.write("Add medication record form would appear here.")

import streamlit as st

st.title("Resident Management")

# Search Bar
search_term = st.text_input("Search residents by name or ID...")
if st.button("Search"):
    st.write(f"Searching for: {search_term}")

# Resident Table
residents = [
    {
        "Name": "John Doe",
        "Age": 78,
        "Status": "Stable",
        "Conditions": "Diabetes, Hypertension",
    },
    {
        "Name": "Jane Smith",
        "Age": 82,
        "Status": "Needs Attention",
        "Conditions": "Heart Disease",
    },
]
st.table(residents)

# Actions
if st.button("Add Resident"):
    st.write("Add resident form would appear here.")

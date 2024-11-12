import streamlit as st

st.title("Shift Schedule")

# Shift Table
shifts = [
    {
        "Date": "10/08/2024",
        "Time": "08:00 AM - 04:00 PM",
        "Shift": "Morning Shift",
        "Status": "Confirmed",
    },
    {
        "Date": "11/08/2024",
        "Time": "04:00 PM - 12:00 AM",
        "Shift": "Evening Shift",
        "Status": "Pending",
    },
]
st.table(shifts)

# Manage Shifts Button
if st.button("Manage Shifts"):
    st.write("Manage shifts form would appear here.")

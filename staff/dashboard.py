import streamlit as st

# Dashboard Overview Content
st.title("Dashboard Overview")
st.subheader("Summary")
# Summary Cards
st.metric("Total Residents", "50")
st.metric("Staff on Duty", "12")
st.metric("Scheduled Medications", "25")
st.metric("Pending Tasks", "5")

st.subheader("Resident Overview")
st.metric("New Admissions", "2")
st.metric("Medical Alerts", "3")

st.subheader("Your Schedule")
st.metric("Today’s Shift", "9:00 AM - 5:00 PM")
st.write("Assigned Tasks: Administer Medications, Resident Care")

st.subheader("Medication Management")
st.metric("Medications Due", "25")
st.metric("Completed Medications", "15")

st.subheader("Notifications / Alerts")
st.write("- Upcoming Medication Schedule")
st.write("- Pending Tasks")

st.subheader("Recent Activity Feed")
st.write("- Admin updated resident information")
st.write("- Staff completed medication rounds")

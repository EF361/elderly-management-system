import streamlit as st

st.title("Admin Dashboard")
st.subheader("Overview")

# Summary Cards
st.write("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Residents", "50")
col2.metric("Staff on Duty", "12")
col3.metric("Scheduled Medications", "25")
col4.metric("Pending Tasks", "5")

# Notifications and Recent Activity
st.write("## Notifications/Alerts")
st.write("- Upcoming Medication Schedule")
st.write("- Pending Tasks")

st.write("## Recent Activity Feed")
st.write("- Admin updated resident information")
st.write("- Staff completed medication rounds")

import streamlit as st

st.title("Report Generation")

st.write("## Report Criteria")
date_range = st.date_input("Date Range")
resident = st.text_input("Resident")
staff = st.text_input("Staff")

if st.button("Generate Report"):
    st.write("Report Preview")
    st.write(
        "No report generated yet. Please select criteria and click 'Generate Report'."
    )

# Export options
st.write("## Export Options")
st.button("Export as PDF", key="export-button-1")
st.button("Export as Excel", key="export-button-2")
st.button("Print Report", key="export-button-3")
st.button("Download Report", key="export-button-4")

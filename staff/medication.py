import streamlit as st
from datetime import date
from management import UserManagement

# Initialize UserManagement for the Medical_Record table
medical_record_management = UserManagement(table_name="Medical_Record")

# Check if user is logged in and display title
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title("Medical Record Management")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Display the medical records table
medical_record_management.show_table()

# Fetch residents and medicines for dropdown selections
residents = medical_record_management.fetch_options("Resident", "resident_id", "name")
medicines = medical_record_management.fetch_options(
    "Medicine", "medicine_id", "medicine_name"
)
staff = medical_record_management.fetch_options("Staff", "staff_id", "name")

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    st.write("### Add New Medical Record")

    # Input fields for medical record creation
    resident_name = st.selectbox("Select Resident:", options=list(residents.keys()))
    selected_resident_id = residents[resident_name]

    diagnosis = st.text_area("Diagnosis:")
    treatment = st.text_area("Treatment:")
    medicine_name = st.selectbox("Select Medicine:", options=list(medicines.keys()))
    selected_medicine_id = medicines[medicine_name]

    doctor_name = st.session_state["user_name"]
    selected_doctor_id = staff[doctor_name]

    record_date = st.date_input("Record Date:", value=date.today())

    if st.button("Add Medical Record"):
        try:
            # Create the medical record
            medical_record_management.create_record(
                resident_id=selected_resident_id,
                diagnosis=diagnosis,
                treatment=treatment,
                doctor_id=selected_doctor_id,  # Maps to staff_id
                record_date=record_date,
                medicine_id=selected_medicine_id,
            )
        except Exception as e:
            st.error(f"There was an error: {e}")

elif option == "Update":
    st.write("### Update Medical Record")

    # Fetch existing medical records for selection
    medical_records = medical_record_management.fetch_options(
        "Medical_Record", "record_id", "diagnosis"
    )
    if not medical_records:
        st.info("No records available to update.")
    else:
        record_to_update = st.selectbox(
            "Select Record to Update:", options=list(medical_records.keys())
        )
        selected_record_id = medical_records[record_to_update]

        # Input fields for updatable data
        diagnosis = st.text_area("Diagnosis (leave blank to keep current):")
        treatment = st.text_area("Treatment (leave blank to keep current):")
        medicine_name = st.selectbox("Select Medicine:", options=list(medicines.keys()))
        selected_medicine_id = medicines[medicine_name]

        doctor_name = st.session_state["user_name"]
        selected_doctor_id = staff[doctor_name]

        record_date = st.date_input("Record Date:", value=date.today())

        if st.button("Update Medical Record"):
            try:
                # Update the medical record
                medical_record_management.update_record(
                    selected_record_id,
                    diagnosis=diagnosis,
                    treatment=treatment,
                    doctor_id=selected_doctor_id,  # Maps to staff_id
                    record_date=record_date,
                    medicine_id=selected_medicine_id,
                )
            except Exception as e:
                st.error(f"There was an error: {e}")

elif option == "Delete":
    st.write("### Delete Medical Record")

    # Fetch existing medical records for deletion
    medical_records = medical_record_management.fetch_options(
        "Medical_Record", "record_id", "diagnosis"
    )
    if not medical_records:
        st.info("No records available to delete.")
    else:
        record_to_delete = st.selectbox(
            "Select Record to Delete:", options=list(medical_records.keys())
        )
        selected_record_id = medical_records[record_to_delete]

        with st.expander("Confirm Deletion"):
            st.write(
                f"Are you sure you want to delete the record '{record_to_delete}'?"
            )
            if st.button("Delete Record"):
                try:
                    medical_record_management.delete_record(selected_record_id)
                except Exception as e:
                    st.error(f"There was an error: {e}")

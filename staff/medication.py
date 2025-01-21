import streamlit as st
from datetime import date
from sqlalchemy import create_engine, text
from management import Management

# Database connection setup (adjust with your actual database URL)
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

# Check if user is logged in and display title
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]  # The staff name is stored here
    st.title("Medical Record")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Fetch user role from the database based on the staff name stored in session_state
user_role = None
try:
    with engine.connect() as connection:
        query = text("SELECT role FROM Staff WHERE name = :name")
        result = (
            connection.execute(query, {"name": user_name}).mappings().first()
        )  # Use .mappings() to get a dictionary

        if result:
            user_role = result["role"]  # Access role as a dictionary
        else:
            st.error("User role not found in the database.")
            st.stop()
except Exception as e:
    st.error(f"Error fetching user role: {e}")
    st.stop()

# Display the medical records table
medical_record_management = Management(table_name="Medical_Record")
medical_record_management.show_table_schedule()

# Fetch residents and medicines for dropdown selections
residents = medical_record_management.fetch_options("Resident", "resident_id", "name")
medicines = medical_record_management.fetch_options(
    "Medicine", "medicine_id", "medicine_name"
)
staff = medical_record_management.fetch_options("Staff", "staff_id", "name")

# Select operation
if user_role == "Doctor":
    option = st.selectbox(
        label="Select an operation",
        options=["Create", "Update", "Delete"],
    )
else:
    option = "View"  # For non-doctor roles, set the option to View only

# Create medical record (for Doctors only)
if option == "Create" and user_role == "Doctor":
    with st.expander("Create Medical Record"):
        # Input fields for medical record creation
        resident_name = st.selectbox("Select Resident:", options=list(residents.keys()))
        selected_resident_id = residents.get(resident_name)

        diagnosis = st.text_area("Diagnosis:", placeholder="Diabetes Mellitus")
        treatment = st.text_area(
            "Treatment:", placeholder="Diet control, medication, insulin therapy"
        )
        medicine_name = st.selectbox("Select Medicine:", options=list(medicines.keys()))
        selected_medicine_id = medicines.get(medicine_name)

        doctor_name = st.session_state["user_name"]
        selected_doctor_id = staff.get(doctor_name)

        record_date = st.date_input("Record Date:", value=date.today())

        # Validation: Ensure no field is left empty
        if st.button("Add Medical Record"):
            if not resident_name or not diagnosis or not treatment or not medicine_name:
                st.error("All fields must be filled in. Please provide valid inputs.")
            else:
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

# Update medical record (for Doctors only)
elif option == "Update" and user_role == "Doctor":
    with st.expander("Update Medicine"):
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
            diagnosis = st.text_area("Diagnosis:", placeholder="Optional")
            treatment = st.text_area("Treatment:", placeholder="Optional")
            medicine_name = st.selectbox(
                "Select Medicine:", options=list(medicines.keys())
            )
            selected_medicine_id = medicines.get(medicine_name)

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

# Delete medical record (for Doctors only)
elif option == "Delete" and user_role == "Doctor":
    # Fetch existing medical records for deletion with resident name and diagnosis
    query = """
    SELECT mr.record_id, r.name AS resident_name, mr.diagnosis
    FROM Medical_Record mr
    LEFT JOIN Resident r ON mr.resident_id = r.resident_id;
    """
    try:
        # Fetch the medical records with resident name and diagnosis
        records = medical_record_management.conn.query(query, ttl=0)

        # Create a list of display options combining the resident name and diagnosis
        records_to_display = {
            f"{row['resident_name']} - {row['diagnosis']}": row["record_id"]
            for _, row in records.iterrows()
        }

        if not records_to_display:
            st.info("No records available to delete.")
        else:
            record_to_delete = st.selectbox(
                "Select Record to Delete:", options=list(records_to_display.keys())
            )
            selected_record_id = records_to_display[record_to_delete]

            with st.expander("Confirm Deletion"):
                st.write(
                    f"Are you sure you want to delete the record for '{record_to_delete}'?"
                )
                if st.button("Delete Record"):
                    try:
                        medical_record_management.delete_record(selected_record_id)
                    except Exception as e:
                        st.error(f"There was an error: {e}")
    except Exception as e:
        st.error(f"Error fetching medical records: {e}")

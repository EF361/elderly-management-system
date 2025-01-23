import streamlit as st
from datetime import date
from sqlalchemy import create_engine, text
from management import Management

DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title("Medical Record")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

user_role = None
try:
    with engine.connect() as connection:
        query = text("SELECT role FROM Staff WHERE name = :name")
        result = connection.execute(query, {"name": user_name}).mappings().first()

        if result:
            user_role = result["role"]
        else:
            st.error("User role not found in the database.")
            st.stop()
except Exception as e:
    st.error(f"Error fetching user role: {e}")
    st.stop()

medical_record_management = Management(table_name="Medical_Record")
medical_record_management.show_table_schedule()

residents = medical_record_management.fetch_options("Resident", "resident_id", "name")
medicines = medical_record_management.fetch_options(
    "Medicine", "medicine_id", "medicine_name"
)
staff = medical_record_management.fetch_options("Staff", "staff_id", "name")

if user_role == "Doctor":
    option = st.selectbox(
        label="Select an operation",
        options=["Create", "Update", "Delete"],
    )
else:
    option = "View"


if option == "Create" and user_role == "Doctor":
    with st.expander("Create Medical Record"):
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

        record_date = st.date_input(
            "Record Date:",
            value=date.today(),
            min_value=date.today(),
            max_value=date.today(),
        )

        if st.button("Add Medical Record"):
            if not resident_name or not diagnosis or not treatment or not medicine_name:
                st.error("All fields must be filled in. Please provide valid inputs.")
            else:
                try:
                    medical_record_management.create_record(
                        resident_id=selected_resident_id,
                        diagnosis=diagnosis,
                        treatment=treatment,
                        doctor_id=selected_doctor_id,
                        record_date=record_date,
                        medicine_id=selected_medicine_id,
                    )
                except Exception as e:
                    st.error(f"There was an error: {e}")

elif option == "Update" and user_role == "Doctor":
    with st.expander("Update Medicine"):
        query = """
        SELECT mr.record_id, r.name AS resident_name, mr.diagnosis
        FROM Medical_Record mr
        LEFT JOIN Resident r ON mr.resident_id = r.resident_id;
        """
        try:
            records = medical_record_management.conn.query(query, ttl=0)

            records_to_display = {
                f"{row['resident_name']} - {row['diagnosis']}": row["record_id"]
                for _, row in records.iterrows()
            }

            if not records_to_display:
                st.info("No records available to update.")
            else:
                record_to_update = st.selectbox(
                    "Select Record to Update:", options=list(records_to_display.keys())
                )
                selected_record_id = records_to_display[record_to_update]

                diagnosis = st.text_area("Diagnosis:", placeholder="Optional")
                treatment = st.text_area("Treatment:", placeholder="Optional")
                medicine_name = st.selectbox(
                    "Select Medicine:", options=list(medicines.keys())
                )
                selected_medicine_id = medicines.get(medicine_name)

                doctor_name = st.session_state["user_name"]
                selected_doctor_id = staff[doctor_name]

                record_date = st.date_input(
                    "Record Date:",
                    value=date.today(),
                    min_value=date.today(),
                    max_value=date.today(),
                )

                if st.button("Update Medical Record"):
                    try:
                        medical_record_management.update_record(
                            selected_record_id,
                            diagnosis=diagnosis,
                            treatment=treatment,
                            doctor_id=selected_doctor_id,
                            record_date=record_date,
                            medicine_id=selected_medicine_id,
                        )
                    except Exception as e:
                        st.error(f"There was an error: {e}")
        except Exception as e:
            st.error(f"Error fetching medical records: {e}")

elif option == "Delete" and user_role == "Doctor":
    query = """
    SELECT mr.record_id, r.name AS resident_name, mr.diagnosis
    FROM Medical_Record mr
    LEFT JOIN Resident r ON mr.resident_id = r.resident_id;
    """
    try:
        records = medical_record_management.conn.query(query, ttl=0)

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
                        medical_record_management.delete_record(
                            table_name="medical_record",
                            primary_key_column="record_id",
                            user_id=selected_record_id,
                        )
                    except Exception as e:
                        st.error(f"There was an error: {e}")
    except Exception as e:
        st.error(f"Error fetching medical records: {e}")

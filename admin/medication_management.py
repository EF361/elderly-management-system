import streamlit as st
from management import UserManagement
from datetime import date


# Define MedicationManagement class
class MedicationManagement(UserManagement):
    def __init__(self):
        super().__init__("Medication")
        self.fields = {
            "primary_key": "medication_id",
            "fields": [
                "resident_id",
                "medication_name",
                "dosage",
                "frequency",
                "start_date",
                "end_date",
                "prescribed_by",
            ],
        }
        # Fetch resident and staff names for dropdowns
        self.residents = self.fetch_options("Resident", "resident_id", "resident_name")
        self.staff = self.fetch_options("Staff", "staff_id", "staff_name")

    def fetch_options(self, table_name, id_field, name_field):
        """Fetch ID and Name pairs for dropdown selections."""
        query = f"SELECT {id_field}, {name_field} FROM {table_name}"
        result = self.conn.query(query)

        # Adjust the itertuples call to use index=False and access columns with underscores
        return {
            getattr(row, name_field): getattr(row, id_field)
            for row in result.itertuples(index=False)
        }

    def show_table(self):
        """Display all medications in a table."""
        query = """
        SELECT m.medication_id, r.resident_name, m.medication_name, m.dosage,
               m.frequency, m.start_date, m.end_date, s.staff_name AS prescribed_by
        FROM Medication m
        JOIN Resident r ON m.resident_id = r.resident_id
        LEFT JOIN Staff s ON m.prescribed_by = s.staff_id;
        """
        df = self.conn.query(query, ttl=0)
        st.dataframe(df, use_container_width=True)


# Initialize MedicationManagement
med_manager = MedicationManagement()
st.title("Medication Management")

# Display table of medications
med_manager.show_table()

# Select CRUD operation
operation = st.selectbox("Select Operation", ["Create", "Update", "Delete"])

if operation == "Create":
    st.write("### Add New Medication")
    resident = st.selectbox("Resident", options=list(med_manager.residents.keys()))
    medication_name = st.text_input("Medication Name")
    dosage = st.text_input("Dosage")
    frequency = st.text_input("Frequency")
    start_date = st.date_input("Start Date", value=date.today())
    end_date = st.date_input("End Date", value=None)
    prescriber = st.selectbox("Prescribed By", options=list(med_manager.staff.keys()))

    if st.button("Add Medication"):
        med_manager.create_record(
            resident_id=med_manager.residents[resident],
            medication_name=medication_name,
            dosage=dosage,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
            prescribed_by=med_manager.staff[prescriber],
        )

elif operation == "Update":
    st.write("### Update Medication")
    medication_id = st.number_input("Medication ID to Update", min_value=1, step=1)
    resident = st.selectbox("Resident", options=list(med_manager.residents.keys()))
    medication_name = st.text_input("Medication Name", value="")
    dosage = st.text_input("Dosage", value="")
    frequency = st.text_input("Frequency", value="")
    start_date = st.date_input("Start Date", value=date.today())
    end_date = st.date_input("End Date", value=None)
    prescriber = st.selectbox("Prescribed By", options=list(med_manager.staff.keys()))

    if st.button("Update Medication"):
        med_manager.update_record(
            medication_id,
            resident_id=med_manager.residents[resident],
            medication_name=medication_name,
            dosage=dosage,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
            prescribed_by=med_manager.staff[prescriber],
        )

elif operation == "Delete":
    st.write("### Delete Medication")
    medication_id = st.number_input("Medication ID to Delete", min_value=1, step=1)

    if st.button("Delete Medication"):
        med_manager.delete_record(medication_id)

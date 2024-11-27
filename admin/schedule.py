import streamlit as st
from management import UserManagement
from datetime import datetime, date, time


# Define ScheduleManagement class
class ScheduleManagement(UserManagement):
    def __init__(self):
        super().__init__("Schedule")
        self.fields = {
            "primary_key": "schedule_id",
            "fields": [
                "resident_id",
                "staff_id",
                "event_type",
                "event_date",
                "start_time",
                "end_time",
                "description",
            ],
        }
        # Fetch resident and staff names for dropdowns
        self.residents = self.fetch_options("Resident", "resident_id", "name")
        self.staff = self.fetch_options("Staff", "staff_id", "name")

    def fetch_options(self, table_name, id_field, name_field):
        """Fetch ID and Name pairs for dropdown selections."""
        query = f"SELECT {id_field}, {name_field} FROM {table_name}"
        result = self.conn.query(query)

        return {
            getattr(row, name_field): getattr(row, id_field)
            for row in result.itertuples(index=False)
        }

    def show_table(self):
        """Display all schedules in a table."""
        query = """
        SELECT s.schedule_id, r.name AS resident_name, t.name AS staff_name, s.event_type, 
               s.event_date, s.start_time, s.end_time, s.description
        FROM Schedule s
        JOIN Resident r ON s.resident_id = r.resident_id
        LEFT JOIN Staff t ON s.staff_id = t.staff_id
        ORDER BY s.event_date, s.start_time;
        """
        df = self.conn.query(query, ttl=0)
        st.dataframe(df, use_container_width=True)


# Initialize ScheduleManagement
schedule_manager = ScheduleManagement()
st.title("Schedule Management")

# Display table of schedules
schedule_manager.show_table()

# Select CRUD operation
operation = st.selectbox("Select Operation", ["Create", "Update", "Delete"])

if operation == "Create":
    st.write("### Add New Schedule")
    resident = st.selectbox("Resident", options=list(schedule_manager.residents.keys()))
    staff = st.selectbox("Staff", options=list(schedule_manager.staff.keys()))
    event_type = st.text_input("Event Type")
    event_date = st.date_input("Event Date", value=date.today())
    start_time = st.time_input("Start Time", value=datetime.now().time())
    end_time = st.time_input("End Time", value=datetime.now().time())
    description = st.text_area("Description")

    if st.button("Add Schedule"):
        schedule_manager.create_record(
            resident_id=schedule_manager.residents[resident],
            staff_id=schedule_manager.staff[staff],
            event_type=event_type,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            description=description,
        )

elif operation == "Update":
    st.write("### Update Schedule")
    schedule_id = st.number_input("Schedule ID to Update", min_value=1, step=1)
    resident = st.selectbox("Resident", options=list(schedule_manager.residents.keys()))
    staff = st.selectbox("Staff", options=list(schedule_manager.staff.keys()))
    event_type = st.text_input("Event Type", value="")
    event_date = st.date_input("Event Date", value=date.today())
    start_time = st.time_input("Start Time", value=datetime.now().time())
    end_time = st.time_input("End Time", value=datetime.now().time())
    description = st.text_area("Description", value="")

    if st.button("Update Schedule"):
        schedule_manager.update_record(
            schedule_id,
            resident_id=schedule_manager.residents[resident],
            staff_id=schedule_manager.staff[staff],
            event_type=event_type,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            description=description,
        )

elif operation == "Delete":
    st.write("### Delete Schedule")
    schedule_id = st.number_input("Schedule ID to Delete", min_value=1, step=1)

    if st.button("Delete Schedule"):
        schedule_manager.delete_record(schedule_id)
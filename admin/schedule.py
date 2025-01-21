import streamlit as st
from management import Management
from datetime import datetime, date, time, timedelta  # noqa: F401


class ScheduleManagement(Management):
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
        self.staff_roles = self.fetch_staff_roles()  # Fetch roles of staff
        self.schedules = self.fetch_schedule_options()

        print(f"Schedules fetched: {self.schedules}")

    def fetch_options(self, table_name, id_field, name_field):
        """Fetch ID and Name pairs for dropdown selections."""
        query = f"SELECT {id_field}, {name_field} FROM {table_name}"
        result = self.conn.query(query)

        return {
            getattr(row, name_field): getattr(row, id_field)
            for row in result.itertuples(index=False)
        }

    def fetch_staff_roles(self):
        """Fetch staff roles (e.g., doctor, nurse) for each staff member."""
        query = "SELECT staff_id, role FROM Staff"
        result = self.conn.query(query)
        return {row.staff_id: row.role for row in result.itertuples(index=False)}

    def fetch_schedule_options(self):
        query = """
        SELECT s.schedule_id, 
            COALESCE(r.name, 'Unknown') AS resident_name, 
            s.description, 
            s.event_date
        FROM Schedule s
        LEFT JOIN Resident r ON s.resident_id = r.resident_id
        ORDER BY s.event_date, s.start_time;
        """
        result = self.conn.query(query)

        # Check if the result is empty
        if result.empty:
            st.error("No schedules found.")
            return {}

        formatted_schedules = {
            f"{row.resident_name} - {row.description} on {row.event_date}": row.schedule_id
            for row in result.itertuples(index=False)
        }

        return formatted_schedules

    def show_table_schedule(self):
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
table_name = "schedule"

# Check if user is logged in, if yes, display title
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title("Schedule Management")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()


# Display table of schedules
schedule_manager.show_table_schedule()

# Select CRUD operation
operation = st.selectbox("Select Operation", ["Create", "Update", "Delete"])

if operation == "Create":
    with st.expander("Create Schedule"):
        resident = st.selectbox(
            "Resident", options=list(schedule_manager.residents.keys())
        )
        staff_name = st.selectbox("Staff", options=list(schedule_manager.staff.keys()))
        staff_id = schedule_manager.staff[staff_name]

        # Fetch staff roles and ensure they are in the correct format (e.g., "Doctor")
        staff_role = schedule_manager.staff_roles.get(staff_id, "Unknown").lower()

        # Event Type: Restrict selection based on staff role
        event_type_options = [
            "Social Activity",
            "Other",
        ]  # Default options
        if staff_role == "doctor":
            event_type_options.insert(
                0, "Medical Appointment"
            )  # Add Medical Appointment for doctors only

        event_type = st.selectbox("Event Type", options=event_type_options)

        # Event Date - restrict to today or future
        event_date = st.date_input(
            "Event Date", value=date.today(), min_value=date.today()
        )

        # Start Time - restrict to an hour later than the current time
        current_time = datetime.now()
        start_time_min = (current_time + timedelta(hours=1)).time()
        start_time = st.time_input("Start Time", value=start_time_min)

        # End Time - make the end time depend on start time
        end_time = st.time_input(
            "End Time",
            value=(
                datetime.combine(date.today(), start_time) + timedelta(hours=1)
            ).time(),
        )

        description = st.text_area(
            "Description",
            placeholder="Exp. Asthma follow-up",
        )

        if st.button("Add Schedule"):
            # Validate inputs
            if event_type == "Medical Appointment" and staff_role != "doctor":
                st.error("Only doctors can schedule medical appointments.")
            elif not description.strip():
                st.error("Description cannot be empty.")
            elif not start_time or not end_time:
                st.error("Start time and end time cannot be empty.")
            elif start_time >= end_time:
                st.error("Start time must be before end time.")
            else:
                schedule_manager.create_record(
                    resident_id=schedule_manager.residents[resident],
                    staff_id=staff_id,
                    event_type=event_type,
                    event_date=event_date,
                    start_time=start_time,
                    end_time=end_time,
                    description=description,
                )

if operation == "Update":
    with st.expander("Update Schedule"):
        # Select a schedule to update (auto-select should work)
        selected_schedule = st.selectbox(
            "Select Schedule to Update:",
            options=list(schedule_manager.schedules.keys()),
            key="selected_schedule_update",  # Unique key
            index=0,  # Automatically select the first item (if it exists)
        )

        if selected_schedule:
            schedule_id = schedule_manager.schedules.get(selected_schedule)

            # Fetch the selected schedule's details to populate the fields
            st.write(f"Selected Schedule ID: {schedule_id}")

            # Fetch and display staff details
            staff_name = st.selectbox(
                "Staff",
                options=list(schedule_manager.staff.keys()),
                index=0,  # Optionally auto-select the first staff
            )
            staff_id = schedule_manager.staff[staff_name]

            # Get the staff role
            staff_role = schedule_manager.staff_roles.get(staff_id, "Unknown").lower()

            # Event Type: Restrict selection based on staff role
            event_type_options = ["Social Activity", "Other"]  # Default options
            if staff_role == "doctor":
                event_type_options.insert(
                    0, "Medical Appointment"
                )  # Add Medical Appointment for doctors only

            event_type = st.selectbox("Event Type", options=event_type_options)

            # Event Date - restrict to today or future
            event_date = st.date_input(
                "Event Date", value=date.today(), min_value=date.today()
            )

            # Start Time - restrict to an hour later than the current time
            current_time = datetime.now()
            start_time_min = (current_time + timedelta(hours=1)).time()
            start_time = st.time_input("Start Time", value=start_time_min)

            # End Time - make the end time depend on start time
            end_time = st.time_input(
                "End Time",
                value=(
                    datetime.combine(date.today(), start_time) + timedelta(hours=1)
                ).time(),
            )

            description = st.text_area("Description", placeholder="Optional")

            if st.button("Update Schedule"):
                # Validate inputs
                if event_type == "Medical Appointment" and staff_role != "doctor":
                    st.error("Only doctors can update medical appointments.")
                elif not start_time or not end_time:
                    st.error("Start time and end time cannot be empty.")
                elif start_time >= end_time:
                    st.error("Start time must be before end time.")
                else:
                    schedule_manager.update_record(
                        schedule_id,
                        staff_id=staff_id,
                        event_type=event_type,
                        event_date=event_date,
                        start_time=start_time,
                        end_time=end_time,
                        description=description,
                    )
        else:
            st.error("Please select a valid schedule.")


elif operation == "Delete":
    selected_schedule = st.selectbox(
        "Select Schedule to Delete:",
        options=list(schedule_manager.schedules.keys()),
    )
    schedule_id = schedule_manager.schedules[selected_schedule]

    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{selected_schedule}'?")
        if st.button("Delete Schedule"):
            schedule_manager.delete_record(table_name, schedule_id)

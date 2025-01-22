import streamlit as st
from datetime import date, timedelta, time
from sqlalchemy import create_engine, text
from management import Management

# Database connection setup (adjust with your actual database URL)
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/elderlymanagement"
engine = create_engine(DATABASE_URL)

# Check if user is logged in and display title
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title("Schedule Management")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

# Display the schedule table
schedule_management = Management(table_name="Schedule")
schedule_management.show_table()
tomorrow = date.today() + timedelta(days=1)

# Fetch residents and staff for dropdown selections
residents = schedule_management.fetch_options("Resident", "resident_id", "name")
staff = schedule_management.fetch_options("Staff", "staff_id", "name")

option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)


# Create schedule (for Managers only)
if option == "Create":
    with st.expander("Create Schedule"):
        # Input fields for schedule creation
        resident_name = st.selectbox("Select Resident:", options=list(residents.keys()))
        selected_resident_id = residents.get(resident_name)

        staff_name = st.selectbox("Select Staff:", options=list(staff.keys()))
        selected_staff_id = staff.get(staff_name)

        # Fetch the role of the selected staff from the database
        try:
            with engine.connect() as connection:
                query = text("SELECT role FROM Staff WHERE staff_id = :staff_id")
                result = (
                    connection.execute(query, {"staff_id": selected_staff_id})
                    .mappings()
                    .first()
                )

            staff_role = result["role"] if result else None
        except Exception as e:
            st.error(f"Error fetching staff role: {e}")
            staff_role = None

        # Determine allowed event types based on staff role
        if staff_role in ["Doctor"]:
            event_type = st.selectbox(
                "Event Type:",
                ["Medical Appointment", "Social Activity", "Other"],
            )
        else:
            event_type = st.selectbox(
                "Event Type:",
                ["Social Activity", "Other"],
            )

        event_date = st.date_input(
            "Event Date:",
            value=tomorrow,
            min_value=tomorrow,
        )
        start_time = st.time_input("Start Time:", value=time(9, 0))
        end_time = st.time_input("End Time:", value=time(10, 0))
        description = st.text_area("Description:", placeholder="Enter event details...")

        if st.button("Add Schedule"):
            if not resident_name or not staff_name or not event_type or not description:
                st.error("All fields must be filled in. Please provide valid inputs.")
            elif start_time >= end_time:
                st.error("End time must greater than Start time.")
            else:
                try:
                    schedule_management.create_record(
                        resident_id=selected_resident_id,
                        staff_id=selected_staff_id,
                        event_type=event_type,
                        event_date=event_date,
                        start_time=start_time,
                        end_time=end_time,
                        description=description,
                    )
                except Exception as e:
                    st.error(f"There was an error: {e}")


# Update schedule (for Managers only)
elif option == "Update":
    with st.expander("Update Schedule"):
        query = """
        SELECT sch.schedule_id, r.name AS resident_name, sch.description, sch.event_date
        FROM schedule sch
        LEFT JOIN Resident r ON sch.resident_id = r.resident_id;
        """
        try:
            # Fetch the medical records with resident name and diagnosis
            records = schedule_management.conn.query(query, ttl=0)

            # Create a list of display options combining the resident name and diagnosis
            records_to_display = {
                f"{row['resident_name']} - {row['description']} - {row['event_date']}": row[
                    "schedule_id"
                ]
                for _, row in records.iterrows()
            }

            if not records_to_display:
                st.info("No records available to delete.")
            else:
                schedule_to_update = st.selectbox(
                    "Select Schedule to Update:",
                    options=list(records_to_display.keys()),
                )
                selected_schedule_id = records_to_display[schedule_to_update]

                event_date = st.date_input(
                    "Event Date:",
                    value=tomorrow,
                    min_value=tomorrow,
                )
                start_time = st.time_input("Start Time:", value=time(9, 0))
                end_time = st.time_input("End Time:", value=time(10, 0))
                description = st.text_area("Description:", placeholder="Optional")

                if st.button("Update Schedule"):
                    if start_time >= end_time:
                        st.error("End time must larger than start time.")
                    else:
                        try:
                            schedule_management.update_record(
                                selected_schedule_id,
                                event_date=event_date,
                                start_time=start_time,
                                end_time=end_time,
                                description=description,
                            )
                        except Exception as e:
                            st.error(f"There was an error: {e}")
        except Exception as e:
            st.error(f"Error fetching schedule: {e}")

# Delete schedule (for Managers only)
elif option == "Delete":
    with st.expander("Delete Schedule"):
        query = """
        SELECT sch.schedule_id, r.name AS resident_name, sch.description, sch.event_date
        FROM schedule sch
        LEFT JOIN Resident r ON sch.resident_id = r.resident_id;
        """
        try:
            # Fetch the medical records with resident name and diagnosis
            records = schedule_management.conn.query(query, ttl=0)

            # Create a list of display options combining the resident name and diagnosis
            records_to_display = {
                f"{row['resident_name']} - {row['description']} - {row['event_date']}": row[
                    "schedule_id"
                ]
                for _, row in records.iterrows()
            }

            if not records_to_display:
                st.info("No records available to delete.")

            else:
                schedule_to_delete = st.selectbox(
                    "Select Schedule to Delete:",
                    options=list(records_to_display.keys()),
                )
                selected_schedule_id = records_to_display[schedule_to_delete]

                if st.button("Delete Schedule"):
                    try:
                        schedule_management.delete_record(
                            "schedule", "schedule_id", selected_schedule_id
                        )
                    except Exception as e:
                        st.error(f"There was an error: {e}")
        except Exception as e:
            st.error(f"Error fetching schedule: {e}")

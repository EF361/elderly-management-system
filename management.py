import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError


# Management class
class Management:
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = st.connection("postgresql", type="sql")
        self.engine = create_engine(
            "postgresql://postgres:12345@localhost:5432/elderlymanagement"
        )

        self.fields = self.get_table_fields()

    def get_table_fields(self):
        """Define fields for each table based on the schema."""
        table_fields = {
            "admin": {
                "primary_key": "admin_id",
                "fields": ["name", "username", "password", "contact_number"],
            },
            "resident": {
                "primary_key": "resident_id",
                "fields": [
                    "name",
                    "date_of_birth",
                    "gender",
                    "contact_number",
                    "address",
                    "username",
                    "password",
                ],
            },
            "staff": {  # Ensure this is defined correctly
                "primary_key": "staff_id",
                "fields": [
                    "name",
                    "role",
                    "contact_number",
                    "username",
                    "password",
                    "hire_date",
                ],
            },
            "medical_record": {
                "primary_key": "record_id",
                "fields": [
                    "resident_id",
                    "diagnosis",
                    "treatment",
                    "doctor_id",
                    "record_date",
                    "medicine_id",
                ],
            },
            "schedule": {
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
            },
        }
        return table_fields.get(self.table_name.lower(), {})

    def show_table_schedule(self):
        """Show all records in the specified user table with names instead of IDs."""
        # Query to join the Medical_Record table with Resident, Staff, and Medicine tables
        query = f"""
        SELECT mr.record_id, r.name AS resident_name, mr.diagnosis, mr.treatment, 
            s.name AS doctor_name, mr.record_date, m.medicine_name
        FROM {self.table_name} mr
        LEFT JOIN Resident r ON mr.resident_id = r.resident_id
        LEFT JOIN Staff s ON mr.doctor_id = s.staff_id
        LEFT JOIN Medicine m ON mr.medicine_id = m.medicine_id;
        """

        try:
            # Execute the query
            result = self.conn.query(query, ttl=0)

            # Display the result as a DataFrame
            st.dataframe(result, use_container_width=True)
        except Exception as e:
            st.error(f"Error fetching medical records: {e}")

    def show_table(self):  # noqa: F811
        """Show all records dynamically for each table."""
        if self.table_name.lower() == "resident":
            query = f"""
                SELECT resident_id, name, date_of_birth, gender, contact_number, address, username, password
                FROM {self.table_name};
            """
        elif self.table_name.lower() == "staff":
            query = f"""
                SELECT staff_id, name, role, contact_number, username, hire_date, password
                FROM {self.table_name};
            """
        elif self.table_name.lower() == "admin":
            query = f"""
                SELECT admin_id, name, username, contact_number, password
                FROM {self.table_name};
            """
        elif self.table_name.lower() == "resident_emergency_contacts":
            query = """
            SELECT rec.contact_id, r.name AS resident_name, rec.contact_name, rec.relationship, rec.contact_number
            FROM Resident_Emergency_Contacts rec
            LEFT JOIN Resident r ON rec.resident_id = r.resident_id;
            """
        elif self.table_name.lower() == "schedule":
            query = """
            SELECT sch.schedule_id, r.name AS resident_name, s.name AS staff_name, sch.event_type, sch.start_time, sch.end_time, sch.description
            FROM schedule sch
            LEFT JOIN Resident r ON sch.resident_id = r.resident_id
            LEFT JOIN Staff s ON sch.staff_id = s.staff_id;
            """
        try:
            result = self.conn.query(query, ttl=0)
            st.dataframe(result, use_container_width=True)
        except Exception as e:
            st.error(f"Error fetching {self.table_name} data: {e}")

    def create_record(self, **kwargs):
        """Insert a new record into the specified user table."""
        if not self.fields:
            st.error(f"Table '{self.table_name}' not found in schema definitions.")
            return

        missing_fields = [
            field for field in self.fields.get("fields", []) if field not in kwargs
        ]
        if missing_fields:
            st.error(f"Missing fields: {', '.join(missing_fields)}")
            return

        fields = ", ".join(self.fields["fields"])
        placeholders = ", ".join([f":{field}" for field in self.fields["fields"]])

        try:
            with self.conn.connect() as conn:
                conn.execute(
                    text(
                        f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
                    ),
                    kwargs,
                )
                conn.commit()
            st.success("Record created successfully!")
        except Exception as e:
            st.error(f"Error creating record: {str(e)}")

    def update_record(self, user_id, **kwargs):
        """Update specific fields in a record, keeping original values if fields are empty."""
        primary_key = self.fields["primary_key"]

        with self.conn.connect() as conn:
            # Fetch current resident data
            result = (
                conn.execute(
                    text(
                        f"SELECT * FROM {self.table_name} WHERE {primary_key} = :user_id"
                    ),
                    {"user_id": user_id},
                )
                .mappings()
                .fetchone()
            )  # Ensures dictionary-like result

            if result:
                current_values = dict(result)  # Convert row to dictionary

                # Update resident fields, keeping original values if input is empty
                update_data = {
                    field: kwargs.get(field)
                    if kwargs.get(field)
                    else current_values.get(field)
                    for field in self.fields["fields"]
                }
                update_set = ", ".join([f"{field} = :{field}" for field in update_data])

                conn.execute(
                    text(
                        f"UPDATE {self.table_name} SET {update_set} WHERE {primary_key} = :user_id"
                    ),
                    {"user_id": user_id, **update_data},
                )

                # Update emergency contact if provided
                if "emergency_contacts" in kwargs and kwargs["emergency_contacts"]:
                    emergency_contact = kwargs["emergency_contacts"][
                        0
                    ]  # Only update one emergency contact for now

                    # Fetch current emergency contact data
                    current_emergency_contact = (
                        conn.execute(
                            text(
                                "SELECT contact_name, relationship, contact_number FROM Resident_Emergency_Contacts WHERE resident_id = :user_id"
                            ),
                            {"user_id": user_id},
                        )
                        .mappings()
                        .fetchone()
                    )  # Ensure dictionary access

                    if current_emergency_contact:
                        # Use existing values if no new data is provided
                        contact_name = (
                            emergency_contact.get("contact_name")
                            or current_emergency_contact["contact_name"]
                        )
                        relationship = (
                            emergency_contact.get("relationship")
                            or current_emergency_contact["relationship"]
                        )
                        contact_number = (
                            emergency_contact.get("contact_number")
                            or current_emergency_contact["contact_number"]
                        )

                        # Update emergency contact in Resident_Emergency_Contacts
                        conn.execute(
                            text(
                                "UPDATE Resident_Emergency_Contacts "
                                "SET contact_name = :contact_name, relationship = :relationship, contact_number = :contact_number "
                                "WHERE resident_id = :user_id"
                            ),
                            {
                                "user_id": user_id,
                                "contact_name": contact_name,
                                "relationship": relationship,
                                "contact_number": contact_number,
                            },
                        )

                conn.commit()
                st.success("Record updated successfully!")
            else:
                st.error("Record not found.")

    def delete_record(self, table_name, primary_key_column, user_id):
        """
        Deletes a record from the specified table based on the primary key column.
        """
        try:
            with self.conn.connect() as conn:
                # Execute the delete query using the provided column name
                query = text(
                    f"DELETE FROM {table_name} WHERE {primary_key_column} = :user_id"
                )
                conn.execute(query, {"user_id": user_id})

                # Commit the transaction
                conn.commit()
                st.success(f"Record successfully deleted from {table_name}!")
        except IntegrityError as e:
            st.error(f"Error deleting record: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

    def fetch_options(self, table_name, id_field, name_field):
        """Fetch ID and Name pairs for dropdown selections."""
        query = f"SELECT {id_field}, {name_field} FROM {table_name}"
        result = self.conn.query(query, ttl=0)
        return {row[name_field]: row[id_field] for _, row in result.iterrows()}

    def show_full_table(self, data):
        if not data:
            st.warning("No resident data available.")
            return

        # Display resident data with emergency contact details
        st.write("### Residents and Their Emergency Contacts")
        for entry in data:
            st.markdown(f"**Resident ID:** {entry['resident_id']}")
            st.markdown(f"**Name:** {entry['name']}")
            st.markdown(f"**Date of Birth:** {entry['date_of_birth']}")
            st.markdown(f"**Gender:** {entry['gender']}")
            st.markdown(f"**Contact Number:** {entry['contact_number']}")
            st.markdown(f"**Address:** {entry['address']}")
            st.markdown(f"**Username:** {entry['username']}")
            st.markdown(f"**Emergency Contact Name:** {entry['contact_name']}")
            st.markdown(f"**Emergency Relationship:** {entry['relationship']}")
            st.markdown(f"**Emergency Contact Number:** {entry['contact_number']}")
            st.divider()

    def create_resident_with_contacts(self, resident_data, emergency_contacts):
        """Insert a resident and their emergency contacts."""
        resident_fields = ", ".join(self.fields["fields"])
        resident_placeholders = ", ".join(
            [f":{field}" for field in self.fields["fields"]]
        )

        try:
            # Insert resident record
            query_resident = f"""
            INSERT INTO Resident ({resident_fields}) 
            VALUES ({resident_placeholders}) 
            RETURNING resident_id;
            """
            with self.conn.connect() as conn:
                result = conn.execute(text(query_resident), resident_data)
                resident_id = result.fetchone()[0]

                # Insert emergency contacts
                for contact in emergency_contacts:
                    contact_query = """
                    INSERT INTO Resident_Emergency_Contacts 
                    (resident_id, contact_name, relationship, contact_number) 
                    VALUES (:resident_id, :contact_name, :relationship, :contact_number);
                    """
                    conn.execute(
                        text(contact_query),
                        {
                            "resident_id": resident_id,
                            "contact_name": contact["contact_name"],
                            "relationship": contact["relationship"],
                            "contact_number": contact["contact_number"],
                        },
                    )
                conn.commit()

            st.success("Resident and emergency contacts added successfully!")
        except Exception as e:
            st.error(f"Error creating resident with contacts: {e}")

    def delete_resident(self, resident_id):
        """
        Deletes a resident and all related records using cascading delete.
        """
        try:
            with self.conn.connect() as conn:
                conn.execute(
                    text("DELETE FROM Resident WHERE resident_id = :resident_id"),
                    {"resident_id": resident_id},
                )
                conn.commit()
                st.success("Resident deleted successfully!")
        except Exception as e:
            st.error(f"Error deleting resident: {e}")

    def clean_up_null_entries(self):
        """
        Deletes orphaned rows where foreign key columns are NULL (e.g., in Schedule or Medical_Record).
        """
        try:
            with self.conn.connect() as conn:
                conn.execute(
                    text(
                        "DELETE FROM Schedule WHERE resident_id IS NULL AND staff_id IS NULL"
                    )
                )
                conn.commit()
        except Exception as e:
            st.error(f"Error during cleanup: {e}")

    def delete_staff(self, staff_id):
        """
        Deletes a staff member and all related records using cascading delete.
        """
        try:
            with self.conn.connect() as conn:
                conn.execute(
                    text("DELETE FROM Staff WHERE staff_id = :staff_id"),
                    {"staff_id": staff_id},
                )
                conn.commit()
                st.success("Staff deleted successfully!")
        except Exception as e:
            st.error(f"Error deleting staff: {e}")

    def delete_admin(self, admin_id):
        """
        Deletes a admin member and all related records using cascading delete.
        """
        try:
            with self.conn.connect() as conn:
                conn.execute(
                    text("DELETE FROM Admin WHERE admin_id = :admin_id"),
                    {"admin_id": admin_id},
                )
                conn.commit()
                st.success("Admin deleted successfully!")
        except Exception as e:
            st.error(f"Error deleting admin: {e}")

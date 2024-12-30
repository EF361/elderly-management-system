import streamlit as st
from sqlalchemy import create_engine, text


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
                "fields": [
                    "name",
                    "username",
                    "password",
                    "contact_number",
                ],
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
            "staff": {
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
        }
        return table_fields.get(self.table_name.lower(), {})

    def show_table(self):
        """Show all records in the specified user table."""
        query = f"SELECT * FROM {self.table_name};"
        df = self.conn.query(query, ttl=0)
        st.dataframe(df, use_container_width=True)

    def create_record(self, **kwargs):
        """Insert a new record into the specified user table."""
        missing_fields = [
            field for field in self.fields["fields"] if field not in kwargs
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
            result = conn.execute(
                text(f"SELECT * FROM {self.table_name} WHERE {primary_key} = :user_id"),
                {"user_id": user_id},
            ).fetchone()

            if result:
                current_values = result._mapping  # Access the columns by name
                update_data = {
                    field: kwargs.get(field) or current_values[field]
                    for field in self.fields["fields"]
                }
                update_set = ", ".join([f"{field} = :{field}" for field in update_data])

                conn.execute(
                    text(
                        f"UPDATE {self.table_name} SET {update_set} WHERE {primary_key} = :user_id"
                    ),
                    {"user_id": user_id, **update_data},
                )
                conn.commit()
                st.success("Record updated successfully!")
            else:
                st.error("Record not found.")

    def delete_record(self, user_id):
        """Delete a record from the specified user table by primary key."""
        primary_key = self.fields["primary_key"]
        with self.conn.connect() as conn:
            conn.execute(
                text(f"DELETE FROM {self.table_name} WHERE {primary_key} = :user_id"),
                {"user_id": user_id},
            )
            conn.commit()
        st.success("Record deleted successfully!")

    def fetch_options(self, table_name, id_field, name_field):
        """Fetch ID and Name pairs for dropdown selections."""
        query = f"SELECT {id_field}, {name_field} FROM {table_name}"
        result = self.conn.query(query, ttl=0)
        return {row[name_field]: row[id_field] for _, row in result.iterrows()}

    def fetch_full_residents_with_contacts(self):
        query = """
        SELECT r.resident_id, r.name, r.date_of_birth, r.gender, r.contact_number, 
            r.address, r.username, rec.contact_name, rec.relationship, rec.contact_number AS emergency_contact_number
        FROM Resident r
        LEFT JOIN Resident_Emergency_Contacts rec ON r.resident_id = rec.resident_id;
        """
        try:
            # Get the connection object
            conn = st.connection("postgresql", type="sql")

            # Execute the query using the `query` method
            result = conn.query(query)

            # Convert result to a list of dictionaries if needed
            return [dict(row) for row in result]
        except Exception as e:
            st.error(f"Error fetching residents with contacts: {e}")
            return []

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

        def get_table_fields(self):
            table_fields = {
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
                # Define for other tables if necessary
            }
            return table_fields.get(self.table_name.lower(), {})

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

    def fetch_full_residents_with_contacts(self):
        """Fetch residents and their emergency contacts."""
        query = """
        SELECT r.resident_id, r.name, r.date_of_birth, r.gender, r.contact_number, 
               r.address, r.username, rec.contact_name, rec.relationship, rec.contact_number AS emergency_contact_number
        FROM Resident r
        LEFT JOIN Resident_Emergency_Contacts rec ON r.resident_id = rec.resident_id;
        """
        try:
            result = self.conn.query(query, ttl=0)
            return result.to_dict("records")  # Convert to a list of dictionaries
        except Exception as e:
            st.error(f"Error fetching residents with contacts: {e}")
            return []

    def delete_resident_with_contacts(self, resident_id):
        """Delete a resident and their emergency contacts."""
        try:
            with self.conn.connect() as conn:
                conn.execute(
                    text("DELETE FROM Resident WHERE resident_id = :resident_id"),
                    {"resident_id": resident_id},
                )
                conn.commit()
            st.success("Resident and emergency contacts deleted successfully!")
        except Exception as e:
            st.error(f"Error deleting resident: {e}")

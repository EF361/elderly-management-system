import streamlit as st
from sqlalchemy import create_engine, text


class UserManagement:
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
                "fields": ["admin_name", "email", "password", "contact_number"],
            },
            "resident": {
                "primary_key": "resident_id",
                "fields": [
                    "resident_name",
                    "date_of_birth",
                    "gender",
                    "contact_number",
                    "address",
                ],
            },
            "staff": {
                "primary_key": "staff_id",
                "fields": [
                    "staff_name",
                    "role",
                    "contact_number",
                    "email",
                    "hire_date",
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
        fields = ", ".join(self.fields["fields"])
        placeholders = ", ".join([f":{field}" for field in self.fields["fields"]])

        with self.conn.connect() as conn:
            conn.execute(
                text(
                    f"INSERT INTO {self.table_name} ({fields}) VALUES ({placeholders})"
                ),
                kwargs,
            )
            conn.commit()
        st.success("Record created successfully!")

    def update_record(self, user_id, **kwargs):
        """Update specific fields in a record, keeping original values if fields are empty."""
        primary_key = self.fields["primary_key"]

        # Retrieve existing record
        with self.conn.connect() as conn:
            result = conn.execute(
                text(f"SELECT * FROM {self.table_name} WHERE {primary_key} = :user_id"),
                {"user_id": user_id},
            ).fetchone()

            # Convert result to dictionary-like mapping to access by column names
            if result:
                current_values = result._mapping  # Access the columns by name

                # Use existing values if no new input is provided
                update_data = {
                    field: kwargs.get(field) or current_values[field]
                    for field in self.fields["fields"]
                }
                update_set = ", ".join([f"{field} = :{field}" for field in update_data])

                # Update the record
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

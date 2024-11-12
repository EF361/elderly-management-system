import streamlit as st
from sqlalchemy import create_engine, text

# Initialize connection
conn = st.connection("postgresql", type="sql")
engine = create_engine("postgresql://postgres:12345@localhost:5432/elderlymanagement")


def showTable():
    """show table that are in the admin table"""
    st.dataframe(df, use_container_width=True)


# Perform initial query to display the admin table.
df = conn.query("SELECT * FROM admin;", ttl=0)

st.title("Admin Management")

# Show the table
showTable()

# Select operation
option = st.selectbox(
    label="Select an operation",
    options=["Create", "Update", "Delete"],
)

if option == "Create":
    name = st.text_input(label="Enter Name:")
    email = st.text_input(label="Enter Email:")
    phone_number = st.text_input(label="Phone Number:")
    password = st.text_input(label="Password: ", type="password")

    if st.button("Add Admin"):
        with conn.connect() as conn:
            # Insert new record using `text`
            conn.execute(
                text(
                    "INSERT INTO admin (admin_name, email, password, contact_number) VALUES (:admin_name, :email, :password, :contact_number)"
                ),
                {
                    "admin_name": name,
                    "email": email,
                    "contact_number": phone_number,
                    "password": password,
                },
            )
            conn.commit()

        st.success("Record created successfully!")


elif option == "Update":
    admin_id = st.number_input("Enter Admin ID to Update:", min_value=1, step=1)
    new_email = st.text_input("New Email:")
    new_phone = st.text_input("New Phone Number:")

    if st.button("Update Admin"):
        with conn.connect() as conn:
            # Update record using `text`
            conn.execute(
                text(
                    "UPDATE admin SET email = :new_email, contact_number = :new_phone WHERE admin_id = :admin_id"
                ),
                {"new_email": new_email, "new_phone": new_phone, "admin_id": admin_id},
            )
            conn.commit()

        st.success("Record updated successfully!")

elif option == "Delete":
    admin_id = st.number_input("Enter Admin ID to Delete:", min_value=1, step=1)

    if st.button("Execute Delete"):
        with conn.connect() as conn:
            # Delete record using `text`
            conn.execute(
                text("DELETE FROM admin WHERE admin_id = :admin_id"),
                {"admin_id": admin_id},
            )
            conn.commit()

        st.success("Record deleted successfully!")

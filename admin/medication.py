import streamlit as st
from management import UserManagement
from datetime import date


# Define MedicineManagement class
class MedicineManagement(UserManagement):
    def __init__(self):
        super().__init__("Medicine")
        self.fields = {
            "primary_key": "medicine_id",
            "fields": ["medicine_name", "description", "usage", "stock_quantity"],
        }

    def show_table(self):
        """Display all medicines in a table."""
        query = """
        SELECT m.medicine_id, m.medicine_name, m.description, m.usage, m.stock_quantity
        FROM Medicine m
        """
        df = self.conn.query(query, ttl=0)
        st.dataframe(df, use_container_width=True)


# Initialize MedicineManagement
med_manager = MedicineManagement()
st.title("Medicine Management")

# Display table of medicines
med_manager.show_table()

# Fetch medicine for dropdown selections
medicines = med_manager.fetch_options("Medicine", "medicine_id", "medicine_name")

# Select CRUD operation
option = st.selectbox("Select Operation", ["Create", "Update", "Delete"])

if option == "Create":
    st.write("### Add New Medicine")
    medicine_name = st.text_input("Medicine Name")
    description = st.text_area("Description")
    usage = st.text_area("Usage Instructions")
    stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1)

    if medicine_name or description or usage or stock_quantity is None:
        if st.button("Add Medicine"):
            try:
                med_manager.create_record(
                    medicine_name=medicine_name,
                    description=description,
                    usage=usage,
                    stock_quantity=stock_quantity,
                )
            except Exception as e:
                st.error(f"There is an error: {e}")

elif option == "Update":
    st.write("### Update Medicine")

    # Select a resident by name
    medicine_name = st.selectbox("Select Medicine:", options=list(medicines.keys()))

    # Fetch the selected medicine's details
    selected_medicine_id = medicines[medicine_name]
    st.write(f"Selected Medicine ID: {selected_medicine_id}")

    # Input fields for updatable data
    description = st.text_area("Description", value="")
    usage = st.text_area("Usage Instructions", value="")
    stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1)

    if st.button("Update Medicine"):
        med_manager.update_record(
            selected_medicine_id,
            description=description,
            usage=usage,
            stock_quantity=stock_quantity,
        )

elif option == "Delete":
    st.write("### Delete Medicine")

    # Select a resident by name for deletion
    resident_name = st.selectbox(
        "Select Medicine to Delete:", options=list(medicines.keys())
    )
    selected_medicine_id = medicines[resident_name]

    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{resident_name}'?")
        if st.button("Delete User"):
            med_manager.delete_record(selected_medicine_id)

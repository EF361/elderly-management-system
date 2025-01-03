import streamlit as st
from management import Management
from datetime import date  # noqa: F401


class MedicineManagement(Management):
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


med_manager = MedicineManagement()

# Check if user is logged in, if yes, display title
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
    st.title("Medicine Management")
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()


# Display table of medicines
med_manager.show_table()

# Fetch medicine for dropdown selections
medicines = med_manager.fetch_options("Medicine", "medicine_id", "medicine_name")

# Select CRUD operation
option = st.selectbox("Select Operation", ["Create", "Update", "Delete"])

if option == "Create":
    with st.expander("Create Medicine"):
        medicine_name = st.text_input(
            "Medicine Name",
            placeholder="Paracetamol",
        )
        description = st.text_area(
            "Description",
            placeholder="Paracetamol is a medication used to treat pain and reduce fever. It works by blocking pain signals in the brain.",
        )
        usage = st.text_area(
            "Usage Instructions", placeholder="Fever reduction, Pain relief"
        )
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
    with st.expander("Update Medicine"):
        # Select a medicine by name
        medicine_name = st.selectbox("Select Medicine:", options=list(medicines.keys()))

        # Fetch the selected medicine's details
        selected_medicine_id = medicines[medicine_name]
        st.write(f"Selected Medicine ID: {selected_medicine_id}")

        # Input fields for updatable data
        description = st.text_area(
            "Description",
            value="",
            placeholder="Optional",
        )
        usage = st.text_area(
            "Usage Instructions",
            value="",
            placeholder="Optional",
        )
        stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1)

        if st.button("Update Medicine"):
            med_manager.update_record(
                selected_medicine_id,
                description=description,
                usage=usage,
                stock_quantity=stock_quantity,
            )

elif option == "Delete":
    # Select a medicine by name for deletion
    medicine_name = st.selectbox(
        "Select Medicine to Delete:", options=list(medicines.keys())
    )
    selected_medicine_id = medicines[medicine_name]

    with st.expander("Confirm Deletion"):
        st.write(f"Are you sure you want to delete '{medicine_name}'?")
        if st.button("Delete Medicine"):
            med_manager.delete_record(selected_medicine_id)

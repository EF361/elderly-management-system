import streamlit as st


class ContactNumberInput:
    def __init__(self, label, placeholder="Enter contact number"):
        self.label = label
        self.placeholder = placeholder
        self.min_length = 10
        self.max_length = 11
        self.contact_number = None

    def render(self, key=None):
        # Create a text input with a unique key
        self.contact_number = st.text_input(
            self.label, placeholder=self.placeholder, key=key
        )

        # Validate input
        if self.contact_number:
            if not self.contact_number.isdigit():
                st.error("Contact number must contain only numbers.")
            elif len(self.contact_number) > self.max_length:
                st.error("Contact number is more than 11 digits.")
            elif len(self.contact_number) < self.min_length:
                st.error("Contact number is too short.")
            else:
                st.success("Valid contact number!")
                return self.contact_number
        return None

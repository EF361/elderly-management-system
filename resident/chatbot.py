import streamlit as st

st.title("Chatbot Interaction")
st.write("Hello! How can I assist you today?")

user_input = st.text_input("Your message:")
if user_input:
    st.write("You:", user_input)
    # Placeholder response
    st.write("Chatbot: I'll check your schedule for you.")

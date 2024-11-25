import streamlit as st

st.title("Chatbot Interaction")

# Check if user is logged in
if "user_name" in st.session_state:
    user_name = st.session_state["user_name"]
else:
    st.error("You are not logged in. Please log in to access the dashboard.")
    st.stop()

messages = st.container(height=300)
if prompt := st.chat_input("Say something"):
    messages.chat_message("user").write(prompt)
    messages.chat_message("assistant").write(f"Echo: {prompt}")

import streamlit as st

st.title("Chatbot Interaction")

messages = st.container(height=300)
if prompt := st.chat_input("Say something"):
    messages.chat_message("user").write(prompt)
    messages.chat_message("assistant").write(f"Echo: {prompt}")

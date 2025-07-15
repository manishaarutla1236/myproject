# app.py

import streamlit as st
from chatbot_logic import get_bot_response

# Streamlit page configuration
st.set_page_config(page_title="Chatbot 🤖", page_icon="💬")

st.title("🤖 Streamlit Chatbot")
st.markdown("Type your message below to chat with the bot!")

# Initialize chat history in session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input box
user_input = st.chat_input("Say something...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append(("user", user_input))

    # Get bot reply using logic from chatbot_logic.py
    bot_response = get_bot_response(user_input)
    st.session_state.chat_history.append(("bot", bot_response))

# Display the conversation
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.chat_message("user").write(message)
    else:
        st.chat_message("assistant").write(message)

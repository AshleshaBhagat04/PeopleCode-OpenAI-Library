# simpleChatAppStreamlit.py
# This Streamlit app allows users to interact with OpenAI's language model. Users can enter prompts
# and receive responses on the web interface.

import streamlit as st
import sys
import os

# Add parent directory to sys.path to import USFGenAI module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from USFGenAI import *

conversation = []

st.title("Simple Q&A")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
set_model(selected_model)

user_prompt = st.text_input("Enter a prompt:")

if st.button("Ask"):
    if user_prompt.strip().lower() == "exit":
        st.stop()
    try:
        response = ask_question(conversation, user_prompt, "You are a helpful assistant."
                                )
        st.session_state.conversation = response['conversation']
        st.text_area("Response:", response['reply'], height=200)
    except Exception as e:
        st.error(f"An error occurred: {e}")

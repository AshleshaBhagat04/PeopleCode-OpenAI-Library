# chatAppWithSamplePromptsStreamlit.py
# This Streamlit app interacts with the OpenAI API to facilitate a conversation.
# Users can ask questions, generate prompts, and get follow-up questions.

import streamlit as st
import sys
import os

# Add parent directory to sys.path to import PeopleCodeAI module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from PeopleCodeOpenAI import OpenAI_Conversation

# Load API key from environment variable or a secure source
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key is not set. Please set the environment variable 'OPENAI_API_KEY'.")
    st.stop()

# Initialize OpenAI_Conversation instance
conversation_instance = OpenAI_Conversation(api_key)

# Streamlit App
st.title("Follow-up Chat")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
conversation_instance.set_model(selected_model)

# Instructions input
instructions = st.text_area("System Prompt:", "You are a very helpful assistant.")

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# User prompt input
user_prompt = st.text_input("Enter your prompt:")

if st.button("Ask"):
    if user_prompt:
        response = conversation_instance.ask_question(instructions, user_prompt)
        answer = response['reply']
        st.session_state.conversation = response['conversation']
        st.text_area("Response:", answer, height=200)

        followup_qs = conversation_instance.generate_followups(user_prompt, answer, 3, 25)
        st.write("Follow-up Questions:")
        for idx, question in enumerate(followup_qs):
            st.write(f"{question}")

with st.expander("Generate a Prompt"):
    context = st.text_input("Enter the context for generating a prompt:")
    if st.button("Generate Prompt"):
        if context:
            generated_prompt = conversation_instance.generate_sample_prompts(context, 1, 25)
            st.text_area("Generated Prompt:", '\n'.join(generated_prompt), height=100)

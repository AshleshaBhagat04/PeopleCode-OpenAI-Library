# chatAppWithSamplePromptsStreamlit.py
# This Streamlit app interacts with the OpenAI API to facilitate a conversation.
# Users can ask questions, generate prompts, and get follow-up questions.


import os
import streamlit as st

from USFGenAI import *

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    st.stop()
set_api_key(api_key)

conversation = []

# Streamlit App
st.title("Follow-up Chat")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
set_model(selected_model)

# Instructions input
instructions = st.text_area("System Prompt:", "You are a very helpful assistant.")

# User prompt input
user_prompt = st.text_input("Enter your prompt:")

if st.button("Ask"):
    if user_prompt:
        response = ask_question(conversation, user_prompt, "You are a very helpful assistant.")
        answer = response['reply']
        conversation = response['conversation']
        st.text_area("Response:", answer)
        followup_qs = generate_followups(user_prompt, answer, 3, 25)
        st.write("Follow-up Questions:")
        for idx, question in enumerate(followup_qs):
            st.write(f"{question}")

with st.expander("Generate a Prompt"):
    context = st.text_input("Enter the context for generating a prompt:")
    if st.button("Generate Prompt"):
        if context:
            generated_prompt = generate_prompt(context, 25)
            st.text_area("Generated Prompt:", generated_prompt)

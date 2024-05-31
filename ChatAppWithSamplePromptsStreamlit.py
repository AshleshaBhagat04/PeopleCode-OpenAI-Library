# chatAppWithSamplePromptsStreamlit.py
# This Streamlit app interacts with the OpenAI API to facilitate a conversation.
# Users can ask questions, generate prompts, and get follow-up questions.


import openai
import os
import streamlit as st

from USFGenAI import generate_prompt, ask_question, generate_followups

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    st.stop()
openai.api_key = api_key

conversation = []

# Streamlit App
st.title("Follow-up Chat")

# Instructions input
instructions = st.text_area("System Prompt:", "You are a very helpful assistant.")

# User prompt input
user_prompt = st.text_input("Enter your prompt:")

if st.button("Ask"):
    if user_prompt:
        response = ask_question(conversation, user_prompt, "You are a very helpful assistant.", settings={"model": "gpt-3.5-turbo"})
        answer = response['reply']
        conversation = response['conversation']
        st.text_area("Response:", answer)
        followup_qs = generate_followups(user_prompt, answer, 3, 25, settings={"model": "gpt-3.5-turbo"})
        st.write("Follow-up Questions:")
        for idx, question in enumerate(followup_qs):
            st.write(f"{question}")

with st.expander("Generate a Prompt"):
    context = st.text_input("Enter the context for generating a prompt:")
    if st.button("Generate Prompt"):
        if context:
            generated_prompt = generate_prompt(context, 25, settings={"model": "gpt-3.5-turbo"})
            st.text_area("Generated Prompt:", generated_prompt)

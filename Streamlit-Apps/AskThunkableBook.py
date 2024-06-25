# AskThunkableBook.py
# This Streamlit application interacts with OpenAI's language models.
# It allows users to select a model, ask questions, generate prompts, and handle follow-up questions.

import streamlit as st
import sys
import os

# Add parent directory to sys.path to import USFGenAI module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from USFGenAI import *

# Streamlit App
st.title("AskThunkableBook")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
set_model(selected_model)

# Assistant ID
ASSISTANT_ID = "asst_RRXmeNcR4UEj8YSrzOqWkJYa"

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if 'generated_prompt' not in st.session_state:
    st.session_state.generated_prompt = ""

if 'instructions' not in st.session_state:
    st.session_state.instructions = "You are a very helpful assistant."

# Instructions input
st.session_state.instructions = st.text_area("System Prompt:", st.session_state.instructions)

# User prompt input
user_prompt = st.text_input("Enter your prompt:", "")

# Ask button
if st.button("Ask"):
    if user_prompt:
        response = ask_assistant_question(st.session_state.conversation, user_prompt, st.session_state.instructions, ASSISTANT_ID)
        st.session_state.conversation = response['conversation']
        st.text_area("Response:", response['reply'], height=200)

# Generate prompt section
with st.expander("Generate a Prompt"):
    context = st.text_input("Enter the context for generating a prompt:", "")
    max_words = st.number_input("Maximum number of words for the generated prompt:", min_value=1, value=25)

    if st.button("Generate Prompt"):
        if context:
            generated_prompt = generate_prompt_assistant(context, max_words, ASSISTANT_ID)
            st.session_state.generated_prompt = generated_prompt
            st.text_area("Generated Prompt:", generated_prompt, height=100)

# Ask generated prompt button
if st.session_state.generated_prompt:
    st.write(f"Generated Prompt: {st.session_state.generated_prompt}")
    if st.button("Ask Generated Prompt"):
        response = ask_assistant_question(st.session_state.conversation, st.session_state.generated_prompt, st.session_state.instructions, ASSISTANT_ID)
        st.session_state.conversation = response['conversation']
        st.text_area("Response:", response['reply'], height=200)
        st.session_state.generated_prompt = ""

# Follow-up questions section
with st.expander("Generate Follow-up Questions"):
    num_samples = st.number_input("Number of follow-up questions to generate:", min_value=1, value=3)
    max_words_followups = st.number_input("Maximum number of words for follow-up questions:", min_value=1, value=25)

    if st.button("Generate Follow-ups"):
        if st.session_state.conversation:
            latest_question = st.session_state.conversation[-2]['content'] if len(st.session_state.conversation) >= 2 else ""
            latest_answer = st.session_state.conversation[-1]['content'] if st.session_state.conversation else ""
            followup_questions = generate_followups_assistant(latest_question, latest_answer, num_samples, max_words_followups, ASSISTANT_ID)
            st.session_state.followup_questions = followup_questions
            st.write("Follow-up Questions:")
            for idx, question in enumerate(followup_questions):
                st.write(f"{question}")

# Select and ask follow-up question
if 'followup_questions' in st.session_state and st.session_state.followup_questions:
    followup_choice = st.selectbox("Select a follow-up question to ask:", range(len(st.session_state.followup_questions)))
    if st.button("Ask Follow-up"):
        selected_followup = st.session_state.followup_questions[followup_choice]
        followup_response = ask_assistant_question(st.session_state.conversation, selected_followup, st.session_state.instructions, ASSISTANT_ID)
        st.session_state.conversation = followup_response['conversation']
        st.text_area("Response:", followup_response['reply'], height=200)

# Display conversation history
if st.button("Show Conversation History"):
    st.write("Conversation History:")
    for msg in st.session_state.conversation:
        role = "User" if msg['role'] == "user" else "Assistant"
        st.write(f"{role}: {msg['content']}")

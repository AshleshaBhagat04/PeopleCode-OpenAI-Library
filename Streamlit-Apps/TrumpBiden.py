# TrumpBiden.py
# This creates a Streamlit application that interacts with OpenAI's language models.
# It allows users to select a model, ask questions, generate prompts, and handle follow-up questions.

import streamlit as st
import sys
import os

# Add parent directory to sys.path to import USFGenAI module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from USFGenAI import *

# Initialize Streamlit app
st.title("Election 2024: Is Voting Worth it?")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = model_options[1]

set_model(selected_model)

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if 'generated_prompt' not in st.session_state:
    st.session_state.generated_prompt = ""

if 'instructions' not in st.session_state:
    st.session_state.instructions = "You are a very helpful assistant."

if 'text_input_value' not in st.session_state:
    st.session_state.text_input_value = ""

if 'cur_question' not in st.session_state:
    st.session_state.cur_question = -1


# Function to update the text input value in session state
def update_text_input_value(new_value=None):
    if new_value is not None:
        st.session_state['text_input_value'] = new_value
    else:
        pass


# Function to ask a question using OpenAI model
def ask_it(user_question):
    response = ask_question(st.session_state.conversation, user_question, st.session_state.instructions)
    st.text_area("OpenAI's Response:", response['reply'], height=300)
    # Add additional handling for special cases if needed


# List of predefined questions
questions = [
    "Compare Trump/Biden on Womens Rights",
    "Compare Trump/Biden on Civil Rights",
    "What are typical behaviors of an aspiring autocrat?",
    "Has Donald Trump exhibited the behavior of an aspiring autocrat?",
    "Is a peaceful transition to power important to a democracy?",
    "Did Trump facilitate the peaceful transition to power on Jan 6., 2021?"
]

# Display buttons for each question
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(questions[0]):
        update_text_input_value(questions[0])
        st.session_state.cur_question = 0

with col2:
    if st.button(questions[1]):
        update_text_input_value(questions[1])
        st.session_state.cur_question = 1

with col3:
    if st.button(questions[2]):
        update_text_input_value(questions[2])
        st.session_state.cur_question = 2

container2 = st.container()

with container2:
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(questions[3]):
            update_text_input_value(questions[3])
            st.session_state.cur_question = 3
    with col2:
        if st.button(questions[4]):
            update_text_input_value(questions[4])
            st.session_state.cur_question = 4

    with col3:
        if st.button(questions[5]):
            update_text_input_value(questions[5])
            st.session_state.cur_question = 5

# Text input for user's custom question
user_prompt = st.text_input("Your Question:", value=st.session_state['text_input_value'],
                            on_change=update_text_input_value, key='text_input')

# Ask button to trigger question processing
if st.button("Ask"):
    if user_prompt:
        ask_it(user_prompt)

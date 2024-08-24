# AskThunkableBook.py
# This Streamlit application interacts with OpenAI's language models.
# It allows users to select a model, ask questions, generate prompts, and handle follow-up questions.

import streamlit as st
import sys
import os

# Add parent directory to sys.path to import OpenAI_Conversation module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from PeopleCodeOpenAI import OpenAI_Conversation

# Initialize OpenAI_Conversation instance
API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    st.error("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    st.stop()
conversation = OpenAI_Conversation(api_key=API_KEY)

# Streamlit App
st.title("Drag and Drop Coding with Thunkable")
st.subheader("Ask the Book")

# Model selection

conversation.set_model("gpt-4o-mini")
conversation.set_temperature(.1)

# Set  assistant ID if using specific assistant functionality

ASSISTANT_ID = "asst_LBdQmnU4xdzxRhZ822zNZk4q";

if 'text_input_value' not in st.session_state:
    st.session_state.text_input_value = ""

if 'instructions' not in st.session_state:
    st.session_state.instructions = "You are an expert Thunkable coder and know the 'Drag And Drop Code with Thunkable' book as good as the author"

# sample prompt
if 'q1' not in st.session_state:
    prompts = conversation.generate_sample_prompts(st.session_state.instructions+ " Please provide some sample questions about the Thunkable book. ",2,7,ASSISTANT_ID)
    if len(prompts)>0:
        st.session_state.q1=prompts[0]
    else:
        st.session_state.q1=""
    if len(prompts)>1:
        st.session_state.q2=prompts[1]
    else:
        st.session_state.q2=""


if st.button(st.session_state.q1):    #sample q1 clicked
   st.session_state.text_input_value=st.session_state.q1 

if st.button(st.session_state.q2):    #sample q2 clicked
   st.session_state.text_input_value=st.session_state.q2
# User prompt input
user_prompt = st.text_input("Enter a question about Thunkable coding:", st.session_state.text_input_value)

# Ask button
if st.button("Ask"):
    if user_prompt:
        response = conversation.ask_question(st.session_state.instructions, user_prompt, ASSISTANT_ID)
        st.text_area("Response:", response, height=200)





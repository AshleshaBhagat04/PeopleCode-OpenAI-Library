# EllaBakerStreamlit.py
# This creates a Streamlit application that interacts with OpenAI's language models.
# It allows users to select a model, ask questions, and generate prompts, as if you're talking to Ella Baker herself.

import streamlit as st
import sys
import os

# Add parent directory to sys.path to import USFGenAI module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from USFGenAI import *

context = "Ella Josephine Baker (December 13, 1903 – December 13, 1986) was an African-American civil rights and human rights activist. She was a largely behind-the-scenes organizer whose career spanned more than five decades. In New York City and the South, she worked alongside some of the most noted civil rights leaders of the 20th century, including W. E. B. Du Bois, Thurgood Marshall, A. Philip Randolph, and Martin Luther King Jr. She also mentored many emerging activists, such as Diane Nash, Stokely Carmichael, and Bob Moses, as leaders in the Student Nonviolent Coordinating Committee (SNCC). Ask her a question."
system_prompt = "Answer from the perspective of Ella Baker. Here is some context: " + context

# Initialize session state variables
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if 'latest_question' not in st.session_state:
    st.session_state.latest_question = ""

if 'latest_answer' not in st.session_state:
    st.session_state.latest_answer = ""

if 'followup_questions' not in st.session_state:
    st.session_state.followup_questions = []

if 'prompts' not in st.session_state:
    st.session_state.prompts = []

if 'user_prompt' not in st.session_state:
    st.session_state.user_prompt = ""

st.title("Chat with Ella Baker")

# Add image and text description side by side
col1, col2 = st.columns([1, 1])
with col1:
    st.image("https://www.crmvet.org/crmpics/band/bakerella.jpg")

with col2:
    st.write("""
Ella Baker was an unsung hero in the on-going fight for equality and social justice. Ask her a question to learn more!
    """)

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
set_model(selected_model)


def generate_initial_prompts():
    prompt1 = generate_sample_prompts(context, 25)
    prompt2 = generate_sample_prompts(context, 25)
    prompt3 = generate_sample_prompts(context, 25)
    st.session_state.prompts = [prompt1, prompt2, prompt3]


if not st.session_state.prompts:
    generate_initial_prompts()


# Display initial prompts or follow-up questions
if st.session_state.latest_question:
    prompts = st.session_state.followup_questions
else:
    prompts = st.session_state.prompts

choice = st.radio("Choose a question to ask:", options=prompts)
ask_selected = st.button("Ask Selected Question")
input_container = st.empty()
user_prompt = input_container.text_input("Or ask your own question:", value=st.session_state.user_prompt)

# Ask and reset side by side
col1, col2 = st.columns([1, 1])
with col1:
    ask_custom = st.button("Ask")
with col2:
    # Provide functionality to reset the conversation
    if st.button("Reset Conversation"):
        st.session_state.conversation = []
        st.session_state.latest_question = ""
        st.session_state.latest_answer = ""
        st.session_state.followup_questions = []
        st.session_state.user_prompt = ""
        generate_initial_prompts()
        st.rerun()


def update_conversation(prompt):
    response = ask_question(st.session_state.conversation, prompt, system_prompt)
    st.session_state.latest_question = prompt
    st.session_state.latest_answer = response['reply']
    st.session_state.conversation = response['conversation']
    st.session_state.followup_questions = generate_followups(
        st.session_state.latest_question, st.session_state.latest_answer, 3, 25)
    st.session_state.user_prompt = prompt
    st.rerun()


if ask_selected:
    st.session_state.user_prompt = choice
    update_conversation(choice)

elif ask_custom and user_prompt:
    st.session_state.user_prompt = user_prompt
    update_conversation(user_prompt)

if st.session_state.latest_answer:
    # Display response
    st.text_area("Response:", st.session_state.latest_answer, height=200)
    speech_file_path = text_to_speech(st.session_state.latest_answer, "nova")
    st.audio(speech_file_path)

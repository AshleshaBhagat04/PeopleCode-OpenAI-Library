# EllaBakerStreamlit.py
# This creates a Streamlit application that interacts with OpenAI's language models.
# It allows users to select a model, ask questions, and generate prompts, as if you're talking to Ella Baker herself.

import streamlit as st
import sys
import os

# Add parent directory to sys.path to import PeopleCodeOpenAI module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from PeopleCodeOpenAI import OpenAI_Conversation

# Define context and system prompt
context = (
    "Ella Josephine Baker (December 13, 1903 – December 13, 1986) was an African-American civil rights and human rights activist. "
    "She was a largely behind-the-scenes organizer whose career spanned more than five decades. In New York City and the South, "
    "she worked alongside some of the most noted civil rights leaders of the 20th century, including W. E. B. Du Bois, Thurgood Marshall, "
    "A. Philip Randolph, and Martin Luther King Jr. She also mentored many emerging activists, such as Diane Nash, Stokely Carmichael, "
    "and Bob Moses, as leaders in the Student Nonviolent Coordinating Committee (SNCC). Ask her a question."
)
system_prompt = "Answer from the perspective of Ella Baker. Here is some context: " + context

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key is not set. Please set the environment variable 'OPENAI_API_KEY'.")
    st.stop()

# Initialize OpenAI_Conversation instance
conversation_instance = OpenAI_Conversation(api_key=api_key)

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
Ella Baker was an unsung hero in the ongoing fight for equality and social justice. Ask her a question to learn more!
    """)

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
conversation_instance.set_model(selected_model)


def generate_initial_prompts():
    prompt1 = conversation_instance.generate_sample_prompts(context, 1, 25)
    prompt2 = conversation_instance.generate_sample_prompts(context, 1, 25)
    prompt3 = conversation_instance.generate_sample_prompts(context, 1, 25)
    st.session_state.prompts = [prompt1[0], prompt2[0], prompt3[0]]


if not st.session_state.prompts:
    generate_initial_prompts()

# Display initial prompts or follow-up questions
prompts = st.session_state.followup_questions if st.session_state.latest_question else st.session_state.prompts
choice = st.radio("Choose a question to ask:", options=prompts)

# User prompt input
input_container = st.empty()
user_prompt = input_container.text_input("Or ask your own question:", value=st.session_state.user_prompt)

# Ask and reset side by side
col1, col2 = st.columns([1, 1])
with col1:
    ask_custom = st.button("Ask")
with col2:
    if st.button("Reset Conversation"):
        st.session_state.conversation = []
        st.session_state.latest_question = ""
        st.session_state.latest_answer = ""
        st.session_state.followup_questions = []
        st.session_state.user_prompt = ""
        generate_initial_prompts()
        st.experimental_rerun()


def update_conversation(prompt):
    response = conversation_instance.ask_question(system_prompt, prompt)
    st.session_state.latest_question = prompt
    st.session_state.latest_answer = response
    st.session_state.conversation.append({"role": "user", "content": prompt})
    st.session_state.conversation.append({"role": "assistant", "content": response})
    st.session_state.followup_questions = conversation_instance.generate_followups(
        st.session_state.latest_question, st.session_state.latest_answer, 3, 25)
    st.session_state.user_prompt = prompt
    st.experimental_rerun()


if st.button("Ask Selected Question"):
    st.session_state.user_prompt = choice
    update_conversation(choice)

elif ask_custom and user_prompt:
    st.session_state.user_prompt = user_prompt
    update_conversation(user_prompt)

if st.session_state.latest_answer:
    # Display response
    st.text_area("Response:", st.session_state.latest_answer, height=200)
    speech_file_path = conversation_instance.text_to_speech(st.session_state.latest_answer, "nova")
    if speech_file_path:
        st.audio(speech_file_path)

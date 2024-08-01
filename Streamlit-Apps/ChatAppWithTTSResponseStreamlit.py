# ChatAppWithTTSResponseStreamlit.py
# This creates a Streamlit application that interacts with OpenAI's language models.
# It allows users to select a model, ask questions, generate prompts, and handle follow-up questions. All responses
# can be played and heard with the help of the text-to-speech library function.

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
st.title("TTS ChatApp")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
conversation_instance.set_model(selected_model)

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

if st.button("Ask"):
    if user_prompt:
        response = conversation_instance.ask_question(st.session_state.instructions, user_prompt, includePrevConvo=True)
        st.session_state.conversation = conversation_instance.get_conversation()

        # Display response
        st.text_area("Response:", response['reply'], height=200)
        speech_file_path = conversation_instance.text_to_speech(response['reply'])
        if speech_file_path:
            st.audio(speech_file_path)

# Generate prompt section
with st.expander("Generate a Prompt"):
    context = st.text_input("Enter the context for generating a prompt:", "")
    max_words = st.number_input("Maximum number of words for the generated prompt:", min_value=1, value=25)

    if st.button("Generate Prompt"):
        if context:
            generated_prompts = conversation_instance.generate_sample_prompts(context, 1, max_words)
            if generated_prompts:
                st.session_state.generated_prompt = generated_prompts[0]
                st.text_area("Generated Prompt:", st.session_state.generated_prompt, height=100)

# Ask generated prompt button
if st.session_state.generated_prompt:
    st.write(f"Generated Prompt: {st.session_state.generated_prompt}")
    speech_file_path = conversation_instance.text_to_speech(st.session_state.generated_prompt)
    if speech_file_path:
        st.audio(speech_file_path)
    if st.button("Ask Generated Prompt"):
        response = conversation_instance.ask_question(st.session_state.instructions, st.session_state.generated_prompt, includePrevConvo=True)
        st.session_state.conversation.append({"role": "user", "content": st.session_state.generated_prompt})
        st.session_state.conversation.append({"role": "assistant", "content": response['reply']})
        st.text_area("Response:", response['reply'], height=200)
        speech_file_path = conversation_instance.text_to_speech(response['reply'])
        if speech_file_path:
            st.audio(speech_file_path)
        st.session_state.generated_prompt = ""

# Follow-up questions section
with st.expander("Generate Follow-up Questions"):
    num_samples = st.number_input("Number of follow-up questions to generate:", min_value=1, value=3)
    max_words_followups = st.number_input("Maximum number of words for follow-up questions:", min_value=1, value=25)

    if st.button("Generate Follow-ups"):
        if st.session_state.conversation:
            latest_question = st.session_state.conversation[-2]['content'] if len(st.session_state.conversation) >= 2 else ""
            latest_answer = st.session_state.conversation[-1]['content'] if st.session_state.conversation else ""
            followup_questions = conversation_instance.generate_followups(latest_question, latest_answer, num_samples, max_words_followups)
            st.session_state.followup_questions = followup_questions
            st.write("Follow-up Questions:")
            for idx, question in enumerate(followup_questions):
                st.write(f"{question}")
            speech_file_path = conversation_instance.text_to_speech('\n'.join(st.session_state.followup_questions))
            if speech_file_path:
                st.audio(speech_file_path)

# Select and ask follow-up question
if 'followup_questions' in st.session_state and st.session_state.followup_questions:
    followup_choices = [f"Option {idx + 1}" for idx in range(len(st.session_state.followup_questions))]

    followup_choice = st.selectbox("Select a follow-up question to ask:", followup_choices)

    if st.button("Ask Follow-up"):
        selected_idx = int(followup_choice.split()[1]) - 1
        selected_followup = st.session_state.followup_questions[selected_idx]
        followup_response = conversation_instance.ask_question(st.session_state.instructions, selected_followup, includePrevConvo=True)
        st.session_state.conversation.append({"role": "user", "content": selected_followup})
        st.session_state.conversation.append({"role": "assistant", "content": followup_response['reply']})
        st.text_area("Response:", followup_response['reply'], height=200)
        speech_file_path = conversation_instance.text_to_speech(followup_response['reply'])
        if speech_file_path:
            st.audio(speech_file_path)

# Display conversation history
if st.button("Show Conversation History"):
    st.write("Conversation History:")
    for msg in st.session_state.conversation:
        role = "User" if msg['role'] == "user" else "Assistant"
        st.write(f"{role}: {msg['content']}")
    speech_file_path = conversation_instance.text_to_speech('\n'.join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.conversation]))
    if speech_file_path:
        st.audio(speech_file_path)

# VoiceChatStreamlit.py
# This Streamlit app allows users to interact with OpenAI's language model. Users can talk
# and get responses, similar to a conversation.

import tempfile
import streamlit as st
import sys
import os

# Add parent directory to sys.path to import PeopleCodeOpenAI module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from streamlit_mic_recorder import mic_recorder
from PeopleCodeOpenAI import OpenAI_Conversation

# Initialize OpenAI_Conversation
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("API key is not set. Please set the environment variable 'OPENAI_API_KEY'.")
    st.stop()

conversation_manager = OpenAI_Conversation(api_key=api_key)

# Initialize Streamlit app
st.title("Voice Chat")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
conversation_manager.set_model(selected_model)

instructions = "You are a helpful assistant"


def callback():
    if st.session_state.get('my_recorder_output'):
        audio_bytes = st.session_state.my_recorder_output['bytes']
        st.audio(audio_bytes)

        # Save audio bytes to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_file_path = temp_audio_file.name

        try:
            # Perform speech recognition
            transcribed_text = conversation_manager.speech_recognition(temp_audio_file_path)

            # Get response from OpenAI model
            response = conversation_manager.ask_question(instructions, transcribed_text)

            # Convert response to speech
            answer_audio = conversation_manager.text_to_speech(response)
            st.write("Response:")
            st.audio(answer_audio)
        finally:
            # Clean up the temporary file
            os.remove(temp_audio_file_path)


# Ensure 'my_recorder_output' is initialized in session state
if 'my_recorder_output' not in st.session_state:
    st.session_state.my_recorder_output = None

# Initialize the mic recorder with a callback function
mic_recorder(key='my_recorder', callback=callback)

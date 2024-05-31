# simpleChatAppStreamlit.py
# This Streamlit app allows users to interact with OpenAI's language model. Users can enter prompts
# and receive responses on the web interface.


import openai
import os
import streamlit as st

from USFGenAI import ask_question

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    st.stop()
openai.api_key = api_key

conversation = []

st.title("Simple Q&A")

user_prompt = st.text_input("Enter a prompt:")

if st.button("Submit"):
    if user_prompt.strip().lower() == "exit":
        st.stop()

    try:
        response = ask_question(conversation, user_prompt, "You are a helpful assistant.",
                                settings={"model": "gpt-3.5-turbo", }
                                )
        st.session_state.conversation = response['conversation']
        st.text_area("Response:", response['reply'], height=200)

    except Exception as e:
        st.error(f"An error occurred: {e}")

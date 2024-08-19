import streamlit as st
import sys
import os

# Add parent directory to sys.path to import the Assistant module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from PeopleCodeOpenAI import OpenAI_Conversation

st.title("Simple Q&A")

# Initialize conversation instance
api_key = os.getenv('OPENAI_API_KEY')

# Check if the conversation object is already in session state
if 'openai_conversation' not in st.session_state:
    st.session_state.openai_conversation = OpenAI_Conversation(api_key=api_key, model="gpt-4")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
st.session_state.openai_conversation.set_model(selected_model)

user_prompt = st.text_input("Enter a prompt:")

if st.button("Ask"):
    if user_prompt.strip().lower() == "exit":
        st.stop()
    try:
        # Get the conversation object from session state
        openai_conversation = st.session_state.openai_conversation

        # Ask the question
        response = openai_conversation.ask_question(
            instructions="You are a helpful assistant.",
            question=user_prompt
        )

        # Update the conversation history in session state
        st.session_state.openai_conversation.__prevConversation = response

        st.text_area("Response:", response, height=200)
    except Exception as e:
        st.error(f"An error occurred: {e}")

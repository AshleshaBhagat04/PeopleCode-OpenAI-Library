import streamlit as st
import sys
import os

# Add parent directory to sys.path to import the Assistant module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from PeopleCodeOpenAI import OpenAI_Conversation

# Initialize the conversation instance
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
    st.stop()

openai_conversation = OpenAI_Conversation(api_key=api_key, model="gpt-4")

st.title("Simple Q&A and List Generation")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
openai_conversation.set_model(selected_model)

# Tab for different functionalities
tab1, tab2 = st.tabs(["Ask a Question", "Generate a List"])

# Tab 1: Asking a question
with tab1:
    st.subheader("Ask a Question")

    user_prompt = st.text_input("Enter a prompt:")

    if st.button("Ask", key="ask_question"):
        if user_prompt.strip().lower() == "exit":
            st.stop()
        try:
            # Initialize conversation history if not present
            if 'conversation' not in st.session_state:
                st.session_state.conversation = []

            # Set previous conversation history
            openai_conversation._OpenAI_Conversation__prevConversation = st.session_state.conversation

            response = openai_conversation.ask_question(
                instructions="You are a helpful assistant.",
                question=user_prompt
            )
            # Update the conversation history in the session state
            st.session_state.conversation = response['conversation']
            st.text_area("Response:", response['reply'], height=200)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Tab 2: Generating a list
with tab2:
    st.subheader("Generate a List")

    list_description = st.text_input("Enter a description for the list:")
    num_items = st.number_input("Number of items:", min_value=1, max_value=20, value=5)
    max_words = st.number_input("Maximum words per item:", min_value=1, max_value=50, value=10)

    if st.button("Generate List", key="generate_list"):
        if list_description.strip():
            try:
                generated_list = openai_conversation.generate_list(
                    list_description=list_description,
                    numItems=num_items,
                    maxWordsPerItem=max_words
                )
                st.write("Generated List:")
                for idx, item in enumerate(generated_list, start=1):
                    st.write(f"{item}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please provide a description for the list.")

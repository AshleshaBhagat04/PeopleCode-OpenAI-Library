import os
import streamlit as st
from USFGenAI import *

# Load API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    st.stop()
set_api_key(api_key)

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

st.title("Chat with Ella Baker")
st.image("https://hulshofschmidt.wordpress.com/wp-content/uploads/2014/12/ella-baker.jpg")

# Model selection
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
selected_model = st.selectbox("Select the model to use:", model_options)
set_model(selected_model)


def generate_initial_prompts():
    prompt1 = generate_prompt(context, 25)
    prompt2 = generate_prompt(context, 25)
    prompt3 = generate_prompt(context, 25)
    st.session_state.prompts = [prompt1, prompt2, prompt3]


if not st.session_state.prompts:
    generate_initial_prompts()


def display_prompts(prompts):
    st.write("Sample Prompts")
    for i, prompt in enumerate(prompts, 1):
        st.write(f"{prompt}")


# Display initial prompts or follow-up questions
if st.session_state.latest_question:
    display_prompts(st.session_state.followup_questions)
else:
    display_prompts(st.session_state.prompts)

choice = st.radio("Choose a question to ask:", options=[1, 2, 3], index=0)
input_container = st.empty()
user_prompt = input_container.text_input("Or ask your own question: ")

# Logic for handling buttons
ask_selected = st.button("Ask Selected Question")
ask_custom = st.button("Ask")


def update_conversation(prompt):
    response = ask_question(st.session_state.conversation, prompt, system_prompt)
    st.session_state.latest_question = prompt
    st.session_state.latest_answer = response['reply']
    st.session_state.conversation = response['conversation']
    st.session_state.followup_questions = generate_followups(
        st.session_state.latest_question, st.session_state.latest_answer, 3, 25)
    st.rerun()


if ask_selected:
    selected_prompt = st.session_state.prompts[choice - 1]
    update_conversation(selected_prompt)

elif ask_custom and user_prompt:
    update_conversation(user_prompt)

if st.session_state.latest_answer:
    st.session_state.user_prompt = ""
    user_prompt = ""
    # Display response
    st.text_area("Response:", st.session_state.latest_answer, height=200)

# Provide functionality to reset the conversation
if st.button("Reset Conversation"):
    st.session_state.conversation = []
    st.session_state.latest_question = ""
    st.session_state.latest_answer = ""
    st.session_state.followup_questions = []
    generate_initial_prompts()
    st.rerun()

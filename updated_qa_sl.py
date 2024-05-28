import openai
import os
import streamlit as st

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    st.stop()
openai.api_key = api_key

convo_dict = {}


def ask_question(question, instructions):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": question}
        ]
    )
    return response


def generate_prompt(context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate a prompt based on the context provided below."},
            {"role": "user", "content": context}
        ]
    )
    prompt = response['choices'][0]['message']['content'].strip()
    return prompt


def generate_followups():
    followups = ""
    if convo_dict:
        last_user_prompt = list(convo_dict.keys())[-1]
        followups = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "Generate 3 follow-up questions that the user could choose to ask based on the conversation history provided below."},
                {"role": "user", "content": last_user_prompt}
            ]
        )
    return followups['choices'][0]['message']['content'].strip()


# Streamlit App
st.title("Follow-up Chat")

# Instructions input
instructions = st.text_area("System Prompt:", "You are a very helpful assistant.")

# User prompt input
user_prompt = st.text_input("Enter your prompt:")

if st.button("Ask"):
    if user_prompt:
        chat_response = ask_question(user_prompt, instructions)
        convo_dict[user_prompt] = chat_response['choices'][0]['message']['content'].strip()
        st.text_area("Response:", chat_response['choices'][0]['message']['content'].strip())
        followups = generate_followups()
        st.text_area("Follow-up questions:", followups)

with st.expander("Generate a Prompt"):
    context = st.text_input("Enter the context for generating a prompt:")
    if st.button("Generate Prompt"):
        if context:
            generated_prompt = generate_prompt(context)
            st.text_area("Generated Prompt:", generated_prompt)

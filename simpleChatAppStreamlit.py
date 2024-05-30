import openai
import os
import streamlit as st

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    st.stop()

openai.api_key = api_key

st.title("Simple Q&A")

user_prompt = st.text_input("Enter a prompt:")

if st.button("Submit"):
    if user_prompt.strip().lower() == "exit":
        st.stop()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_prompt}
            ]
        )

        st.write("Response: ")
        st.write(response['choices'][0]['message']['content'].strip())

    except Exception as e:
        st.error(f"An error occurred: {e}")

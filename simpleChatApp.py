# simpleChatApp.py
# This allows the user to interact with OpenAI's language model via the command line. The user
# can input prompts and receive responses from the model.

import openai
import os
import sys

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ]
    )

    print("Response: ")
    print(response['choices'][0]['message']['content'].strip())

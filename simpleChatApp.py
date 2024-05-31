# simpleChatApp.py
# This allows the user to interact with OpenAI's language model via the command line. The user
# can input prompts and receive responses from the model.

import openai
import os
import sys

from USFGenAI import ask_question

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

conversation = []

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    response = ask_question(conversation, user_prompt, "You are a helpful assistant.",
                            settings={"model": "gpt-3.5-turbo", }
                            )
    answer = response['reply']
    conversation = response['conversation']
    print("Response:\n" + answer)
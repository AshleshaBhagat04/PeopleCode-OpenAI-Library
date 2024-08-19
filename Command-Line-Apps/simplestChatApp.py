# simpleChatApp.py
# This allows the user to interact with OpenAI's language model via the command line. The user
# can input prompts and receive responses from the model.

import sys
import os

sys.path.append("..")
from PeopleCodeOpenAI import OpenAI_Conversation

# Load API key from environment variable
api_key_env = os.getenv('OPENAI_API_KEY')
if not api_key_env:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

# Initialize OpenAI_Conversation with selected model
conversation_manager = OpenAI_Conversation(api_key=api_key_env, model="gpt-4")

instructions = "You are a helpful assistant."

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt. Type 'exit' to quit: ").strip().lower()
    if user_prompt == "exit":
        sys.exit(0)

    # Get response from OpenAI model
    last_response = conversation_manager.ask_question(instructions, user_prompt)

    # Display the response
    print("Response:\n" + last_response)

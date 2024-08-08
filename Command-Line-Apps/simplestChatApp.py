# simpleChatApp.py
# This allows the user to interact with OpenAI's language model via the command line. The user
# can input prompts and receive responses from the model.

import sys
import os

sys.path.append("..")
from PeopleCodeOpenAI import OpenAI_Conversation

# Load API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

# Initialize OpenAI_Conversation with selected model
conversation_manager = OpenAI_Conversation(api_key=api_key, model="gpt-4")

instructions = "You are a helpful assistant."
conversation = []

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt. Type 'exit' to quit: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(0)

    # Get response from OpenAI model
    response_dict = conversation_manager.ask_question(instructions, user_prompt)

    # Extract the reply from the response dictionary
    last_response = response_dict.get('reply', 'No response received.')

    # Update the conversation history
    conversation.append({"role": "user", "content": user_prompt})
    conversation.append({"role": "assistant", "content": last_response})

    # Display the response
    print("Response:\n" + last_response)

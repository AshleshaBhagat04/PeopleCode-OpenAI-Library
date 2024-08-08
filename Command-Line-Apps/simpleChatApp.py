# simpleChatApp.py
# This allows the user to interact with OpenAI's language model via the command line. The user
# can input prompts and receive responses from the model.

import sys
import os

sys.path.append("..")
from PeopleCodeOpenAI import OpenAI_Conversation

# Define available models
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
print("Available models:")
for idx, model in enumerate(model_options, start=1):
    print(f"{idx}. {model}")

# Select model with default
selected_model = model_options[0]
try:
    model_choice = input("Select the model to use (1-3) or press enter to use the default: ").strip()
    if model_choice.isdigit() and 1 <= int(model_choice) <= len(model_options):
        selected_model = model_options[int(model_choice) - 1]
    else:
        print("Invalid choice. Using default model.")
except ValueError:
    print("Using default model.")

# Load API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

# Initialize OpenAI_Conversation
conversation_manager = OpenAI_Conversation(api_key=api_key, model=selected_model)

instructions = "You are a helpful assistant."

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt. Type 'exit' to quit: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(0)

    # Get response from OpenAI model
    response_dict = conversation_manager.ask_question(instructions, user_prompt)

    # Extract the reply from the response dictionary
    response = response_dict.get('reply', 'No response received.')

    # Display the response
    print("Response:\n" + response)

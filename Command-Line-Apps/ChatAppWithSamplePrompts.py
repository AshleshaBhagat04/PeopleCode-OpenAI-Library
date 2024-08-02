# chatAppWithSamplePrompts.py
# This interacts with the OpenAI API to facilitate a conversation through the command
# line. Users can ask questions, generate prompts, and get follow-up questions.

import sys
import os

sys.path.append("..")
from PeopleCodeOpenAI import OpenAI_Conversation

# Load API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

# Define available models
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
print("Available models:")
for idx, model in enumerate(model_options, start=1):
    print(f"{idx}. {model}")

# Select model with default
selected_model = model_options[0]
try:
    model_choice = int(input("Select the model to use (1-3) or press enter to use the default: ").strip())
    if 1 <= model_choice <= len(model_options):
        selected_model = model_options[model_choice - 1]
    else:
        print("Invalid choice. Using default model.")
except ValueError:
    print("Using default model.")

# Initialize OpenAI_Conversation with selected model
conversation_manager = OpenAI_Conversation(api_key=api_key, model=selected_model)

instructions = "You are a helpful assistant."
conversation = conversation_manager.get_conversation()

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt or type 'generate' to create a new prompt. Type 'exit' to quit: ")
    system_prompt = "You are a helpful assistant."
    if user_prompt.strip().lower() == "exit":
        sys.exit(0)
    elif user_prompt.strip().lower() == "generate":
        prompt_context = input("Enter the context for generating a prompt: ")
        generated_prompts = conversation_manager.generate_sample_prompts(prompt_context, 1, 25)
        print("Generated Prompts:")
        for idx, question in enumerate(generated_prompts, start=1):
            print(f"{idx}. {question}")
        user_prompt = generated_prompts[0]
    else:
        system_prompt = input("Enter a potential system prompt or press enter to use the default: ")
        if not system_prompt.strip():
            system_prompt = "You are a very helpful assistant."

    # Get response from OpenAI model
    response_dict = conversation_manager.ask_question(system_prompt, user_prompt, includePrevConvo=True)

    # Extract the reply from the response dictionary
    answer = response_dict.get('reply', 'No response received.')

    # Display the response
    print("Response:\n" + answer)

    followup_qs = conversation_manager.generate_followups(user_prompt, answer, 3, 25)
    print("Follow-up Questions:")
    for idx, question in enumerate(followup_qs, start=1):
        print(f"{question}")

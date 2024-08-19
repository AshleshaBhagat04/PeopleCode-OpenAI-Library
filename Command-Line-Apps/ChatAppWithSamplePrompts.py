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
    model_choice = input("Select the model to use (1-3) or press enter to use the default: ").strip()
    if model_choice:
        model_choice = int(model_choice)
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
    system_prompt = "You are a very helpful assistant."
    user_prompt = input("Enter a prompt or type 'generate' to create a new prompt. Type 'exit' to quit: ").strip()

    if user_prompt.lower() == "exit":
        sys.exit(0)
    elif user_prompt.lower() == "generate":
        prompt_context = input("Enter the context for generating a prompt: ").strip()
        generated_prompts = conversation_manager.generate_sample_prompts(prompt_context, 1, 25)
        print("Generated Prompts:")
        for idx, question in enumerate(generated_prompts, start=1):
            print(f"{question}")
        user_prompt = generated_prompts[0] if generated_prompts else ""
    else:
        system_prompt = input("Enter a potential system prompt or press enter to use the default: ").strip()
        if not system_prompt:
            system_prompt = "You are a very helpful assistant."

    # Get response from OpenAI model
    response_dict = conversation_manager.ask_question(system_prompt, user_prompt)

    # Extract the reply from the response dictionary
    answer = response_dict.get('reply', 'No response received.')

    # Display the response
    print("Response:\n" + answer)

    print("Follow-up Questions:")
    # Generate follow-up questions
    followup_qs = conversation_manager.generate_followups(user_prompt, answer, 3, 25)
    for idx, question in enumerate(followup_qs, start=1):
        print(f"{question}")

# chatAppWithSamplePrompts.py
# This interacts with the OpenAI API to facilitate a conversation through the command
# line. Users can ask questions, generate prompts, and get follow-up questions.

import sys
import os

# Add parent directory to sys.path to import USFGenAI module
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from USFGenAI import *

# Define available models
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
print("Available models:")
for idx, model in enumerate(model_options, start=1):
    print(f"{idx}. {model}")

# Select model with default
selected_model = model_options[0]
try:
    model_choice = int(input("Select the model to use or press enter to use the default: ").strip())
    if 1 <= model_choice <= len(model_options):
        selected_model = model_options[model_choice - 1]
    else:
        print("Invalid choice. Using default model.")
except ValueError:
    print("Using default model.")
set_model(selected_model)

conversation = []

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt or type 'generate' to create a new prompt. Type 'exit' to quit: ")
    system_prompt = ""
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    elif user_prompt.strip().lower() == "generate":
        prompt_context = input("Enter the context for generating a prompt: ")
        generated_prompts = generate_sample_prompts(prompt_context, 1, 25)
        print("Generated Prompts:")
        for idx, question in enumerate(generated_prompts, start=1):
            print(f"{idx}. {question}")
        user_prompt = generated_prompts[0]  # Select the first generated prompt
    else:
        system_prompt = input("Enter a potential system prompt or press enter to use the default: ")
        if not system_prompt.strip():
            system_prompt = "You are a very helpful assistant."

    response = ask_question(conversation, user_prompt, system_prompt)
    answer = response['reply']
    conversation = response['conversation']
    print("Response:\n" + answer)

    followup_qs = generate_followups(user_prompt, answer, 3, 25)
    print("Follow-up Questions:")
    for idx, question in enumerate(followup_qs, start=1):
        print(f"{question}")

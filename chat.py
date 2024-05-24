import sys
import os
from chatfunctions import *

api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

convo_dict = {}
latest_question = ""
latest_answer = ""

model_options = ["gpt-3.5-turbo", "gpt-4"]
print("Available models:")
for idx, model in enumerate(model_options, start=1):
    print(f"{idx}. {model}")
model_choice = input("Select the model to use: ").strip()

try:
    model_idx = int(model_choice) - 1
    if 0 <= model_idx < len(model_options):
        selected_model = model_options[model_idx]
    else:
        print("Invalid choice. Using default model.")
        selected_model = model_options[0]
except ValueError:
    print("Invalid input. Using default model.")
    selected_model = model_options[0]

settings = {"model": selected_model}

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt or type 'generate' to create a new prompt. Type 'exit' to quit: ")
    system_prompt = ""
    num_samples = int(input("Enter the number of follow-up questions to generate: "))
    max_words = int(input("Enter the maximum number of words for questions and prompts: "))

    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    elif user_prompt.strip().lower() == "generate":
        prompt_context = input("Enter the context for generating a prompt: ")
        user_prompt = generate_prompt(prompt_context, max_words, settings)
        print("Generated prompt: " + user_prompt)
    else:
        system_prompt = input("Enter a system prompt or press enter to use default: ")
        if not system_prompt.strip():
            system_prompt = "You are a very helpful assistant."

    chat_response = ask_question(user_prompt, system_prompt, settings)
    answer = chat_response['choices'][0]['message']['content'].strip()
    convo_dict[user_prompt] = answer
    latest_question = user_prompt
    latest_answer = answer

    print("Response:\n" + answer)

    latest_question, latest_answer = handle_followups(convo_dict, latest_question, latest_answer, system_prompt, num_samples, max_words, settings)

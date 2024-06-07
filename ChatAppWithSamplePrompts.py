# chatAppWithSamplePrompts.py
# This interacts with the OpenAI API to facilitate a conversation through the command
# line. Users can ask questions, generate prompts, and get follow-up questions.


from USFGenAI import *

# Define available models
model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
print("Available models:")
for idx, model in enumerate(model_options, start=1):
    print(f"{idx}. {model}")

# Select model with default
selected_model = model_options[0]
try:
    model_choice = int(input("Select the model to use: ").strip())
    if 1 <= model_choice <= len(model_options):
        selected_model = model_options[model_choice - 1]
    else:
        print("Invalid choice. Using default model.")
except ValueError:
    print("Invalid input. Using default model.")
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
        user_prompt = generate_prompt(prompt_context, 25)
        print("Generated prompt: " + user_prompt)
    else:
        system_prompt = input("Enter a potential system prompt or press enter to use default: ")
        if not system_prompt.strip():
            system_prompt = "You are a very helpful assistant."
    response = ask_question(conversation, user_prompt, system_prompt)
    answer = response['reply']
    conversation = response['conversation']
    print("Response:\n" + answer)

    followup_qs = generate_followups(user_prompt, answer, 3, 25)
    print("Follow-up Questions:")
    for idx, question in enumerate(followup_qs):
        print(f"{question}")

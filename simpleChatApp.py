# simpleChatApp.py
# This allows the user to interact with OpenAI's language model via the command line. The user
# can input prompts and receive responses from the model.


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
    user_prompt = input("Enter a prompt. Type 'exit' to quit: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    response = ask_question(conversation, user_prompt, "You are a helpful assistant."
                            )
    answer = response['reply']
    conversation = response['conversation']
    print("Response:\n" + answer)

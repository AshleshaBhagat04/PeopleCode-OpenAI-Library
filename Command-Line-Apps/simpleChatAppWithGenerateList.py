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
    print("\nOptions:")
    print("1. Ask a question")
    print("2. Generate a list")
    print("3. Exit")

    user_choice = input("Choose an option (1-3): ").strip()

    if user_choice == "1":
        # Ask a question
        user_prompt = input("Enter a prompt: ")
        response = conversation_manager.ask_question(instructions, user_prompt)
        print("Response:\n" + response)

    elif user_choice == "2":
        # Generate a list
        list_description = input("Enter a description for the list: ")
        num_items = int(input("Enter the number of items: "))
        max_words = int(input("Enter the maximum number of words per item: "))
        generated_list = conversation_manager.generate_list(list_description, num_items, max_words)
        print("Generated List:")
        for idx, item in enumerate(generated_list, start=1):
            print(f"{item}")

    elif user_choice == "3" or user_choice.lower() == "exit":
        # Exit the application
        print("Goodbye!")
        sys.exit(0)

    else:
        print("Invalid choice. Please try again.")

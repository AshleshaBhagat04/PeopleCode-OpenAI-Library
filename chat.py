import sys
import os
from chatfunctions import ask_question, generate_prompt, handle_followups


def main():
    # Get API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
        sys.exit(-1)

    # Define available models
    model_options = ["gpt-3.5-turbo", "gpt-4"]
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

    settings = {"model": selected_model}

    # Conversation history
    conversation = []
    latest_question = ""
    latest_answer = ""

    print("How can I help you today?")
    while True:
        user_prompt = input(
            "Enter a prompt or type 'generate' to create a new prompt. Type 'exit' to quit: ").strip().lower()

        # Handle user input
        if user_prompt == "exit":
            print("Goodbye!")
            sys.exit(0)
        elif user_prompt == "generate":
            # Generate a new prompt
            prompt_context = input("Enter the context for generating a prompt: ").strip()
            try:
                max_words = 25
                max_words = int(input("Enter the maximum number of words for the generated prompt or press enter to use default: ").strip())
                user_prompt = generate_prompt(prompt_context, max_words, settings)
                print("Generated prompt: " + user_prompt)
            except ValueError:
                print("Invalid input for maximum number of words. Please enter a valid integer.")

        # Get system prompt or use default
        system_prompt = input("Enter a system prompt or press enter to use default: ").strip()
        if not system_prompt:
            system_prompt = "You are a very helpful assistant."
        num_samples = 3
        max_words = 25
        try:
            # Get the number of follow-up questions and maximum words
            num_samples = int(input("Enter the number of follow-up questions to generate or press enter to use default: ").strip())
            max_words = int(input("Enter the maximum number of words for questions and prompts or press enter to use default: ").strip())
        except ValueError:
            print("Invalid input. Please enter valid integers for the number of follow-up questions and maximum words.")

        # Get response from the model
        response = ask_question(conversation, user_prompt, system_prompt, settings)
        answer = response['reply']
        conversation = response['conversation']
        latest_question = user_prompt
        latest_answer = answer

        print("Response:\n" + answer)

        # Handle follow-up questions
        latest_question, latest_answer, conversation = handle_followups(conversation, latest_question, latest_answer,
                                                                        system_prompt, num_samples, max_words, settings)


if __name__ == "__main__":
    main()

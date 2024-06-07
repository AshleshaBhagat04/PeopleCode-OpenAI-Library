# ChatApp.py
# This initializes the OpenAI API key and sets up conversation through the command line. It interacts
# with the user to select a model and ask questions based on the provided context. It handles model selection,
# generates prompts, and manages follow-up questions.


from USFGenAI import *


def main():
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
            user_prompt = input("Enter the context for generating a prompt: ").strip()
            try:
                max_words = 25
                max_words = int(input("Enter the maximum number of words for the generated prompt or press enter to use default: ").strip())
                user_prompt = generate_prompt(user_prompt, max_words)
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
        response = ask_question(conversation, user_prompt, system_prompt)
        answer = response['reply']
        conversation = response['conversation']
        latest_question = user_prompt
        latest_answer = answer

        print("Response:\n" + answer)

        # Handle follow-up questions
        latest_question, latest_answer, conversation = handle_followups(conversation, latest_question, latest_answer,
                                                                        system_prompt, num_samples, max_words)


if __name__ == "__main__":
    main()

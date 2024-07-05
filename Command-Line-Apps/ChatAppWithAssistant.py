# ChatAppWithAssistant.py
# This script initializes the OpenAI API key and sets up conversation through the command line. It interacts
# with the user to select a model and ask questions based on the provided context. It handles model selection,
# generates prompts, and manages follow-up questions.

import sys
sys.path.append("..")
from USFGenAI import *

# Set your OpenAI assistant ID here
ASSISTANT_ID = "asst_RRXmeNcR4UEj8YSrzOqWkJYa"


def handle_followups(conversation, latest_question, latest_answer):
    followup_questions = generate_assistant_followups(latest_question, latest_answer, 2, 6, ASSISTANT_ID)
    if followup_questions:
        print("Follow-up Questions:")
        for idx, question in enumerate(followup_questions, start=1):
            print(f"{idx}. {question}")
        choice = input("Enter the follow-up question number you want to ask (or 0 to skip): ").strip()
        try:
            choice_idx = int(choice) - 1
            if choice_idx == -1:
                return latest_question, latest_answer, conversation
            elif 0 <= choice_idx < len(followup_questions):
                user_prompt = followup_questions[choice_idx]
                response = ask_assistant_question(conversation, user_prompt, "You are a very helpful assistant.",
                                                  ASSISTANT_ID)
                latest_question = user_prompt
                latest_answer = response['reply']
                print("Response:\n" + latest_answer)
                return latest_question, latest_answer, response['conversation']
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
    return latest_question, latest_answer, conversation


def main():
    print(
        "You are talking to the book, 'Drag and Drop Coding with Thunkable' by David Wolber. Ask Professor Wolber a "
        "coding question!")

    model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
    print("Available models:")
    for idx, model in enumerate(model_options, start=1):
        print(f"{idx}. {model}")

    selected_model = model_options[0]
    model_choice = input("Select the model to use or press enter to use the default: ").strip()
    if model_choice.isdigit():
        model_choice = int(model_choice)
        if 1 <= model_choice <= len(model_options):
            selected_model = model_options[model_choice - 1]
        else:
            print("Invalid choice. Using default model.")
    else:
        print("Using default model.")
    set_model(selected_model)

    conversation = []
    latest_question = ""
    latest_answer = ""

    print("How can I help you today?")
    while True:
        user_prompt = input("Enter a prompt or type 'exit' to quit: ").strip().lower()
        if user_prompt == "exit":
            print("Goodbye!")
            sys.exit(0)

        if not user_prompt:
            print("User prompt cannot be empty. Please enter a valid prompt.")
            continue

        response = ask_assistant_question(conversation, user_prompt, "You are a very helpful assistant.", ASSISTANT_ID)
        latest_question = user_prompt
        latest_answer = response['reply']
        conversation = response['conversation']

        print("Response:\n" + latest_answer)

        latest_question, latest_answer, conversation = handle_followups(conversation, latest_question, latest_answer)


if __name__ == "__main__":
    main()
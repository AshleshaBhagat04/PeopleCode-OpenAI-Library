# ChatAppWithAssistant.py
# This script initializes the OpenAI API key and sets up conversation through the command line. It interacts
# with the user to select a model and ask questions based on the provided context. It handles model selection,
# generates prompts, and manages follow-up questions.

import sys
sys.path.append("..")
from USFGenAI import *

# Set your OpenAI assistant ID here
ASSISTANT_ID = "asst_RRXmeNcR4UEj8YSrzOqWkJYa"


def handle_followups(conversation, latest_question, latest_answer, system_prompt, num_samples, max_words):
    followup_questions = generate_assistant_followups(latest_question, latest_answer, num_samples, max_words, ASSISTANT_ID)
    if followup_questions:
        print("Follow-up Questions:")
        for idx, question in enumerate(followup_questions, start=1):
            print(f"{question}")
        choice = input("Enter the follow-up question number you want to ask (or 0 to skip): ").strip()
        try:
            choice_idx = int(choice) - 1
            if choice_idx == -1:
                return latest_question, latest_answer, conversation
            elif 0 <= choice_idx < len(followup_questions):
                user_prompt = followup_questions[choice_idx]
                response = ask_assistant_question(conversation, user_prompt, system_prompt, ASSISTANT_ID)
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
    # Define available models
    model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
    print("Available models:")
    for idx, model in enumerate(model_options, start=1):
        print(f"{idx}. {model}")

    # Select model with default
    selected_model = model_options[0]
    try:
        model_choice = input("Select the model to use or press enter to use the default: ").strip()
        if model_choice.isdigit():
            model_choice = int(model_choice)
            if 1 <= model_choice <= len(model_options):
                selected_model = model_options[model_choice - 1]
            else:
                print("Invalid choice. Using default model.")
        else:
            print("Using default model.")
    except ValueError:
        print("Using default model.")
    set_model(selected_model)

    # Conversation history
    conversation = []
    latest_question = ""
    latest_answer = ""

    print("How can I help you today?")
    while True:
        user_prompt = input("Enter a prompt or type 'generate' to create a new prompt. Type 'exit' to quit: ").strip().lower()
        system_prompt = "You are a very helpful assistant."
        if user_prompt == "exit":
            print("Goodbye!")
            sys.exit(0)
        elif user_prompt == "generate":
            user_prompt = input("Enter the context for generating a prompt: ").strip()
            if not user_prompt:
                print("Context cannot be empty. Please enter a valid context.")
                continue
            try:
                num_samples_input = input("Enter the number of sample prompts to generate: ").strip()
                num_samples = int(num_samples_input) if num_samples_input else 1

                max_words_input = input("Enter the maximum number of words for the generated prompt: ").strip()
                max_words = int(max_words_input) if max_words_input else 25

                generated_prompts = generate_assistant_sample_prompts(user_prompt, num_samples, max_words, ASSISTANT_ID)
                print(generated_prompts)
                if isinstance(generated_prompts, list) and generated_prompts:
                    print("Generated Prompts:")
                    for idx, prompt in enumerate(generated_prompts, start=1):
                        print(f"{prompt}")
                    choice = input("Enter the prompt number you want to ask: ").strip()
                    try:
                        choice_idx = int(choice) - 1
                        if choice_idx == -1:
                            return latest_question, latest_answer, conversation
                        elif 0 <= choice_idx < len(generated_prompts):
                            user_prompt = generated_prompts[choice_idx]
                        else:
                            print("Invalid choice, using the first prompt.")
                            user_prompt = generated_prompts[0]
                    except ValueError:
                        print("Invalid input.")
                else:
                    print("No prompts generated. Please try again.")
                    continue
            except ValueError:
                print("Invalid input. Please try again.")
                continue
        else:
            system_prompt = input("Enter a system prompt or press enter to use the default: ").strip()
            if not system_prompt:
                system_prompt = "You are a very helpful assistant."

        try:
            num_samples_input = input("Enter the number of follow-up questions to generate or press enter to use the default: ").strip()
            num_samples = int(num_samples_input) if num_samples_input else 3

            max_words_input = input("Enter the maximum number of words for questions and prompts or press enter to use the default: ").strip()
            max_words = int(max_words_input) if max_words_input else 25
        except ValueError:
            print("Invalid input. Using default values.")
            num_samples = 3
            max_words = 25

        if not user_prompt:
            print("User prompt cannot be empty. Please enter a valid prompt.")
            continue

        response = ask_assistant_question(conversation, user_prompt, system_prompt, ASSISTANT_ID)
        answer = response['reply']
        conversation = response['conversation']
        latest_question = user_prompt
        latest_answer = answer

        print("Response:\n" + answer)

        latest_question, latest_answer, conversation = handle_followups(conversation, latest_question, latest_answer, system_prompt, num_samples, max_words)


if __name__ == "__main__":
    main()

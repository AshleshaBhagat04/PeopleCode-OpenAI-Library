import sys
import os

sys.path.append("..")
from PeopleCodeOpenAI import OpenAI_Conversation

# Set your OpenAI assistant ID here
ASSISTANT_ID = "asst_RRXmeNcR4UEj8YSrzOqWkJYa"


def handle_followups(conversation_manager, latest_question, latest_answer, assistant_id):
    followup_questions = conversation_manager.generate_assistant_followups(
        latest_question, latest_answer, 3, 25, assistant_id
    )
    if followup_questions:
        print("Follow-up Questions:")
        for idx, question in enumerate(followup_questions, start=1):
            print(f"{question}")
        choice = input("Enter the follow-up question number you want to ask (or 0 to skip): ").strip()
        try:
            choice_idx = int(choice) - 1
            if choice_idx == -1:
                return latest_question, latest_answer, conversation_manager.get_conversation()
            elif 0 <= choice_idx < len(followup_questions):
                user_prompt = followup_questions[choice_idx]
                response = conversation_manager.ask_question(
                    "You are a very helpful assistant.", user_prompt, includePrevConvo=True
                )
                latest_question = user_prompt
                latest_answer = response['reply']
                print("Response:\n" + latest_answer)
                return latest_question, latest_answer, response['conversation']
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
    return latest_question, latest_answer, conversation_manager.get_conversation()


def main():
    print(
        "You are talking to the book, 'Drag and Drop Coding with Thunkable' by David Wolber. Ask Professor Wolber a "
        "coding question!"
    )

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

    # Load API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
        sys.exit(-1)

    # Initialize OpenAI_Conversation with selected model
    conversation_manager = OpenAI_Conversation(api_key=api_key, model=selected_model)

    print("How can I help you today?")
    while True:
        user_prompt = input("Enter a prompt or type 'exit' to quit: ").strip().lower()
        if user_prompt == "exit":
            print("Goodbye!")
            sys.exit(0)

        if not user_prompt:
            print("User prompt cannot be empty. Please enter a valid prompt.")
            continue

        response = conversation_manager.ask_question(
            "You are a very helpful assistant.", user_prompt, ASSISTANT_ID
        )
        latest_question = user_prompt
        latest_answer = response['reply']
        conversation = response['conversation']

        print("Response:\n" + latest_answer)

        latest_question, latest_answer, conversation = handle_followups(
            conversation_manager, latest_question, latest_answer, ASSISTANT_ID
        )


if __name__ == "__main__":
    main()

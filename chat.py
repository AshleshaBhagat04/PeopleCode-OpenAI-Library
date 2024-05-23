import sys
from chatfunctions import *

openai.api_key = 'sk-proj-C41dhuNFgtqVNy7WwiIIT3BlbkFJrSlVU2qLpLWjIvUyaahA'

convo_dict = {}
latest_question = ""
latest_answer = ""

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt or type 'generate' to create a new prompt. Type 'exit' to quit: ")
    system_prompt = ""
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    elif user_prompt.strip().lower() == "generate":
        prompt_context = input("Enter the context for generating a prompt: ")
        user_prompt = generate_prompt(prompt_context)
        print("Generated prompt: " + user_prompt)
    else:
        system_prompt = input("Enter a system prompt or press enter to use default: ")
        if not system_prompt.strip():
            system_prompt = "You are a very helpful assistant."

    chat_response = ask_question(user_prompt, system_prompt)
    answer = chat_response['choices'][0]['message']['content'].strip()
    convo_dict[user_prompt] = answer
    latest_question = user_prompt
    latest_answer = answer

    print("Response:\n" + answer)

    followup_questions = generate_followups(latest_question, latest_answer)

    if followup_questions:
        print("Follow-up Questions:")
        for idx, questions in enumerate(followup_questions):
            print(f"{questions}")
        choice = input("Enter the follow-up question number you want to ask (or 0 to skip): ")
        try:
            choice_idx = int(choice) - 1
            if choice_idx == -1:
                continue
            elif 0 <= choice_idx < len(followup_questions):
                user_prompt = followup_questions[choice_idx]
                chat_response = ask_question(user_prompt, system_prompt)
                answer = chat_response['choices'][0]['message']['content'].strip()
                convo_dict[user_prompt] = answer
                latest_question = user_prompt
                latest_answer = answer
                print("Response:\n" + answer)
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
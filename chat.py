import openai
import sys

openai.api_key = 'sk-proj-C41dhuNFgtqVNy7WwiIIT3BlbkFJrSlVU2qLpLWjIvUyaahA'

convo_dict = {}
recent_question = ""
recent_answer = ""


def ask_question(question, instructions):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": question}
        ]
    )
    return response


def generate_prompt(context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Generate a prompt based on the context provided below."},
            {"role": "user", "content": context}
        ]
    )
    prompt = response['choices'][0]['message']['content'].strip()
    return prompt


def generate_followups(question, answer):
    convo_history = f"User: {question}\nAssistant: {answer}\n"
    followups = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Generate 3 follow-up questions that the user could choose to ask based on the conversation history provided below."},
            {"role": "user", "content": convo_history}
        ]
    )
    questions = followups['choices'][0]['message']['content'].strip().split('\n')
    return questions


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
    recent_question = user_prompt
    recent_answer = answer

    print("Response:\n" + answer)

    followup_questions = generate_followups(recent_question, recent_answer)

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
                recent_question = user_prompt
                recent_answer = answer
                print("Response:\n" + answer)
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
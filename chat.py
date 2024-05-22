import openai
import sys

openai.api_key = 'sk-proj-C41dhuNFgtqVNy7WwiIIT3BlbkFJrSlVU2qLpLWjIvUyaahA'

convo_dict = {}


def ask_question(question, instructions):
    if instructions is None:
        instructions = "You are a helpful assistant."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": question}
        ]
    )
    return response


def generate_followups():
    convo_history = ""
    for q, a in convo_dict.items():
        convo_history += f"User: {q}\nAssistant: {a}\n"

    followups = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Generate 3 follow-up questions that the user could choose from to askbased on the conversation history provided below."},
            {"role": "user", "content": convo_history}
        ]
    )
    print("Follow-up questions:\n" + followups['choices'][0]['message']['content'].strip())


print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt: ")
    system_prompt = input("Enter a potential system prompt: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    answer = ask_question(user_prompt, system_prompt)
    convo_dict[user_prompt] = answer['choices'][0]['message']['content'].strip()

    print("Response:\n" + (answer['choices'][0]['message']['content'].strip()))
    generate_followups()

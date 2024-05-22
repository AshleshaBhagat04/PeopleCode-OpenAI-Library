import openai
import sys

openai.api_key = 'sk-proj-C41dhuNFgtqVNy7WwiIIT3BlbkFJrSlVU2qLpLWjIvUyaahA'

convo_dict = {}


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



def generate_followups():
    convo_history = ""
    for q, a in convo_dict.items():
        convo_history += f"User: {q}\nAssistant: {a}\n"

    followups = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Generate 3 follow-up questions that the user could choose from to ask based on the conversation history."},
            {"role": "user", "content": convo_history}
        ]
    )
    print("Follow-up questions:\n" + followups['choices'][0]['message']['content'].strip())


print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt or type 'generate' to create a new prompt. Type 'exit' to quit: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    elif user_prompt.strip().lower() == "generate":
        context = input("Enter the context for generating a prompt: ")
        user_prompt = generate_prompt(context)
        print("Generated prompt: " + user_prompt)
    else:
        system_prompt = input("Enter a potential system prompt or press enter to use default: ")
        if not system_prompt.strip():
            system_prompt = "You are a helpful assistant."
    answer = ask_question(user_prompt, system_prompt)
    convo_dict[user_prompt] = answer['choices'][0]['message']['content'].strip()

    print("Response:\n" + (answer['choices'][0]['message']['content'].strip()))
    generate_followups()
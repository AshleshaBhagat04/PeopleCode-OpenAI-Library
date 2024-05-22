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


def generate_followups():
    convo_history = ""
    for q, a in convo_dict.items():
        convo_history += f"User: {q}\nAssistant: {a}\n"

    followups = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Generate 3 follow-up questions that the user could choose to ask based on the "
                        "conversation history provided below."},
            {"role": "user", "content": convo_history}
        ]
    )
    print("Follow-up questions:\n" + followups['choices'][0]['message']['content'].strip())


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
        system_prompt = input("Enter a potential system prompt or press enter to use default: ")
        if not system_prompt.strip():
            system_prompt = "You are a very helpful assistant."
    chat_response = ask_question(user_prompt, system_prompt)
    convo_dict[user_prompt] = chat_response['choices'][0]['message']['content'].strip()

    print("Response:\n" + (chat_response['choices'][0]['message']['content'].strip()))
    generate_followups()
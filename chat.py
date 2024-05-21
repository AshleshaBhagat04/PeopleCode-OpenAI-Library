import openai
import sys

openai.api_key = 'sk-proj-C41dhuNFgtqVNy7WwiIIT3BlbkFJrSlVU2qLpLWjIvUyaahA'


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


print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt: ")
    system_prompt = input("Enter a potential system prompt: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    answer = ask_question(user_prompt, system_prompt)

    print("Response: ")
    print(answer['choices'][0]['message']['content'].strip())

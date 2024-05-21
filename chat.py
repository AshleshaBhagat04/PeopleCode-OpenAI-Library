import openai
import sys

openai.api_key = 'sk-proj-C41dhuNFgtqVNy7WwiIIT3BlbkFJrSlVU2qLpLWjIvUyaahA'

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt}
        ]
    )

    print("Response: ")
    print(response['choices'][0]['message']['content'].strip())

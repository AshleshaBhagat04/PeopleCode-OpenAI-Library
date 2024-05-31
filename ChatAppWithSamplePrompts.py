# chatAppWithSamplePrompts.py
# This interacts with the OpenAI API to facilitate a conversation through the command
# line. Users can ask questions, generate prompts, and get follow-up questions.


import os
import sys

from USFGenAI import generate_prompt, ask_question, generate_followups

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

conversation = []

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt or type 'generate' to create a new prompt. Type 'exit' to quit: ")
    system_prompt = ""
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    elif user_prompt.strip().lower() == "generate":
        prompt_context = input("Enter the context for generating a prompt: ")
        user_prompt = generate_prompt(user_prompt, 25, settings={"model": "gpt-3.5-turbo"})
        print("Generated prompt: " + user_prompt)
    else:
        system_prompt = input("Enter a potential system prompt or press enter to use default: ")
        if not system_prompt.strip():
            system_prompt = "You are a very helpful assistant."
    response = ask_question(conversation, user_prompt, system_prompt, settings={"model": "gpt-3.5-turbo"})
    answer = response['reply']
    conversation = response['conversation']
    print("Response:\n" + answer)

    followup_qs = generate_followups(user_prompt, answer, 3, 25, settings={"model": "gpt-3.5-turbo"})
    print("Follow-up Questions:")
    for idx, question in enumerate(followup_qs):
        print(f"{question}")

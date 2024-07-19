# simpleChatApp.py
# This allows the user to interact with OpenAI's language model via the command line. The user
# can input prompts and receive responses from the model.

import sys
sys.path.append("..")
from USFGenAI import *

set_model("gpt-4") #

conversation = []

print("How can I help you today?")
while True:
    user_prompt = input("Enter a prompt. Type 'exit' to quit: ")
    if user_prompt.strip().lower() == "exit":
        sys.exit(-1)
    response = ask_question(conversation, user_prompt, "You are a helpful assistant.")
    lastResponse = response['reply']
    conversation = response['conversation']
    print("Response:\n" + lastResponse)

import sys
import os
from chatfunctions import *

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

conversation = []

settings={"model": "gpt-3.5-turbo"}
context = "Ella Josephine Baker (December 13, 1903 – December 13, 1986) was an African-American civil rights and human rights activist. She was a largely behind-the-scenes organizer whose career spanned more than five decades. In New York City and the South, she worked alongside some of the most noted civil rights leaders of the 20th century, including W. E. B. Du Bois, Thurgood Marshall, A. Philip Randolph, and Martin Luther King Jr. She also mentored many emerging activists, such as Diane Nash, Stokely Carmichael, and Bob Moses, as leaders in the Student Nonviolent Coordinating Committee (SNCC). Ask her a question."
system_prompt = "Answer from the perspective of Ella Baker. Here is some context: " + context

prompt1 = generate_prompt(context, 25, settings)
prompt2 = generate_prompt(context, 25, settings)
prompt3 = generate_prompt(context, 25, settings)

print(prompt1)
print(prompt2)
print(prompt3)

answer = ""

choice = int(input("Enter the question number you want to ask (or 0 to skip): ").strip())
if choice == 1:
    response = ask_question(conversation, prompt1, system_prompt, settings)
    answer = response['reply']
    conversation = response['conversation']
    latest_question = prompt1
    latest_answer = answer
elif choice == 2:
    response = ask_question(conversation, prompt2, system_prompt, settings)
    answer = response['reply']
    conversation = response['conversation']
    latest_question = prompt2
    latest_answer = answer
elif choice == 3:
    response = ask_question(conversation, prompt3, system_prompt, settings)
    answer = response['reply']
    conversation = response['conversation']
    latest_question = prompt3
    latest_answer = answer

print("Response:\n" + answer)


latest_question, latest_answer, conversation = handle_followups(conversation, latest_question, latest_answer,
                                                                system_prompt, 3, 25, settings)

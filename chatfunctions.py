import openai

settings = {
    "model": "gpt-3.5-turbo"
}


def ask_question(question, instructions):
    response = openai.ChatCompletion.create(
        model=settings["model"],
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": question}
        ]
    )
    return response


def generate_prompt(context):
    response = openai.ChatCompletion.create(
        model=settings["model"],
        messages=[
            {"role": "system",
             "content": "Generate a prompt based on the context provided below."},
            {"role": "user", "content": context}
        ]
    )
    prompt = response['choices'][0]['message']['content'].strip()
    return prompt


def generate_followups(question, response):
    convo_history = f"User: {question}\nAssistant: {response}\n"
    followups = openai.ChatCompletion.create(
        model=settings["model"],
        messages=[
            {"role": "system",
             "content": "Generate 3 follow-up questions that the user could choose to ask based on the conversation history provided below."},
            {"role": "user", "content": convo_history}
        ]
    )
    followup_qs = followups['choices'][0]['message']['content'].strip().split('\n')
    return followup_qs

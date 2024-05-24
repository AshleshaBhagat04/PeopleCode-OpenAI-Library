import openai


def ask_question(question, instructions, settings):
    response = openai.ChatCompletion.create(
        model=settings["model"],
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": question}
        ]
    )
    return response


def generate_prompt(context, max_words, settings):
    response = openai.ChatCompletion.create(
        model=settings["model"],
        messages=[
            {"role": "system",
             "content": f"Generate a prompt based on the context provided below in no more than {max_words} words."},
            {"role": "user", "content": context}
        ]
    )
    prompt = response['choices'][0]['message']['content'].strip()
    return prompt


def generate_followups(question, response, num_samples, max_words, settings):
    convo_history = f"User: {question}\nAssistant: {response}\n"
    followups = openai.ChatCompletion.create(
        model=settings["model"],
        messages=[
            {"role": "system",
             "content": f"Generate {num_samples} follow-up questions that the user could choose to ask based on the conversation history provided below. Each follow-up question should be no more than {max_words} words."},
            {"role": "user", "content": convo_history}
        ]
    )
    followup_qs = followups['choices'][0]['message']['content'].strip().split('\n')
    return followup_qs


def handle_followups(convo_dict, latest_question, latest_answer, system_prompt, num_samples, max_words, settings):
    followup_questions = generate_followups(latest_question, latest_answer, num_samples, max_words, settings)

    if followup_questions:
        print("Follow-up Questions:")
        for idx, question in enumerate(followup_questions):
            print(f"{question}")
        choice = input("Enter the follow-up question number you want to ask (or 0 to skip): ")
        try:
            choice_idx = int(choice) - 1
            if choice_idx == -1:
                return latest_question, latest_answer
            elif 0 <= choice_idx < len(followup_questions):
                user_prompt = followup_questions[choice_idx]
                chat_response = ask_question(user_prompt, system_prompt, settings)
                answer = chat_response['choices'][0]['message']['content'].strip()
                convo_dict[user_prompt] = answer
                latest_question = user_prompt
                latest_answer = answer
                print("Response:\n" + answer)
                return latest_question, latest_answer
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
    return latest_question, latest_answer

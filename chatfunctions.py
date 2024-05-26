import openai


def ask_question(conversation, question, instructions, settings):
    """
    Asks a question to the OpenAI Chat API

    Args:
        conversation (list): The conversation history.
        question (str): The question to ask.
        instructions (str): Instructions or system prompt for the chat.
        settings (dict): The model to use.

    Returns:
        dict: The response from the OpenAI Chat API,
    """
    conversation.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
        model=settings["model"],
        messages=[
                     {"role": "system", "content": instructions}
                 ] + conversation
    )
    answer = response['choices'][0]['message']['content'].strip()
    conversation.append({"role": "assistant", "content": answer})
    return {"reply": answer, "conversation": conversation}


def generate_prompt(context, max_words, settings):
    """
    Generates a prompt based on the context.

    Args:
        context (str): The context for generating the prompt.
        max_words (int): Maximum number of words for the prompt.
        settings (dict): The model to use.

    Returns:
        str: The prompt.
    """
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


def generate_followups(conversation, question, response, num_samples, max_words, settings):
    """
    Generates follow-up questions.

    Args:
        conversation (list): The conversation history.
        question (str): The previous question asked.
        response (str): The response to the previous question.
        num_samples (int): Number of follow-up questions to generate.
        max_words (int): Maximum number of words for each follow-up question.
        settings (dict): The model to use.

    Returns:
        list: A list of follow-up questions.
    """
    recent_history = f"User: {question}\nAssistant: {response}\n"
    convo_history = conversation + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": response}
    ]
    followups = openai.ChatCompletion.create(
        model=settings["model"],
        messages=[
            {"role": "system",
             "content": f"Generate {num_samples} follow-up questions that the user could choose to ask based on the conversation. Each follow-up question should be no more than {max_words} words."},
            {"role": "user",
             "content": recent_history}
        ]
    )
    followup_qs = followups['choices'][0]['message']['content'].strip().split('\n')
    return followup_qs


def handle_followups(conversation, latest_question, latest_answer, system_prompt, num_samples, max_words, settings):
    """
    Handles the process of presenting and selecting follow-up questions.

    Args:
        conversation (list): The conversation history.
        latest_question (str): The latest question asked.
        latest_answer (str): The response to the latest question.
        system_prompt (str): The system prompt.
        num_samples (int): Number of follow-up questions to generate.
        max_words (int): Maximum number of words for each follow-up question.
        settings (dict): The model to use.

    Returns:
        tuple: A tuple with the updated latest question and response, and the conversation history.
    """
    followup_questions = generate_followups(conversation, latest_question, latest_answer, num_samples, max_words,
                                            settings)

    if followup_questions:
        print("Follow-up Questions:")
        for idx, question in enumerate(followup_questions):
            print(f"{question}")
        choice = input("Enter the follow-up question number you want to ask (or 0 to skip): ").strip()
        try:
            choice_idx = int(choice) - 1
            if choice_idx == -1:
                return latest_question, latest_answer, conversation
            elif 0 <= choice_idx < len(followup_questions):
                user_prompt = followup_questions[choice_idx]
                response = ask_question(conversation, user_prompt, system_prompt, settings)
                latest_question = user_prompt
                latest_answer = response['reply']
                print("Response:\n" + latest_answer)
                return latest_question, latest_answer, response['conversation']
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
    return latest_question, latest_answer, conversation

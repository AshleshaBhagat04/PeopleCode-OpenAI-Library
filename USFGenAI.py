from openai import OpenAI

client = OpenAI()
settings = {}


def set_api_key(api_key):
    """
    Sets the API key for the OpenAI API.

    Args:
        api_key (str): The API key.
    """
    client.api_key = api_key


def set_model(model_name):
    """
    Sets the model for the OpenAI API.

    Args:
        model_name (str): The model name.
    """
    global settings
    settings = {"model": model_name}


def ask_question(conversation, question, instructions):
    """
    Asks a question to the OpenAI Chat API.

    Args:
        conversation (list): The conversation history.
        question (str): The question to ask.
        instructions (str): Instructions or system prompt for the chat.

    Returns:
        dict: The response from the OpenAI Chat API,
              containing the reply and updated conversation.
    """
    conversation.append({"role": "user", "content": question})
    response = client.chat.completions.create(model=settings["model"],
                                              messages=[
                                                           {"role": "system", "content": instructions}
                                                       ] + conversation)
    (dict(response).get('usage'))
    (response.model_dump_json(indent=2))
    answer = response.choices[0].message.content.strip()
    conversation.append({"role": "assistant", "content": answer})
    return {"reply": answer, "conversation": conversation}


def generate_prompt(context, max_words):
    """
    Generates a prompt based on the context.

    Args:
        context (str): The context for generating the prompt.
        max_words (int): Maximum number of words for the prompt.

    Returns:
        str: The generated prompt.
    """
    response = client.chat.completions.create(model=settings["model"],
                                              messages=[
                                                  {"role": "system",
                                                   "content": f"Generate a prompt in no more than {max_words} words from the user perspective based on the context provided below."},
                                                  {"role": "user", "content": context}
                                              ])
    (dict(response).get('usage'))
    (response.model_dump_json(indent=2))
    prompt = response.choices[0].message.content.strip()
    return prompt


def generate_followups(question, response, num_samples, max_words):
    """
    Generates follow-up questions.

    Args:
        question (str): The previous question asked.
        response (str): The response to the previous question.
        num_samples (int): Number of follow-up questions to generate.
        max_words (int): Maximum number of words for each follow-up question.

    Returns:
        list: A list of follow-up questions.
    """
    recent_history = f"User: {question}\nAssistant: {response}\n"
    followups = client.chat.completions.create(model=settings["model"],
                                               messages=[
                                                   {"role": "system",
                                                    "content": f"Generate {num_samples} follow-up questions from the user perspective based on the conversation. Each follow-up question should be no more than {max_words} words."},
                                                   {"role": "user", "content": recent_history}
                                               ])
    (dict(followups).get('usage'))
    (followups.model_dump_json(indent=2))
    followup_qs = followups.choices[0].message.content.strip().split('\n')
    return followup_qs


def handle_followups(conversation, latest_question, latest_answer, system_prompt, num_samples, max_words):
    """
    Handles the process of presenting and selecting follow-up questions.

    Args:
        conversation (list): The conversation history.
        latest_question (str): The latest question asked.
        latest_answer (str): The response to the latest question.
        system_prompt (str): The system prompt.
        num_samples (int): Number of follow-up questions to generate.
        max_words (int): Maximum number of words for each follow-up question.

    Returns:
        tuple: A tuple with the updated latest question and response, and the conversation history.
    """
    followup_questions = generate_followups(latest_question, latest_answer, num_samples, max_words)

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
                response = ask_question(conversation, user_prompt, system_prompt)
                latest_question = user_prompt
                latest_answer = response['reply']
                print("Response:\n" + latest_answer)
                return latest_question, latest_answer, response['conversation']
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")
    return latest_question, latest_answer, conversation

def text_to_speech(text):
    """
    Converts text to speech using OpenAI's TTS model.

    Args:
        text (str): The text to convert to speech.
    """
    speech_file_path = Path(__file__).parent / "response.mp3"
    response = openai.Audio.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_file_path)
    return response

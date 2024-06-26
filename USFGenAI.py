import os
import sys
from pathlib import Path
from openai import OpenAI

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
    sys.exit(-1)

client = OpenAI(api_key=api_key)
settings = {}


def set_model(model_name):
    """
    Sets the model for the OpenAI API.

    Args:
        model_name (str): The model name.
    """
    global settings
    settings = {"model": model_name}


def ask_question(conversation, question, instructions, assistant_id=None):
    """
    Asks a question to the OpenAI Chat API.

    Args:
        conversation (list): The conversation history.
        question (str): The question to ask.
        instructions (str): Instructions or system prompt for the chat.
        assistant_id (str): The ID of the existing assistant.

    Returns:
        dict: The response from the OpenAI Chat API,
              containing the reply and updated conversation.
    """
    conversation.append({"role": "user", "content": question})

    if assistant_id is not None:
        return __ask_assistant(conversation, question, instructions, assistant_id)
    else:
        return __ask_openai(conversation, instructions)


def __ask_assistant(conversation, question, instructions, assistant_id):
    """
    Private function to ask a question to an OpenAI Assistant with a specified ID.

    Args:
        conversation (list): The conversation history.
        question (str): The question to ask.
        instructions (str): Instructions or system prompt for the chat.
        assistant_id (str): The ID of the existing assistant.

    Returns:
        dict: The response from the OpenAI Chat API,
              containing the reply and updated conversation.
    """
    # Create a new thread
    thread = client.beta.threads.create()

    # Add the user's question to the thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )

    # Run the assistant
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions=instructions
    )

    if run.status == 'completed':
        # List all messages in the thread
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        # Get the latest assistant message
        latest_message = None
        for message in messages.data:
            if message.role == "assistant":
                latest_message = message.content[0].text.value

        if latest_message:
            return {"reply": latest_message, "conversation": conversation}
        else:
            return {"reply": None, "conversation": conversation}
    else:
        return {"reply": None, "conversation": conversation}


def __ask_openai(conversation, instructions):
    """
    Private function to ask a question to the OpenAI Chat API.

    Args:
        conversation (list): The conversation history.
        instructions (str): Instructions or system prompt for the chat.

    Returns:
        dict: The response from the OpenAI Chat API,
              containing the reply and updated conversation.
    """
    response = client.chat.completions.create(model=settings["model"],
                                              messages=[
                                                  {"role": "system", "content": instructions}
                                              ] + conversation)
    (dict(response).get('usage'))
    (response.model_dump_json(indent=2))
    answer = response.choices[0].message.content.strip()
    conversation.append({"role": "assistant", "content": answer})
    return {"reply": answer, "conversation": conversation}


def ask_assistant_question(conversation, question, instructions, assistant_id):
    """
    Asks a question to an OpenAI Assistant with a specified ID.

    Args:
        question (str): The question to ask.
        instructions (str): Instructions or system prompt for the chat.
        conversation (list): The conversation history.
        assistant_id (str): The ID of the existing assistant.
    """
    return ask_question(conversation, question, instructions, assistant_id)


def generate_sample_prompts(context, num_samples, max_words, assistant_id=None, followups=None):
    """
    Generates a prompt based on the context.

    Args:
        context (str): The context for generating the prompt.
        num_samples (int): Number of prompts to generate.
        max_words (int): Maximum number of words for the prompt.
        assistant_id (str): The ID of the existing assistant.
        followups (bool): Whether the prompts are follow-up questions.

    Returns:
        list: A list of generated prompts.
    """
    if followups is not None:
        instructions = f"Generate {num_samples} follow-up questions from the user perspective based on the conversation. Each follow-up question should be no more than {max_words} words."
    else:
        instructions = f"Generate {num_samples} sample prompts from the user perspective based on the context. Each sample prompt should be no more than {max_words} words."

    if assistant_id is not None:
        return __generate_assistant_prompts(context, instructions, assistant_id)
    else:
        response = client.chat.completions.create(model=settings["model"],
                                                  messages=[
                                                      {"role": "system", "content": instructions},
                                                      {"role": "user", "content": context}
                                                  ])
        (dict(response).get('usage'))
        (response.model_dump_json(indent=2))
        prompts = response.choices[0].message.content.strip().split('\n')
        return prompts


def __generate_assistant_prompts(context, instructions, assistant_id):
    """
    Private function to generate prompts using an OpenAI Assistant.

    Args:
        context (str): The context for generating the prompt.
        instructions (str): Instructions or system prompt for the chat.
        assistant_id (str): The ID of the existing assistant.

    Returns:
        list: A list of generated prompts.
    """
    # Create a new thread
    thread = client.beta.threads.create()

    # Add the user's question to the thread
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=context
    )

    # Run the assistant
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions=instructions
    )

    if run.status == 'completed':
        # List all messages in the thread
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        # Get the latest assistant message
        prompts = []
        for message in messages.data:
            if message.role == "assistant":
                prompts = message.content[0].text.value.split('\n')
        return prompts
    else:
        return []


def generate_assistant_sample_prompts(context, num_samples, max_words, assistant_id):
    """
    Generates a prompt based on the OpenAI Assistant with a specified ID.

    Args:
        context (str): The context for generating the prompt.
        num_samples (int): Number of prompts to generate.
        max_words (int): Maximum number of words for the prompt.
        assistant_id (str): The ID of the existing assistant.
    """
    return generate_sample_prompts(context, num_samples, max_words, assistant_id)


def generate_followups(question, response, num_samples, max_words, assistant_id=None):
    """
    Generates follow-up questions.

    Args:
        question (str): The previous question asked.
        response (str): The response to the previous question.
        num_samples (int): Number of follow-up questions to generate.
        max_words (int): Maximum number of words for each follow-up question.
        assistant_id (str): The ID of the existing assistant.

    Returns:
        list: A list of follow-up questions.
    """
    recent_history = f"User: {question}\nAssistant: {response}\n"
    return generate_sample_prompts(recent_history, num_samples, max_words, assistant_id, followups=True)


def generate_assistant_followups(question, response, num_samples, max_words, assistant_id):
    """
    Generates follow-up questions based on the OpenAI Assistant with a specified ID.

    Args:
        question (str): The previous question asked.
        response (str): The response to the previous question.
        num_samples (int): Number of follow-up questions to generate.
        max_words (int): Maximum number of words for each follow-up question.
        assistant_id (str): The ID of the existing assistant.

    Returns:
        list: A list of follow-up questions.
    """
    return generate_followups(question, response, num_samples, max_words, assistant_id)


def text_to_speech(text, voice=None):
    """
    Converts text to speech using OpenAI's TTS model.

    Args:
        text (str): The text to convert to speech.
        voice: The voice to use.

    Returns:
        object: The response object from OpenAI audio API.
    """
    if not voice:
        voice = "alloy"
    try:
        speech_file_path = Path(__file__).parent / "speech.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        response.stream_to_file(speech_file_path)
        return response.content
    except Exception as e:
        print(f"Error converting text to speech: {e}")
        return None


def speech_recognition(file):
    """
    Converts speech to text using OpenAI's Whisper model.

    Args:
        file (str): Path to the audio file.

    Returns:
        str: The transcribed text.
    """
    with open(file, "rb") as audio_file:
        translation = client.audio.translations.create(
            model="whisper-1",
            file=audio_file
        )
    return translation.text

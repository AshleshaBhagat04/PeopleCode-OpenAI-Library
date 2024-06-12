
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
    else:
        response = client.chat.completions.create(model=settings["model"],
                                                  messages=[
                                                               {"role": "system", "content": instructions}
                                                           ] + conversation)
        (dict(response).get('usage'))
        (response.model_dump_json(indent=2))
        answer = response.choices[0].message.content.strip()
        conversation.append({"role": "assistant", "content": answer})
        return {"reply": answer, "conversation": conversation}


def ask_question_assistant(conversation, question, instructions, assistant_id):
    """
    Asks a question to an OpenAI Assistant with a specified ID.

    Args:
        question (str): The question to ask.
        instructions (str): Instructions or system prompt for the chat.
        conversation (list): The conversation history.
        assistant_id (str): The ID of the existing assistant.
    """
    return ask_question(conversation, question, instructions, assistant_id)


def generate_prompt(context, max_words, assistant_id=None):
    """
    Generates a prompt based on the context.

    Args:
        context (str): The context for generating the prompt.
        max_words (int): Maximum number of words for the prompt.
        assistant_id (str): The ID of the existing assistant.

    Returns:
        str: The generated prompt.
    """
    instructions = f"Generate a prompt in no more than {max_words} words from the user perspective based on the context provided below."

    if assistant_id is not None:
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
            prompt = None
            for message in messages.data:
                if message.role == "assistant":
                    prompt = message.content[0].text.value

            if prompt:
                return prompt
            else:
                return None
        else:
            return None
    else:
        response = client.chat.completions.create(model=settings["model"],
                                                  messages=[
                                                      {"role": "system",
                                                       "content": instructions},
                                                      {"role": "user", "content": context}
                                                  ])
        (dict(response).get('usage'))
        (response.model_dump_json(indent=2))
        prompt = response.choices[0].message.content.strip()
        return prompt


def generate_prompt_assistant(context, max_words, assistant_id):
    """
    Generates a prompt based on the OpenAI Assistant with a specified ID.

    Args:
        context (str): The context for generating the prompt.
        max_words (int): Maximum number of words for the prompt.
        assistant_id (str): The ID of the existing assistant.
    """
    return generate_prompt(context, max_words, assistant_id)


def generate_followups(question, response, num_samples, max_words, assistant_id=None):
    """
    Generates follow-up questions.

    Args:
        question (str): The previous question asked.
        response (str): The response to the previous question.
        num_samples (int): Number of follow-up questions to generate.
        max_words (int): Maximum number of words for each follow-up question.
        assistant_id (str): The ID of the existing assistant

    Returns:
        list: A list of follow-up questions.
    """
    recent_history = f"User: {question}\nAssistant: {response}\n"
    instructions = f"Generate {num_samples} follow-up questions from the user perspective based on the conversation. Each follow-up question should be no more than {max_words} words."

    if assistant_id is not None:
        # Create a new thread
        thread = client.beta.threads.create()

        # Add the user's question to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=recent_history
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
            followup_qs = []
            for message in messages.data:
                if message.role == "assistant":
                    followup_qs = message.content[0].text.value.split('\n')
            return followup_qs
        else:
            return []
    else:
        followups = client.chat.completions.create(model=settings["model"],
                                                   messages=[
                                                       {"role": "system",
                                                        "content": instructions},
                                                       {"role": "user", "content": recent_history}
                                                   ])
        (dict(followups).get('usage'))
        (followups.model_dump_json(indent=2))
        followup_qs = followups.choices[0].message.content.strip().split('\n')
        return followup_qs


def generate_followups_assistant(question, response, num_samples, max_words, assistant_id):
    """
    Generates follow-up questions based on the OpenAI Assistant with a specified ID.

    Args:
        question (str): The previous question asked.
        response (str): The response to the previous question.
        num_samples (int): Number of follow-up questions to generate.
        max_words (int): Maximum number of words for each follow-up question.
        assistant_id (str): The ID of the existing assistant

    Returns:
        list: A list of follow-up questions.
    """
    return generate_followups(question, response, num_samples, max_words, assistant_id)


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
    followup_questions = generate_followups_assistant(latest_question, latest_answer, num_samples, max_words, "asst_RRXmeNcR4UEj8YSrzOqWkJYa")
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


def text_to_speech(text, voice=None):
    """
    Converts text to speech using OpenAI's TTS model.

    Args:
        text (str): The text to convert to speech.
        voice: The voice to use

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

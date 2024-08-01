from pathlib import Path
from openai import OpenAI

DEFAULT_MODEL = "gpt-4"
DEFAULT_TEMPERATURE = 0.7


class OpenAI_Conversation:
    def __init__(self, api_key, model=DEFAULT_MODEL, assistant=None, temperature=DEFAULT_TEMPERATURE):
        self.__api_key = api_key
        if not self.__api_key:
            raise Exception("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
        self.__client = OpenAI(api_key=self.__api_key)
        self.__model = model
        self.__assistant = assistant
        self.__prevConversation = []
        self.__temperature = temperature

    def __set_context(self):
        # Telling the AI the incoming conversation is based on this context
        pass

    def set_model(self, model_name):
        """
        Sets the model for the OpenAI API.

        Args:
            model_name (str): The model name.
        """
        self.__model = model_name

    def set_assistant(self, assistant_name):
        """
        Sets the assistant name or description for context in the conversation.

        Args:
            assistant_name (str): The assistant's name or description.
        """
        self.__assistant = assistant_name

    def set_temperature(self, temperature):
        """
        Sets the temperature for the OpenAI API.

        Args:
            temperature (float): The temperature setting (between 0 and 1).
        """
        if 0 <= temperature <= 1:
            self.__temperature = temperature
        else:
            raise ValueError("Temperature must be between 0 and 1.")

    def get_conversation(self):
        """
        Returns the conversation history.

        Returns:
            list: The previous conversation history.
        """
        return self.__prevConversation

    def ask_question(self, instructions, question, includePrevConvo=True):
        """
        Asks a question to the OpenAI Chat API.

        Args:
            instructions (str): Instructions or system prompt for the chat.
            question (str): The question to ask.
            includePrevConvo (bool): Whether to include previous conversation in the request.

        Returns:
            dict: The response from the OpenAI Chat API,
                  containing the reply and updated conversation.
        """
        if includePrevConvo:
            messages = [{"role": "system", "content": instructions}] + self.__prevConversation
        else:
            messages = [{"role": "system", "content": instructions}]
        messages.append({"role": "user", "content": question})

        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            temperature=self.__temperature
        )

        answer = response.choices[0].message.content.strip()
        self.__prevConversation.append({"role": "assistant", "content": answer})

        return {"reply": answer, "conversation": self.__prevConversation}

    def generate_sample_prompts(self, context, num_samples, max_words, assistant_id=None, followups=None):
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
        instructions = (
            f"Generate {num_samples} follow-up questions from the user perspective based on the conversation. "
            f"Each follow-up question should be no more than {max_words} words. Only provide the prompts in the response."
            if followups else
            f"Generate {num_samples} sample prompts from the user perspective based on the context. "
            f"Each sample prompt should be no more than {max_words} words. Only provide the questions in the response.")

        if assistant_id is not None:
            return self.__generate_assistant_prompts(context, instructions, assistant_id)
        else:
            response = self.__client.chat.completions.create(
                model=self.__model,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": context}
                ],
                temperature=self.__temperature
            )
            prompts = response.choices[0].message.content.strip().split('\n')
            return prompts

    def generate_assistant_sample_prompts(self, context, num_samples, max_words, assistant_id):
        """
        Generates a prompt based on the OpenAI Assistant with a specified ID.

        Args:
            context (str): The context for generating the prompt.
            num_samples (int): Number of prompts to generate.
            max_words (int): Maximum number of words for the prompt.
            assistant_id (str): The ID of the existing assistant.

        Returns:
            list: A list of generated prompts.
        """
        return self.generate_sample_prompts(context, num_samples, max_words, assistant_id)

    def generate_followups(self, question, response, num_samples, max_words, assistant_id=None):
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
        return self.generate_sample_prompts(recent_history, num_samples, max_words, assistant_id, followups=True)

    def generate_assistant_followups(self, question, response, num_samples, max_words, assistant_id):
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
        return self.generate_followups(question, response, num_samples, max_words, assistant_id)

    def text_to_speech(self, text, voice=None):
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
            response = self.__client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            response.stream_to_file(speech_file_path)
            return response.content
        except Exception as e:
            print(f"Error converting text to speech: {e}")
            return None

    def speech_recognition(self, file):
        """
        Converts speech to text using OpenAI's Whisper model.

        Args:
            file (str): Path to the audio file.

        Returns:
            str: The transcribed text.
        """
        with open(file, "rb") as audio_file:
            translation = self.__client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )
        return translation.text

    def __ask_assistant(self, conversation, question, instructions, assistant_id):
        """
        Private function to ask a question to an OpenAI Assistant with a specified ID.

        Args:
            conversation (list): The conversation history.
            question (str): The question to ask.
            instructions (str): Instructions or system prompt for the chat.
            assistant_id (str): The ID of the existing assistant.

        Returns:
            dict: The response from the OpenAI Chat API,
                  containing the reply with citations and updated conversation.
        """
        # Create a new thread
        thread = self.__client.beta.threads.create()

        # Add the user's question to the thread
        self.__client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        # Run the assistant
        run = self.__client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions=instructions
        )

        if run.status == 'completed':
            # List all messages in the thread
            messages = self.__client.beta.threads.messages.list(
                thread_id=thread.id
            )

            # Get the latest assistant message
            latest_message = None
            for message in messages.data:
                if message.role == "assistant":
                    latest_message = message.content[0].text.value
                    annotations = message.content[0].text.annotations
                    for index, annotation in enumerate(annotations):
                        if file_citation := getattr(annotation, "file_citation", None):
                            cited_file = self.__client.files.retrieve(file_citation.file_id)
                            latest_message = latest_message.replace(annotation.text,
                                                                    f"[{index}]({cited_file.filename})")
                            latest_message += f"\n[{index}] {cited_file.filename}"

            if latest_message:
                return {"reply": latest_message, "conversation": conversation}
            else:
                return {"reply": None, "conversation": conversation}
        else:
            return {"reply": None, "conversation": conversation}

    def __ask_openai(self, conversation, instructions, question):
        """
        Private function to ask a question to the OpenAI Chat API.

        Args:
            conversation (list): The conversation history.
            instructions (str): Instructions or system prompt for the chat.

        Returns:
            dict: The response from the OpenAI Chat API,
                  containing the reply and updated conversation.
        """
        messages = [{"role": "system", "content": instructions}] + conversation
        messages.append({"role": "user", "content": question})

        # Make the API call
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            temperature=self.__temperature
        )

        # Extract the answer from the response
        answer = response.choices[0].message.content.strip()
        conversation.append({"role": "assistant", "content": answer})

        return {"reply": answer, "conversation": conversation}

    def __generate_assistant_prompts(self, context, instructions, assistant_id):
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
        thread = self.__client.beta.threads.create()

        # Add the user's question to the thread
        self.__client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=context
        )

        # Run the assistant
        run = self.__client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions=instructions
        )

        if run.status == 'completed':
            # List all messages in the thread
            messages = self.__client.beta.threads.messages.list(
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

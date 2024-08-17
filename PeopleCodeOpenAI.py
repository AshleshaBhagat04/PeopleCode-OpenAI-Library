from pathlib import Path
from openai import OpenAI

DEFAULT_MODEL = "gpt-4"
DEFAULT_TEMPERATURE = 0.7


class OpenAI_Conversation:
    def __init__(self, api_key, model=DEFAULT_MODEL, assistant=None, temperature=DEFAULT_TEMPERATURE):
        """
        Initializes the OpenAI_Conversation instance with API key and optional model and assistant.

        Args:
            api_key: The API key for OpenAI.
            model: The model to use, default is 'gpt-4'.
            assistant: The assistant ID, default is None.
            temperature: The creativity level of the model output, ranging from 0 to 1.
        """
        self.__api_key = api_key
        if not self.__api_key:
            raise Exception("Error: The API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
        self.__client = OpenAI(api_key=self.__api_key)
        self.__model = model
        self.__assistant = assistant
        self.__prevConversation = []
        self.__temperature = temperature

    def set_model(self, model_name):
        """
        Sets the model to be used for the conversation.

        Args:
            model_name: The name of the model to use.
        """
        self.__model = model_name

    def set_assistant(self, assistant_name):
        """
        Sets the assistant to be used for the conversation.

        Args:
            assistant_name: The name of the assistant to use.
        """
        self.__assistant = assistant_name

    def set_temperature(self, temperature):
        """
        Sets the temperature (creativity level) for the model's output.

        Args:
            temperature: A float between 0 and 1 representing the creativity level.
        """
        if 0 <= temperature <= 1:
            self.__temperature = temperature
        else:
            raise ValueError("Temperature must be between 0 and 1.")

    def get_conversation(self):
        """
        Returns the current conversation history.

        Returns:
            A list of dictionaries representing the conversation history.
        """
        return self.__prevConversation

    def ask_question(self, instructions, question, assistant_id=None):
        """
        Sends a question to the model and returns the model's reply.

        Args:
            instructions: Instructions for the model.
            question: The user's question.
            assistant_id: The assistant ID to use, if any.

        Returns:
            A string containing the model's reply.
        """
        if assistant_id:
            return self.__ask_assistant(self.__prevConversation, question, instructions, assistant_id)
        else:
            return self.__ask_openai(self.__prevConversation, instructions, question)

    def generate_sample_prompts(self, context, num_samples, max_words, assistant_id=None):
        """
        Generates sample prompts based on the given context.

        Args:
            context: The context for generating the prompts.
            num_samples: The number of prompts to generate.
            max_words: The maximum number of words per prompt.
            assistant_id: The assistant ID to use, if any.

        Returns:
            A list of strings, each representing a generated sample prompt.
        """
        instructions = (
            f"Generate {num_samples} sample prompts from the user perspective based on the context. "
            f"Each sample prompt should be no more than {max_words} words."
        )

        if assistant_id:
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

    def generate_followups(self, question, response, num_samples, max_words, assistant_id=None):
        """
        Generates follow-up questions based on the previous question and response.

        Args:
            question: The previous question.
            response: The model's response to the previous question.
            num_samples: The number of follow-up questions to generate.
            max_words: The maximum number of words per follow-up question.
            assistant_id: The assistant ID to use, if any.

        Returns:
            A list of strings, each representing a generated follow-up question.
        """
        recent_history = f"User: {question}\nAssistant: {response}\n"

        instructions = (
            f"Generate {num_samples} follow-up questions from the user perspective based on the conversation. "
            f"Each follow-up question should be no more than {max_words} words. Only provide the questions in the response."
        )

        if assistant_id:
            return self.__generate_assistant_followups(recent_history, instructions, assistant_id)
        else:
            response = self.__client.chat.completions.create(
                model=self.__model,
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": recent_history}
                ],
                temperature=self.__temperature
            )
            followups = response.choices[0].message.content.strip().split('\n')
            return followups

    def generate_list(self, list_description, numItems, maxWordsPerItem):
        """
        Generates a list of items based on the provided description.

        Args:
            list_description: A description of the list to be generated.
            numItems: The number of items to generate.
            maxWordsPerItem: The maximum number of words per item.

        Returns:
            A list of strings, each representing an item in the generated list.
        """
        instructions = (
            f"Generate a list of {numItems} items based on the following description: {list_description}. "
            f"Each item should be no more than {maxWordsPerItem} words. "
            f"Please use '%%' as the delimiter between items and do not add any extra content."
        )

        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=[
                {"role": "system", "content": instructions}
            ],
            temperature=self.__temperature
        )

        raw_list = response.choices[0].message.content.strip()
        list_items = raw_list.split('%%')
        list_items = [item.strip() for item in list_items if item.strip()]

        return list_items

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
        Handles asking a question to a specific assistant and returns the assistant's reply.

        Args:
            conversation: The current conversation history.
            question: The user's question.
            instructions: Instructions for the assistant.
            assistant_id: The assistant ID to use.

        Returns:
            A string containing the assistant's reply.
        """
        thread = self.__client.beta.threads.create()
        self.__client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        run = self.__client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions=instructions
        )

        if run.status == 'completed':
            messages = self.__client.beta.threads.messages.list(thread_id=thread.id)
            latest_message = None
            for message in messages.data:
                if message.role == "assistant":
                    latest_message = message.content[0].text.value
            return latest_message or ""
        return ""

    def __ask_openai(self, conversation, instructions, question):
        """
        Handles asking a question to the OpenAI model and returns the model's reply.

        Args:
            conversation: The current conversation history.
            instructions: Instructions for the model.
            question: The user's question.

        Returns:
            A string containing the model's reply.
        """
        messages = [{"role": "system", "content": instructions}] + conversation
        messages.append({"role": "user", "content": question})

        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=messages,
            temperature=self.__temperature
        )

        answer = response.choices[0].message.content.strip()
        conversation.append({"role": "assistant", "content": answer})

        return answer

    def __generate_assistant_prompts(self, context, instructions, assistant_id):
        """
        Generates sample prompts using a specific assistant and returns them as a list.

        Args:
            context: The context for generating the prompts.
            instructions: Instructions for the assistant.
            assistant_id: The assistant ID to use.

        Returns:
            A list of strings, each representing a generated sample prompt.
        """
        thread = self.__client.beta.threads.create()
        self.__client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=context
        )

        run = self.__client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions=instructions
        )

        if run.status == 'completed':
            messages = self.__client.beta.threads.messages.list(thread_id=thread.id)
            prompts = []
            for message in messages.data:
                if message.role == "assistant":
                    prompts = message.content[0].text.value.split('\n')
            return prompts
        return []

    def __generate_assistant_followups(self, recent_history, instructions, assistant_id):
        """
        Generates follow-up questions using a specific assistant and returns them as a list.

        Args:
            recent_history: The recent conversation history.
            instructions: Instructions for the assistant.
            assistant_id: The assistant ID to use.

        Returns:
            A list of strings, each representing a generated follow-up question.
        """
        thread = self.__client.beta.threads.create()
        self.__client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=recent_history
        )

        run = self.__client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions=instructions
        )

        if run.status == 'completed':
            messages = self.__client.beta.threads.messages.list(thread_id=thread.id)
            followups = []
            for message in messages.data:
                if message.role == "assistant":
                    followups = message.content[0].text.value.split('\n')
            return followups
        return []

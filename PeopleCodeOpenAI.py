from pathlib import Path
from openai import OpenAI

DEFAULT_MODEL = "gpt-4"
DEFAULT_TEMPERATURE = 0.7

class OpenAI_Conversation:
    def __init__(self, api_key, model=DEFAULT_MODEL, assistant=None, temperature=DEFAULT_TEMPERATURE):
        """
        Initializes the OpenAI_Conversation instance.

        Args:
            api_key: The API key for OpenAI.
            model: The model to use, default is 'gpt-4'.
            assistant: The assistant ID, default is None.
            temperature: The creativity level of the model output, ranging from 0 to 1.
        """
        self._api_key = api_key
        if not self._api_key:
            raise ValueError("API key is not set. Set the environment variable 'OPENAI_API_KEY'.")
        self._client = OpenAI(api_key=self._api_key)
        self._model = model
        self._assistant = assistant
        self._prev_conversation = []
        self._temperature = temperature

    def set_model(self, model_name):
        """Sets the model for the conversation."""
        self._model = model_name

    def set_assistant(self, assistant_name):
        """Sets the assistant for the conversation."""
        self._assistant = assistant_name

    def set_temperature(self, temperature):
        """Sets the temperature for the model's output."""
        if 0 <= temperature <= 1:
            self._temperature = temperature
        else:
            raise ValueError("Temperature must be between 0 and 1.")

    def get_conversation(self):
        """Returns the current conversation history."""
        return self._prev_conversation

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
            return self._ask_assistant(instructions, question, assistant_id)
        else:
            return self._ask_openai(instructions, question)

    def generate_sample_prompts(self, context, num_samples, max_words, assistant_id=None):
        """
        Generates sample prompts based on the given context.

        Args:
            context: The context for generating prompts.
            num_samples: The number of prompts to generate.
            max_words: The maximum number of words per prompt.
            assistant_id: The assistant ID to use, if any.

        Returns:
            A list of generated sample prompts.
        """
        instructions = f"Generate {num_samples} sample prompts based on the context. Put each generated question on a separate line with no text before or after. Each prompt should be no more than {max_words} words. "
        if assistant_id:
            return self._generate_assistant_prompts(context, instructions, assistant_id)
        else:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "system", "content": instructions}, {"role": "user", "content": context}],
                temperature=self._temperature
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
            A list of generated follow-up questions.
        """
        recent_history = f"User: {question}\nAssistant: {response}\n"
        instructions = f"Generate {num_samples} follow-up questions based on the conversation. Each follow-up should be no more than {max_words} words."
        if assistant_id:
            return self._generate_assistant_followups(recent_history, instructions, assistant_id)
        else:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "system", "content": instructions}, {"role": "user", "content": recent_history}],
                temperature=self._temperature
            )
            followups = response.choices[0].message.content.strip().split('\n')
            return followups

    def generate_list(self, list_description, num_items, max_words_per_item):
        """
        Generates a list of items based on the provided description.

        Args:
            list_description: A description of the list to be generated.
            num_items: The number of items to generate.
            max_words_per_item: The maximum number of words per item.

        Returns:
            A list of generated items.
        """
        instructions = f"Generate a list of {num_items} items based on the description: {list_description}. Each item should be no more than {max_words_per_item} words. Use '%%' as the delimiter."
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "system", "content": instructions}],
            temperature=self._temperature
        )
        raw_list = response.choices[0].message.content.strip()
        list_items = raw_list.split('%%')
        return [item.strip() for item in list_items if item.strip()]

    def text_to_speech(self, text, voice=None):
        """
        Converts text to speech using OpenAI's TTS model.

        Args:
            text: The text to convert to speech.
            voice: The voice to use.

        Returns:
            The response content from OpenAI audio API.
        """
        if not voice:
            voice = "alloy"
        try:
            speech_file_path = Path(__file__).parent / "speech.mp3"
            response = self._client.audio.speech.create(
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
            file: Path to the audio file.

        Returns:
            The transcribed text.
        """
        with open(file, "rb") as audio_file:
            translation = self._client.audio.translations.create(
                model="whisper-1",
                file=audio_file
            )
        return translation.text

    def _ask_assistant(self, instructions, question, assistant_id):
        """Handles asking a question to a specific assistant."""
        thread = self._client.beta.threads.create()
        self._client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )
        run = self._client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions=instructions
        )
        if run.status == 'completed':
            messages = self._client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value
        return ""

    def _ask_openai(self, instructions, question):
        """Handles asking a question to the OpenAI model."""
        messages = [{"role": "system", "content": instructions}] + self._prev_conversation
        messages.append({"role": "user", "content": question})
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature
        )
        answer = response.choices[0].message.content.strip()
        self._prev_conversation.append({"role": "assistant", "content": answer})
        return answer

    def _generate_assistant_prompts(self, context, instructions, assistant_id):
        """Generates sample prompts using a specific assistant."""
        thread = self._client.beta.threads.create()
        self._client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=context
        )
        run = self._client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions=instructions
        )
        if run.status == 'completed':
            messages = self._client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value.split('\n')
        return []

    def _generate_assistant_followups(self, recent_history, instructions, assistant_id):
        """Generates follow-up questions using a specific assistant."""
        thread = self._client.beta.threads.create()
        self._client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=recent_history
        )
        run = self._client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
            instructions=instructions
        )
        if run.status == 'completed':
            messages = self._client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value.split('\n')
        return []

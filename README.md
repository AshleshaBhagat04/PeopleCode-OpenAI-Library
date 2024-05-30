The library facilitates the development of Gen-AI software with Python code built on top of OpenAI’s API.

The library takes care of tasks such as the following:

- ask a question of openAI with given prompt
- generate sample prompts for a topic
- generate followup questions based on last response or conversation
- track a conversation

The library comes with sample apps demonstrating the use of the library code:

- simple chatbot (chat with Socrates)
- chatbot with sample prompts and followup questions
- chatbot with sample prompts, followup questions, and conversations
    - (user can end a conversation and start new one)
- Streamlit version of chatbot with sample prompts, followups and conversations (Talk with Ella Baker)

## What’s coming?

- voice — library methods to easily use [speech recognition](https://platform.openai.com/docs/guides/speech-to-text) and [TTS](https://platform.openai.com/docs/guides/text-to-speech) using OpenAI omni. We’ll think about vision as well (-:
- RAG — ability to add files to a conversation and adjust how much answers come from database or LLM. We’ll make use of the [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)
- USF GenAI API — API Access to the library

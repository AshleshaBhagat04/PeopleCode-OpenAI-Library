The library facilitates the development of Gen-AI software with Python code built on top of OpenAI’s API.

The library takes care of tasks such as the following:

- ask a question of OpenAI with a given prompt
- generate sample prompts for a topic
- generate follow-up questions based on the last response or conversation
- track a conversation

The library comes with sample apps demonstrating the use of the library code:

- simple chatbot (chat with Socrates)
- chatbot with sample prompts and follow-up questions
- chatbot with sample prompts, follow-up questions, and conversations
    - (user can end a conversation and start a new one)
- Streamlit version of chatbot with sample prompts, followups, and conversations (Talk with Ella Baker)

Deploying on Streamlit:
- Go to my apps and then click "Create app" on the top right
- Select whether or not you already have code written for an app
- If so, enter the complete path of the repository name
- Enter the name of the file
- To use an OpenAI api key, click on "Advanced settings"
- Set the key with OPENAI_API_KEY=""
- Click "Save" and then "Deploy!"

## What’s coming?

- voice — library methods to easily use [speech recognition](https://platform.openai.com/docs/guides/speech-to-text) and [TTS](https://platform.openai.com/docs/guides/text-to-speech) using OpenAI omni. We’ll think about vision as well (-:
- RAG — the ability to add files to a conversation and adjust how many answers come from a database or LLM. We’ll make use of the [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)
- USF GenAI API — API Access to the library

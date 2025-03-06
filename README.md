For in-depth tutorials, please visit: peoplecode.ai

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

## Running the Sample Apps

You need Python3 to run the samples and you’ll need Pip to install some Python packages. Generally Pip comes with your Python installation.

1. Clone the GitHub repo into a local folder. Open a terminal and enter the following command to clone the app (% represents the linux prompt)
        
        % git clone https://github.com/People-Museum-Project/PeopleCode-OpenAI-Library.git
        
3. Install the OpenAI library
    
          % pip install OpenAI
    
4. Get an OpenAI/API key and set it in your env variables.
   -- Here is a [video](https://youtu.be/RwVHrUhY_DQ) on getting a key
   -- Once you have a key, set your command-line environment variables with it. At the terminal run the following command, replacing "your-api-key" with the key you got from OpenAI:
        
         % export OPENAI_API_KEY="your-api-key”
        

### Command-line apps

The command-line samples are in the Command-Line-Apps subfolder. From that folder, run one of the samples, e.g.,

    % python simpleChatApp.py

### Streamlit Apps

Steamlit is a Python library for building user interfaces. Streamlit provides a Python-centric way to add a front-end to some back-end code.

We have developed a number of sample Streamlit apps that use the [PeopleCode.AI](http://PeopleCode.AI) OpenAI library. They are in the “Streamlit-Apps” subfolder of the repository.

To run one of the sample streamlit apps, perform the following steps:

1. Install the Streamlit library
    
    pip install steamlit
    
2. run the app with the following command:

From the main project folder:

% streamlit run ./Streamlit-Apps/EllaBakerStreamlit.py

or any of the other samples

You can also deploy a Streamlit apps so that it runs on the web with a URL you can share with others. Streamlit community will event host your app.

- Get an account at Streamlit.com.
- At Streamlit, choose “My Apps” and then click "Create app" on the top right
- Select that you already have code written for an app and enter the complete path of the repository name and the name of the file
- To use an OpenAI api key, click on "Advanced settings"
- Set the key with OPENAI_API_KEY=""
- Click "Save" and then "Deploy"

## What’s coming?

- voice — library methods to easily use [speech recognition](https://platform.openai.com/docs/guides/speech-to-text) and [TTS](https://platform.openai.com/docs/guides/text-to-speech) using OpenAI omni. We’ll think about vision as well (-:
- RAG — the ability to add files to a conversation and adjust how many answers come from a database or LLM. We’ll make use of the [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)
- USF GenAI API — API Access to the library

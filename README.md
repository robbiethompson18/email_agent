## Setup

1. Clone the repository
2. Install dependencies (pip install requirements.txt)
3. get an API key for using gmail and add it to the file mcagent2.json
    a. a chatbot will explain how to do this better than I can, but you need to go to Google Cloud setup and enable gmail apis
4. Get an API key for openai, save it to your bashrc or .zshrc as OPENAI_API_KEY 
    a. apparently saving it here and not in a file is best practice? I guess good so that it won't get uploaded to git.

# Email Unsubscribe Agent

A Python tool that automatically finds and unsubscribes from unwanted emails using the Gmail API and optional LLM assistance.

## Features

- **Email Finding**: Search for emails matching specific criteria in your Gmail account
- **Rule-Based Unsubscribing**: Find and follow unsubscribe links using pattern matching
- **LLM-Based Unsubscribing**: Use OpenAI's models to intelligently find unsubscribe links
- **Modular Design**: Separate components for authentication, email finding, and unsubscribing

## Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/robbiethompson18/email_agent.git](https://github.com/robbiethompson18/email_agent.git)
   cd email_agent

2. **install dependencies**
Create and activate a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install required packages:
pip install -r requirements.txt

3. Gmail API credentials
Set up Gmail API credentials
Go to Google Cloud Console
Create a new project
Enable the Gmail API
Configure OAuth consent screen (add yourself as a test user)
Create OAuth client ID credentials (Desktop application)
Download the credentials JSON file and save as mcagent2.json in the project directory

4. Setupup OpenAI API Key 
Add your API to a .env file, ie 
OPENAI_API_KEY="your_key_here"

## Basic usage:
python main.py
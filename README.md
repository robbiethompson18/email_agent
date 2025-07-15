# Email Project

Automating unsubscribing from emails.

## Setup

1. Clone the repository
2. Install dependencies (pip install requirements.txt)
3. get an API key for using gmail and add it to the file mcagent2.json
    a. a chatbot will explain how to do this better than I can, but you need to go to Google Cloud setup and enable gmail apis
4. Get an API key for openai, save it to your bashrc or .zshrc as OPENAI_API_KEY 
    a. apparently saving it here and not in a file is best practice? I guess good so that it won't get uploaded to git.

## Development

I need to sort out a linter


## how to use

Just forward the email you want to unsubscribe from to agent: unsubscribe. It should be able to click on links, but can't yet send unsubscribe emails.

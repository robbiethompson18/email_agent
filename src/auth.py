"""Authentication utilities for OpenAI and Gmail APIs."""

import os
import sys
import pickle
from openai import OpenAI
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_openai_client(api_key=None):
    """Get an authenticated OpenAI client.
    
    Args:
        api_key (str, optional): OpenAI API key. If not provided, will try to get from env var.
        
    Returns:
        OpenAI: Authenticated OpenAI client
    """
    # Try to load from .env file
    load_dotenv()
    
    # Get API key with priority: 1) passed param, 2) env var, 3) .env file
    openai_api_key = api_key or os.environ.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found. Please provide it as a parameter or set it as an environment variable.")
        print("You can set it in your shell with: export OPENAI_API_KEY='your-key-here'")
        print("Or create a .env file in the project directory with: OPENAI_API_KEY='your-key-here'")
        sys.exit(1)
        
    return OpenAI(api_key=openai_api_key)


def get_gmail_service(credential_filename = ""):
    """Get an authenticated Gmail service instance.
    
    Args:
        credential_filename (str): Path to the Google credentials JSON file
        
    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail service
    """
    if not credential_filename:
        credential_filename = os.getenv("GMAIL_CREDENTIAL_FILENAME")
        # Load environment
        # Get project root (parent of src directory)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dotenv_path = os.path.join(project_root, '.env')
        load_dotenv(dotenv_path, override=True)
        credential_filename = os.getenv("GMAIL_CREDENTIALS_FILE")
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    creds = None
    
    # Get the directory where the credential file is located (should be keys/)
    credential_dir = os.path.dirname(credential_filename)
    token_path = os.path.join(credential_dir, 'token.pickle')
    
    # Check if we have valid credentials
    if os.path.exists(token_path):
        print('Loading saved credentials')
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If credentials are invalid or don't exist, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print('Refreshing credentials')
            creds.refresh(Request())
        else:
            print('Getting new credentials')
            if not os.path.exists(credential_filename):
                raise FileNotFoundError(
                    f"Credentials file {credential_filename} not found. Please download it from Google Cloud Console"
                )
            flow = InstalledAppFlow.from_client_secrets_file(credential_filename, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for future use in the same directory as the credential file
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)
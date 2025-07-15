import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GmailAuthenticator:
    """Handles Gmail API authentication for all agents."""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    
    @staticmethod
    def get_gmail_service(credential_filename):
        """Get an authenticated Gmail service instance."""
        creds = None
        
        # Check if we have valid credentials
        if os.path.exists('token.pickle'):
            print('Loading saved credentials')
            with open('token.pickle', 'rb') as token:
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
                flow = InstalledAppFlow.from_client_secrets_file(
                    credential_filename, GmailAuthenticator.SCOPES)
                creds = flow.run_local_server(port=0)

            # Save credentials for future use
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

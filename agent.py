import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

class GmailAgent:
    # If modifying these scopes, delete the token.pickle file.
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    def __init__(self):
        """Initialize the Gmail API service."""
        load_dotenv()
        self.creds = None
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0."""
        # Check if we have valid credentials
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If credentials are invalid or don't exist, get new ones
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    raise FileNotFoundError(
                        "credentials.json file not found. Please download it from Google Cloud Console"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Save the credentials for future runs
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('gmail', 'v1', credentials=self.creds)

    def list_messages(self, query="", max_results=10):
        """List messages matching the specified query."""
        try:
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])
            return messages
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def read_message(self, msg_id):
        """Read a specific message by its ID."""
        try:
            message = self.service.users().messages().get(
                userId='me', id=msg_id, format='full').execute()
            return message
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def send_message(self, to, subject, message_text):
        """Send an email message."""
        try:
            from email.mime.text import MIMEText
            import base64

            message = MIMEText(message_text)
            message['to'] = to
            message['subject'] = subject
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()).decode('utf-8')
            
            self.service.users().messages().send(
                userId='me',
                body={'raw': raw_message}).execute()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

if __name__ == '__main__':
    # Example usage
    agent = GmailAgent()
    
    # List recent messages
    messages = agent.list_messages(max_results=5)
    for msg in messages:
        print(f"Message ID: {msg['id']}")
        
        # Read each message
        full_msg = agent.read_message(msg['id'])
        if full_msg:
            print(f"Subject: {full_msg.get('payload', {}).get('headers', [{}])[0].get('value', 'No subject')}")
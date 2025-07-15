import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import base64

class GmailAgent:
    # If modifying these scopes, delete the token.pickle file.
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    def __init__(self, credential_filename):
        """Initialize the Gmail API service."""
        load_dotenv()
        self.creds = None
        self.service = None
        self.credential_filename = credential_filename
        self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0."""
        # Check if we have valid credentials
        if os.path.exists('token.pickle'):
            print('unpickling credentials')
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If credentials are invalid or don't exist, get new ones
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                print('trying to get credentials')
                if not os.path.exists(self.credential_filename):
                    raise FileNotFoundError(
                        f"""credentials file {self.credential_filename} not found. Please download it from Google Cloud Console"""
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credential_filename, self.SCOPES)
                print('gotten creds?')
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
            
            # Get headers
            headers = {}
            for header in message.get('payload', {}).get('headers', []):
                name = header.get('name')
                value = header.get('value')
                if name and value:
                    headers[name] = value

            # Get message body
            payload = message.get('payload', {})
            if payload.get('body', {}).get('data'):
                # If body is in the main payload
                body = base64.urlsafe_b64decode(payload['body']['data']).decode()
            elif payload.get('parts'):
                # If body is in the first part (multipart messages)
                body = base64.urlsafe_b64decode(
                    payload['parts'][0]['body']['data']).decode()
            else:
                body = "No body found"
            
            return {
                'subject': headers.get('Subject', 'No subject'),
                'from': headers.get('From', 'No sender'),
                'body': body
            }
            
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
    agent = GmailAgent("mcagent2.json")
    print('successfully logged in')
    
    # List recent messages
    messages = agent.list_messages("agent: unsubscribe", max_results=5)
    print(f'got {len(messages)} messages')
    
    for msg in messages:
        print("\n" + "="*50)
        print(f"Message ID: {msg['id']}")
        
        # Read message
        message_data = agent.read_message(msg['id'])
        if message_data:
            print(f"From: {message_data['from']}")
            print(f"Subject: {message_data['subject']}")
            print("\nBody preview:")
            print(message_data['body'][:100] + "...")
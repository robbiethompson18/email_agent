import re
import base64
import requests
from bs4 import BeautifulSoup
from shared_auth import GmailAuthenticator

class UnsubscribeAgent:
    """Handles the unsubscribe process for emails."""
    
    def __init__(self, credential_filename):
        """Initialize the Gmail API service."""
        self.service = GmailAuthenticator.get_gmail_service(credential_filename)

    def get_message_content(self, msg_id):
        """Get the full content of a message."""
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
                body = base64.urlsafe_b64decode(payload['body']['data']).decode()
            elif payload.get('parts'):
                body = base64.urlsafe_b64decode(
                    payload['parts'][0]['body']['data']).decode()
            else:
                body = "No body found"
            
            return {
                'headers': headers,
                'body': body
            }
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def find_unsubscribe_link(self, headers, body):
        """Find unsubscribe link from email headers or body."""
        # Check List-Unsubscribe header first
        if 'List-Unsubscribe' in headers:
            unsubscribe = headers['List-Unsubscribe']
            # Extract URL from <> brackets if present
            url_match = re.search(r'<(https?://[^>]+)>', unsubscribe)
            if url_match:
                return url_match.group(1)
            
        # Parse HTML body for unsubscribe links
        soup = BeautifulSoup(body, 'html.parser')
        
        # Look for common unsubscribe patterns in links
        unsubscribe_patterns = [
            r'unsubscribe',
            r'opt.?out',
            r'remove.*(?:subscription|mailing)',
            r'(?:manage|update).*preferences'
        ]
        
        pattern = '|'.join(unsubscribe_patterns)
        for link in soup.find_all('a', href=True):
            if re.search(pattern, link.text.lower()) or re.search(pattern, link['href'].lower()):
                return link['href']
        
        return None

    def unsubscribe(self, msg_id):
        """Attempt to unsubscribe from an email."""
        message_data = self.get_message_content(msg_id)
        if not message_data:
            print("Could not read message")
            return False

        unsubscribe_url = self.find_unsubscribe_link(
            message_data['headers'], 
            message_data['body']
        )
        
        if unsubscribe_url:
            print(f"Found unsubscribe URL: {unsubscribe_url}")
            try:
                # Some unsubscribe links are mailto: links
                if unsubscribe_url.startswith('mailto:'):
                    print("This is an email unsubscribe link. Would need to send an email to:", unsubscribe_url[7:])
                    return False
                
                # Try to follow the unsubscribe link
                response = requests.get(unsubscribe_url)
                print(f"Unsubscribe request status: {response.status_code}")
                return response.status_code == 200
            except Exception as e:
                print(f"Error following unsubscribe link: {e}")
                return False
        else:
            print("No unsubscribe link found")
            return False

if __name__ == '__main__':
    # Example usage with message IDs from email_finder.py
    agent = UnsubscribeAgent("mcagent2.json")
    msg_id = "your-message-id-here"  # Get this from email_finder.py
    
    if agent.unsubscribe(msg_id):
        print("Successfully unsubscribed!")
    else:
        print("Could not unsubscribe automatically")

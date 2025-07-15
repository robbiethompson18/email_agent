import base64
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from shared_auth import GmailAuthenticator

class UnsubscribeLLMAgent:
    """Uses LLM to find and follow unsubscribe links in emails."""
    
    def __init__(self, credential_filename):
        """Initialize the Gmail API service and OpenAI client."""
        load_dotenv()
        self.service = GmailAuthenticator.get_gmail_service(credential_filename)
        
        # Initialize OpenAI client
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        self.client = OpenAI(api_key=openai_api_key)

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

    def find_unsubscribe_link_with_llm(self, headers, body):
        """Use LLM to find unsubscribe link from email headers or body."""
        # First check List-Unsubscribe header as it's standard
        if 'List-Unsubscribe' in headers:
            unsubscribe = headers['List-Unsubscribe']
            if '<http' in unsubscribe:
                # Extract URL from <> brackets
                start = unsubscribe.find('<http') + 1
                end = unsubscribe.find('>', start)
                if start > 0 and end > start:
                    return unsubscribe[start:end]
        
        # Prepare content for the LLM
        email_content = f"""
        From: {headers.get('From', 'Unknown')}
        Subject: {headers.get('Subject', 'No Subject')}
        
        {body[:10000]}  # Limit size to avoid token limits
        """
        
        # Ask LLM to find the unsubscribe link
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Use appropriate model
                messages=[
                    {"role": "system", "content": "You are an assistant that helps find unsubscribe links in emails. Extract ONLY the URL, nothing else."},
                    {"role": "user", "content": f"Find the unsubscribe link in this email. Return ONLY the full URL, nothing else. If you can't find one, respond with 'NO_UNSUBSCRIBE_LINK_FOUND'.\n\n{email_content}"}
                ],
                temperature=0,
                max_tokens=100
            )
            
            link = response.choices[0].message.content.strip()
            if link == "NO_UNSUBSCRIBE_LINK_FOUND" or not link.startswith("http"):
                return None
            return link
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return None

    def unsubscribe(self, msg_id):
        """Attempt to unsubscribe from an email using LLM."""
        message_data = self.get_message_content(msg_id)
        if not message_data:
            print("Could not read message")
            return False

        unsubscribe_url = self.find_unsubscribe_link_with_llm(
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
    agent = UnsubscribeLLMAgent("mcagent2.json")
    msg_id = "your-message-id-here"  # Get this from email_finder.py
    
    if agent.unsubscribe(msg_id):
        print("Successfully unsubscribed!")
    else:
        print("Could not unsubscribe automatically")

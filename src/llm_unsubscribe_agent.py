import os
import requests
from .openai_agent import OpenAIAgent
import argparse

class UnsubscribeLLMAgent(OpenAIAgent):
    """Uses LLM to find and follow unsubscribe links in emails."""
    
    def __init__(self, api_key=None):
        """Initialize the OpenAI client.
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided, will try to get from env var.
        """
        super().__init__(api_key)

    def find_unsubscribe_link(self, email_body, email_subject=None, email_from=None, list_unsubscribe_header=None):
        """Use LLM to find unsubscribe link from email body.
        
        Args:
            email_body (str): The body content of the email
            email_subject (str, optional): The subject of the email
            email_from (str, optional): The sender of the email
            list_unsubscribe_header (str, optional): The List-Unsubscribe header if available
            
        Returns:
            str or None: The unsubscribe URL if found, otherwise None
        """
        # Limit email body size to avoid token limits
        truncated_body = email_body[:20000] if email_body else ""
        
        # Ask LLM to find the unsubscribe link
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use appropriate model
                messages=[
                    {"role": "system", "content": "You are an assistant that helps find unsubscribe links in emails. Extract ONLY the URL, nothing else."},
                    {"role": "user", "content": f"Find the unsubscribe link in this email. Return ONLY the full URL, nothing else. If you can't find one, respond with 'NO_UNSUBSCRIBE_LINK_FOUND'.\n\n{truncated_body}"}
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

    def attempt_unsubscribe(self, unsubscribe_url):
        """Attempt to follow an unsubscribe URL.
        
        Args:
            unsubscribe_url (str): The URL to unsubscribe
            
        Returns:
            bool: True if successfully followed the link, False otherwise
        """
        if not unsubscribe_url:
            print("No unsubscribe URL provided")
            return False
            
        print(f"Attempting to follow unsubscribe URL: {unsubscribe_url}")
        
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

if __name__ == '__main__':
    # Example usage
    import argparse
    import os
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='LLM Unsubscribe Agent Example')
    parser.add_argument('--api-key', help='OpenAI API key (overrides environment variable)')
    args = parser.parse_args()
    
    # Get API key with priority: command line > environment variable > .env file
    api_key = args.api_key or os.environ.get('OPENAI_API_KEY')
    
    # Initialize agent with API key
    agent = UnsubscribeLLMAgent(api_key=api_key)
    
    # Example email body
    email_body = """
    <html>
    <body>
    <p>Thank you for subscribing to our newsletter!</p>
    <p>To unsubscribe from future emails, <a href="https://example.com/unsubscribe?id=123">click here</a>.</p>
    </body>
    </html>
    """
    
    # Optional metadata
    email_subject = "Weekly Newsletter"
    email_from = "newsletter@example.com"
    list_unsubscribe = "<https://example.com/unsubscribe/123>"
    
    print(f"Processing email from: {email_from}")
    print(f"Subject: {email_subject}")
    
    # Find the unsubscribe link
    unsubscribe_url = agent.find_unsubscribe_link(
        email_body=email_body,
        email_subject=email_subject,
        email_from=email_from,
        list_unsubscribe_header=list_unsubscribe
    )
    
    if unsubscribe_url:
        print(f"Found unsubscribe URL: {unsubscribe_url}")
        if agent.attempt_unsubscribe(unsubscribe_url):
            print("✓ Successfully unsubscribed!")
        else:
            print("✗ Could not unsubscribe automatically")
    else:
        print("✗ No unsubscribe link found")

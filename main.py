from email_finder import EmailFinder
from llm_unsubscribe_agent import UnsubscribeLLMAgent
import base64
import argparse
import os

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Email Unsubscribe Tool')
    parser.add_argument('--query', default='agent: unsubscribe', help='Search query for finding emails')
    parser.add_argument('--max-results', type=int, default=5, help='Maximum number of emails to process')
    parser.add_argument('--api-key', help='OpenAI API key (overrides environment variable)')
    args = parser.parse_args()
    
    # Get API key from command line or environment
    api_key = args.api_key or os.environ.get('OPENAI_API_KEY')
    
    # Find emails to unsubscribe from
    finder = EmailFinder("mcagent2.json")
    candidates = finder.find_unsubscribe_candidates(query=args.query, max_results=args.max_results)
    
    if not candidates:
        print("No emails found to unsubscribe from")
        return
    
    print(f"\nFound {len(candidates)} candidates for unsubscribing:")
    for i, candidate in enumerate(candidates, 1):
        print(f"\n{i}. From: {candidate['from']}")
        print(f"   Subject: {candidate['subject']}")
        print(f"   Date: {candidate['date']}")
    
    # Initialize the LLM agent with API key
    llm_agent = UnsubscribeLLMAgent(api_key=api_key)
    
    # Process each candidate
    for candidate in candidates:
        print(f"\nProcessing: {candidate['subject']}")
        
        # Get the full message content
        message = finder.service.users().messages().get(
            userId='me', id=candidate['id'], format='full').execute()
        
        # Extract headers
        headers = {}
        for header in message.get('payload', {}).get('headers', []):
            name = header.get('name')
            value = header.get('value')
            if name and value:
                headers[name] = value
        
        # Get message body
        payload = message.get('payload', {})
        body = ""
        if payload.get('body', {}).get('data'):
            body = base64.urlsafe_b64decode(payload['body']['data']).decode()
        elif payload.get('parts'):
            body = base64.urlsafe_b64decode(
                payload['parts'][0]['body']['data']).decode()
        
        # Find unsubscribe link using the LLM agent
        unsubscribe_url = llm_agent.find_unsubscribe_link(
            email_body=body,
            list_unsubscribe_header=headers.get('List-Unsubscribe')
        )
        
        # Try to unsubscribe
        if unsubscribe_url:
            if llm_agent.attempt_unsubscribe(unsubscribe_url):
                print("✓ Successfully unsubscribed!")
            else:
                print("✗ Could not unsubscribe automatically")
        else:
            print("✗ No unsubscribe link found")


if __name__ == '__main__':
    main()

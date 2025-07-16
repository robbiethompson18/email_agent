from shared_auth import GmailAuthenticator
import argparse

class EmailFinder:
    """Finds emails that should be unsubscribed from."""
    
    def __init__(self, credential_filename):
        """Initialize the Gmail API service."""
        self.service = GmailAuthenticator.get_gmail_service(credential_filename)

    def find_unsubscribe_candidates(self, query, max_results=10):
        """Find emails matching unsubscribe criteria."""
        try:
            print(f"Searching for emails matching: {query}")
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])
            
            candidates = []
            for msg in messages:
                message = self.service.users().messages().get(
                    userId='me', id=msg['id'], format='full').execute()
                
                # Get headers
                headers = {}
                for header in message.get('payload', {}).get('headers', []):
                    name = header.get('name')
                    value = header.get('value')
                    if name and value:
                        headers[name] = value
                
                candidates.append({
                    'id': msg['id'],
                    'subject': headers.get('Subject', 'No subject'),
                    'from': headers.get('From', 'No sender'),
                    'date': headers.get('Date', 'No date')
                })
            
            return candidates
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, default='default_value', help = 'string to search for when looking for emails. TODO: make this an LLM prompt?')
    parser.add_argument('')
    args = parser.parse_args()
    print(args.query)
    finder = EmailFinder("mcagent2.json")
    candidates = finder.find_unsubscribe_candidates(args.query)
    
    print(f"\nFound {len(candidates)} candidates for unsubscribing:")
    for candidate in candidates:
        print("\n" + "="*50)
        print(f"Message ID: {candidate['id']}")
        print(f"From: {candidate['from']}")
        print(f"Subject: {candidate['subject']}")
        print(f"Date: {candidate['date']}")

from email_finder import EmailFinder
from unsubscribe_agent import UnsubscribeAgent

def main():
    # Find emails to unsubscribe from
    finder = EmailFinder("mcagent2.json")
    candidates = finder.find_unsubscribe_candidates()
    
    if not candidates:
        print("No emails found to unsubscribe from")
        return
    
    print(f"\nFound {len(candidates)} candidates for unsubscribing:")
    for i, candidate in enumerate(candidates, 1):
        print(f"\n{i}. From: {candidate['from']}")
        print(f"   Subject: {candidate['subject']}")
        print(f"   Date: {candidate['date']}")
    
    # Process each candidate
    agent = UnsubscribeAgent("mcagent2.json")
    for candidate in candidates:
        print(f"\nProcessing: {candidate['subject']}")
        if agent.unsubscribe(candidate['id']):
            print("✓ Successfully unsubscribed!")
        else:
            print("✗ Could not unsubscribe automatically")

if __name__ == '__main__':
    main()

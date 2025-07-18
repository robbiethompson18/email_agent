import argparse
import base64
import os

from dotenv import load_dotenv
from unsubscribe_agent import UnsubscribeAgent

from email_finder import EmailFinder


def main():
    # Load environment variables from .env file in project root
    # Get project root (parent of src directory)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dotenv_path = os.path.join(project_root, ".env")
    load_dotenv(dotenv_path, override=True)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Email Unsubscribe Tool")
    parser.add_argument(
        "--query", default="agent: unsubscribe", help="Search query for finding emails"
    )
    parser.add_argument(
        "--max-results", type=int, default=5, help="Maximum number of emails to process"
    )
    parser.add_argument(
        "--api-key", help="OpenAI API key (overrides environment variable)"
    )
    parser.add_argument(
        "--gmail-credentials-filepath",
        help="(absolute) path to gmail credentials json (overrides environment variable)",
    )
    args = parser.parse_args()

    # Get API key from command line or environment
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")

    # Find emails to unsubscribe from
    gmail_credential_filename = args.gmail_credentials_filepath or ""
    email_finder = EmailFinder(gmail_credential_filename)
    candidates = email_finder.find_unsubscribe_candidates(
        query=args.query, max_results=args.max_results
    )

    if not candidates:
        print("No emails found to unsubscribe from")
        return

    print(f"\nFound {len(candidates)} candidates for unsubscribing:")
    for i, candidate in enumerate(candidates, 1):
        print(f"\n{i}. From: {candidate['from']}")
        print(f"   Subject: {candidate['subject']}")
        print(f"   Date: {candidate['date']}")

    # Initialize the LLM agent with API key
    unsubscribe_agent = UnsubscribeAgent(api_key=api_key)

    # Process each candidate
    for candidate in candidates:
        print(f"\nProcessing: {candidate['subject']}")
        unsubscribe_agent.attempt_unsubscribe_from_body(candidate.body):

if __name__ == "__main__":
    main()

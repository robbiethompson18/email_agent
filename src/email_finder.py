from auth import get_gmail_service
import argparse
import base64


class EmailFinder:
    """Finds emails that should be unsubscribed from."""

    def __init__(self, credential_filename=""):
        """Initialize the Gmail API service."""
        self.service = get_gmail_service(credential_filename)

    @staticmethod
    def extract_gmail_json_into_usable_format(message):
        headers = {}
        for header in message.get("payload", {}).get("headers", []):
            name = header.get("name")
            value = header.get("value")
            if name and value:
                headers[name] = value
        payload = message.get("payload", {})
        body = ""
        if payload.get("body", {}).get("data"):
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode()
        elif payload.get("parts"):
            body = base64.urlsafe_b64decode(
                payload["parts"][0]["body"]["data"]
            ).decode()

        return {
            "id": message["id"],
            "subject": headers.get("Subject", "No subject"),
            "sender": headers.get("From", "No sender"),
            "date": headers.get("Date", "No date"),
            "body": body
        }

    def find_unsubscribe_candidates(self, query, max_results=10):
        """Find emails matching unsubscribe criteria."""
        try:
            print(f"Searching for emails matching: {query}")
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )
            messages = results.get("messages", [])

            candidates = []
            for msg in messages:
                message = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=msg["id"], format="full")
                    .execute()
                )
                candidates.append(EmailFinder.extract_gmail_json_into_usable_format(message))
            return candidates

        except Exception as e:
            print(f"An error occurred: {e}")
            return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--query",
        type=str,
        default="unsubscribe",
        help="string to search for when looking for emails. TODO: make this an LLM prompt?",
    )
    args = parser.parse_args()
    finder = EmailFinder("")
    candidates = finder.find_unsubscribe_candidates(args.query)

    print(f"\nFound {len(candidates)} candidates for query {args.query}")
    for candidate in candidates:
        print(candidate)
        print("\n" + "=" * 50)
        print(f"Message ID: {candidate['id']}")
        print(f"From: {candidate['sender']}")
        print(f"Subject: {candidate['subject']}")
        print(f"Date: {candidate['date']}")
        print(f"Body Truncated: {candidate['body'][0:100]}")

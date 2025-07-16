import pytest
from src.email_finder import EmailFinder

def basic_test_find_vital_email(query = "unsubscribe"):
    finder = Email_Finder("keys/mcagent2.json")
    candidates = finder.find_unsubscribe_candidates(query) 
    assert len(candidates) >= 1

# TODO add more tests when I have more examples

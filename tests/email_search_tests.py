import pytest
import os
from email_finder import EmailFinder

def test_basic_find_vital_email(query = "unsubscribe"):
    # Get absolute path to keys directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    keys_path = os.path.join(project_root, "keys", "mcagent2.json")
    finder = EmailFinder(keys_path)
    candidates = finder.find_unsubscribe_candidates(query) 
    assert len(candidates) >= 1

def test_basic_find_vital_email_auto_keys(query = "unsubscribe"):
    finder = EmailFinder()
    candidates = finder.find_unsubscribe_candidates(query) 
    assert len(candidates) >= 1
# TODO add more tests when I have more examples

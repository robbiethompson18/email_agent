import pytest
from llm_unsubscribe_agent import UnsubscribeLLMAgent
import os


# make sure it successfully unsubscribes from that one vital link


# make sure we find the link in the vital email
def test_find_link_in_vital_email():
    unsub_agent = UnsubscribeLLMAgent()
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    keys_path = os.path.join(project_root, "tests", "vital_email_body.txt")
    with open(keys_path, "r") as file:
        body = file.read()
    link = unsub_agent.find_unsubscribe_link(body)
    print(link)
    assert link == "https://vitalclimbinggym.us10.list-manage.com/unsubscribe?u=5dadccc279b0a369ccfbe0a63&id=ad7c9f0f37&t=b&e=062607c861&c=2948f4dd4c"
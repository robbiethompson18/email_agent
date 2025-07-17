import pytest
from llm_unsubscribe_agent import UnsubscribeLLMAgent


# make sure it successfully unsubscribes from that one vital link


# make sure we find the link in the vital email
def test_find_link_in_vital_email():
    unsub_agent = UnsubscribeLLMAgent()
    with open("vital_email_body.txt", "r") as file:
        body = file.read()
    link = unsub_agent.find_unsubscribe_link(body)
    print(link)
    assert link == "https://vitalclimbinggym.us10.list-manage.com/unsubscribe?u=5dadccc279b0a369ccfbe0a63&id=ad7c9f0f37&t=b&e=062607c861&c=2948f4dd4c"
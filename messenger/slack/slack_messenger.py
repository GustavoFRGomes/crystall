import requests
import json


class SlackMessenger:
    def __init__(self, webhook_url: str):
        self._webhook_url = webhook_url

    def create_message(self, message: str) -> str:
        return json.dumps({"text": message})

    def create_user_mention_message(self, message: str, user_id: str) -> str:
        return json.dumps({"text": message, "blocks": [{"type": "user", "user_id": user_id}]})

    def send(self, message):
        requests.post(self._webhook_url, data=message, headers={'Content-Type': 'application/json'})

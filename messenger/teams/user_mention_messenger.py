from messenger.teams.webhook_exception import TeamsWebhookException
import urllib3


class UserMention:
    def __init__(self, user_name: str, user_email: str):
        self.user_email = user_email
        self.user_name = user_name


class MentionConnectorCard:
    def __init__(self, webhook_url: str, http_timeout: int = 60):
        self.http = urllib3.PoolManager()
        self.payload = {}
        self.webhook_url = webhook_url
        self.http_timeout = http_timeout

    def _create_mention_payload(self, mention: UserMention):
        json = """{
    "type": "message",
    "attachments": [
        {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": {
            "type": "AdaptiveCard",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "Hello <at>XXX</at>"
                }
            ],
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "version": "1.0",
            "msteams": {
                "entities": [
                    {
                        "type": "mention",
                        "text": "<at>XXX</at>",
                        "mentioned": {
                              "id": "EMAIL",
                              "name": "XXX"
                        }
                    }
                ]
            }
        }
    }]
}"""
        return json.replace("XXX", mention.user_name).replace("EMAIL", mention.user_email)

    def mention(self, mention: UserMention):
        self.payload = self._create_mention_payload(mention)
        return self

    def send(self):
        headers = {"Content-Type": "application/json"}
        r = self.http.request(
            'POST',
            f'{self.webhook_url}',
            body=self.payload,
            headers=headers, timeout=self.http_timeout)
        if r.status == 200:
            return True
        else:
            raise TeamsWebhookException(r.reason)

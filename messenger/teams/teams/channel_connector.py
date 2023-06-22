import urllib3
import json
from connectors.connector import TeamsWebhookException


class ChannelWideMention:
    def __init__(self, channel_name, channel_id):
        self.channel_name = channel_name
        self.channel_id = channel_id

    def export_as_json(self):
        mention = """
        {
                "type": "mention",
                "text": "<at>CHANNELNAME</at>",
                "mentioned": {
                  "id": "CHANNELID",
                  "displayName": "CHANNELNAME",
                  "conversationIdentityType": "channel",
                  "conversationIdentityType@odata.type": "#Microsoft.Teams.GraphSvc.conversationIdentityType"
                }
              }"""

        return mention.replace("CHANNELNAME", self.channel_name).replace("CHANNELID", self.channel_id)


class ChannelConnectorCard:
    def __init__(self, webhook_url, http_timeout=60):
        self.http = urllib3.PoolManager()
        self.payload = {}
        self.hookurl = webhook_url
        self.http_timeout = http_timeout

    def _create_mention_payload(self, mention: ChannelWideMention):
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
            "version": "1.4",
            "msteams": {
                "entities": [
                    ENTITY
                ]
            }
        }
    }]
}"""
        return json.replace("ENTITY", mention.export_as_json()).replace("XXX", mention.channel_name)

    def text(self, mention: ChannelWideMention):
        self.payload = self._create_mention_payload(mention)
        return self

    def send(self):
        headers = {"Content-Type": "application/json"}
        r = self.http.request(
            'POST',
            f'{self.hookurl}',
            body=self.payload,
            headers=headers, timeout=self.http_timeout)
        if r.status == 200:
            return True
        else:
            raise TeamsWebhookException(r.reason)

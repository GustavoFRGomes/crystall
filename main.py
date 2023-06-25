import argparse

from messenger.teams.user_mention_messenger import MentionConnectorCard, UserMention
from resolver.name_resolver import GitTeamsNameResolver
from utils.args_validator import validate_args

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--webhook', required=True, help='Webhook URL for the Teams Channel')
parser.add_argument('-r', '--resolver', required=True, help='Filepath to the name resolver mapping file')
parser.add_argument('-i', '--user-info', required=True, help='User info to be matched against resolver for Teams')
parser.add_argument('-m', '--message', required=True, help='Message to be sent mentioned the user (User placeholder is USER)')

args = parser.parse_args()

class GitTeamsNameResolver:
    def __init__(self, resolver_file_path: str):
        self.matching_list = dict()
        resolver_file = open(resolver_file_path, 'r')
        resolver_file.readline()  # reads first line with column names

        for line in resolver_file:
            (teams_user, teams_email, git_email) = self._get_item_from_line(line)
            self.matching_list[git_email] = (teams_user, teams_email)

    def resolve(self, committer_email: str) -> tuple[str, str]:
        if committer_email in self.matching_list:
            return self.matching_list[committer_email]
        return None

    def resolve_git_input(self, provided_string: str):
        # for Git to Teams it provides the name of the committer and their email
        committer_email = provided_string.split(' ')[-1]

        return self.resolve(committer_email)

    def _get_item_from_line(line: str):
        teams_name, teams_email, _, git_email = line.split(':')
        return tuple(teams_name.strip(), teams_email.strip(), git_email.strip())

@staticmethod
def _create_mention_payload(self, teams_username: str, teams_email: str, message_with_placeholder: str) -> str:
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
                    "text": "MESSAGE"
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
                              "name": "USERNAME"
                        }
                    }
                ]
            }
        }
    }]
}"""
        return json.replace("USERNAME", teams_username).replace("EMAIL", teams_email).replace("MESSAGE", message_with_placeholder)

@staticmethod
def send(webhook_url, payload, http_timeout=60):
        http = urllib3.PoolManager()

        response = http.request(
            'POST',
            f'{webhook_url}',
            body=payload,
            headers={"Content-Type": "application/json"},
            timeout=http_timeout)
        if response.status == 200:
            return True
        else:
            raise Exception(response.reason)

def notify_user(webhook_url: str, teams_user_name: str, teams_email: str, message: str):
    message_payload = _create_mention_payload(teams_user_name, teams_email, args.message)
    send(webhook_url, message_payload)


if __name__ == '__main__':
    # Because arguments in argparse are REQUIRED we don't need to check much

    # Assumes the validation or args discards both usages Email/Name and Resolver/User Info
    if args.resolver:
        name_resolver = GitTeamsNameResolver(args.resolver)
        (teams_username, teams_email) = name_resolver.resolve_git_input(args.user_info)

        if teams_username is None or teams_email is None:
            print("Invalid user info, no match found in supplied name resolution file...")
            exit(-1)

        resolved_email = teams_email
        resolved_user_name = teams_username

        notify_user(args.webhook, resolved_user_name, resolved_email, args.message)
    else:
        print(args.user_email)

import argparse

from messenger.teams.user_mention_messenger import MentionConnectorCard, UserMention
from resolver.name_resolver import GitTeamsNameResolver
from utils.args_validator import validate_args

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--webhook', required=True, help='Webhook URL for the Teams Channel')
parser.add_argument('-c', '--channel', required=False, help='Teams Channel Name')
parser.add_argument('-e', '--user-email', required=False, help='User email in the Teams Channel')
parser.add_argument('-n', '--user-name', required=False, help='User name in the Teams Channel')
parser.add_argument('-r', '--resolver', required=False, help='Filepath to the name resolver mapping file')
parser.add_argument('-i', '--user-info', required=False, help='User info to be matched against resolver for Teams')

args = parser.parse_args()


def notify_user(webhook_url: str, teams_user_name: str, teams_email: str):
    teams_connector = MentionConnectorCard(webhook_url)

    teams_user_mention = UserMention(teams_user_name, teams_email)

    teams_connector.mention(teams_user_mention)
    teams_connector.send()


if __name__ == '__main__':
    validate_args(args)

    # Assumes the validation or args discards both usages Email/Name and Resolver/User Info
    if args.resolver:
        name_resolver = GitTeamsNameResolver(args.resolver)
        name_resolution_result = name_resolver.resolve_git_input(args.user_info)

        if name_resolution_result is None:
            print("Invalid user info, no match found in supplied name resolution file...")
            exit(1)

        resolved_email = name_resolution_result.teams_email
        resolved_user_name = name_resolution_result.teams_name

        notify_user(args.webhook, resolved_user_name, resolved_email)
    else:
        print(args.user_email)

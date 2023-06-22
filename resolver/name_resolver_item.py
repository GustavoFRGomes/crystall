class GitTeamsNameResolverItem:
    def __init__(self, teams_name: str, teams_email: str, git_name: str, git_email: str):
        self.teams_name = teams_name
        self.teams_email = teams_email
        self.git_name = git_name
        self.git_email = git_email

    @staticmethod
    def from_line(line: str):
        teams_name, teams_email, git_name, git_email = line.split(':')
        return GitTeamsNameResolverItem(teams_name.strip(), teams_email.strip(), git_name.strip(),
                                        git_email.strip())

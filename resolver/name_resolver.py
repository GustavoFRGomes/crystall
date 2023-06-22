# This class is used to resolve the name of the file to the name of the class
from resolver.name_resolver_item import GitTeamsNameResolverItem


class GitTeamsNameResolver:
    def __init__(self, resolver_file_path: str):
        self.matching_list = dict()
        resolver_file = open(resolver_file_path, 'r')
        resolver_file.readline()  # reads first line with column names

        for line in resolver_file:
            resolver_item = GitTeamsNameResolverItem.from_line(line)
            self.matching_list[resolver_item.git_email] = resolver_item

    def resolve(self, committer_email: str):
        if committer_email in self.matching_list:
            return self.matching_list[committer_email]
        return None

    def resolve_git_input(self, provided_string: str):
        # for Git to Teams it provides the name of the committer and their email
        committer_email = provided_string.split(' ')[-1]

        if committer_email in self.matching_list:
            return self.matching_list[committer_email]
        return None

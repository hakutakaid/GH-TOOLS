def create_repo(client, name, private=False, description="", org=None):
    """
    Wrapper ringan untuk membuat repo.
    client: instance modules.github_client.GitHubClient
    """
    return client.create_repo(name=name, private=private, description=description, org=org)
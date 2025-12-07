def get_repo(client, owner, repo):
    """
    Kembalikan data repository.
    """
    return client.get_repo(owner, repo)
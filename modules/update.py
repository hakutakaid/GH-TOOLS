def update_repo(client, owner, repo, **kwargs):
    """
    Update repository; kwarg bisa berisi 'name', 'description', 'private', dll.
    """
    return client.update_repo(owner, repo, **kwargs)
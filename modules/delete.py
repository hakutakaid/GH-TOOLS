def delete_repo(client, owner, repo):
    """
    Hapus repository. Mengembalikan None pada keberhasilan (204),
    atau melempar exception jika gagal.
    """
    return client.delete_repo(owner, repo)
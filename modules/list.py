def list_repos(client, visibility="all", per_page=100):
    """
    Kembalikan daftar repository user yang terautentikasi.
    """
    results = []
    page = 1
    while True:
        batch = client.list_repos(visibility=visibility, per_page=per_page, page=page)
        if not batch:
            break
        results.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return results
import requests

class GitHubAPIError(Exception):
    pass

class GitHubClient:
    API_URL = "https://api.github.com"

    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "python-requests-github-client"
        })

    def _request(self, method, path, **kwargs):
        url = f"{self.API_URL}{path}"
        resp = self.session.request(method, url, **kwargs)
        if resp.status_code >= 400:
            # Attempt to surface a helpful error
            try:
                err = resp.json()
            except ValueError:
                err = resp.text
            raise GitHubAPIError(f"{resp.status_code} {resp.reason}: {err}")
        if resp.status_code == 204:
            return None
        try:
            return resp.json()
        except ValueError:
            return resp.text

    def get_authenticated_user(self):
        data = self._request("GET", "/user")
        return data.get("login")

    def create_repo(self, name, private=False, description="", org=None):
        body = {"name": name, "private": private, "description": description}
        if org:
            return self._request("POST", f"/orgs/{org}/repos", json=body)
        return self._request("POST", "/user/repos", json=body)

    def delete_repo(self, owner, repo):
        # Returns None on success (204)
        return self._request("DELETE", f"/repos/{owner}/{repo}")

    def list_repos(self, visibility="all", per_page=100, page=1):
        params = {"visibility": visibility, "per_page": per_page, "page": page}
        return self._request("GET", "/user/repos", params=params)

    def get_repo(self, owner, repo):
        return self._request("GET", f"/repos/{owner}/{repo}")

    def update_repo(self, owner, repo, **kwargs):
        return self._request("PATCH", f"/repos/{owner}/{repo}", json=kwargs)
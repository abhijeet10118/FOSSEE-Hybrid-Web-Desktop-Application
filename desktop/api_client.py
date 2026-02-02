import requests

DEFAULT_BASE = "http://127.0.0.1:8000/api"


class ApiClient:
    def __init__(self, base_url=None, username=None, password=None):
        self.base = base_url or DEFAULT_BASE
        self.auth = (username, password) if (username and password) else None

    def set_auth(self, username, password):
        self.auth = (username, password)

    def _request(self, method, path, **kwargs):
        url = f"{self.base.rstrip('/')}/{path.lstrip('/')}"
        kwargs.setdefault("auth", self.auth)
        kwargs.setdefault("timeout", 30)
        r = requests.request(method, url, **kwargs)
        r.raise_for_status()
        if r.headers.get("content-type", "").startswith("application/json"):
            return r.json()
        return r

    def login(self, username, password):
        self.set_auth(username, password)
        self._request("GET", "history/")
        return True

    def upload_csv(self, file_path):
        with open(file_path, "rb") as f:
            files = {"file": (file_path.split("/")[-1].split("\\")[-1], f, "text/csv")}
            return self._request("POST", "upload/", files=files)

    def get_history(self):
        return self._request("GET", "history/")

    def get_dataset(self, dataset_id):
        return self._request("GET", f"datasets/{dataset_id}/")

    def download_pdf(self, dataset_id, save_path):
        url = f"{self.base.rstrip('/')}/datasets/{dataset_id}/pdf/"
        r = requests.get(url, auth=self.auth, timeout=30)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(r.content)
        return save_path

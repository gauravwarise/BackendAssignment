import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class GetMovies(object):

    @staticmethod
    def getMovies(url=None, username=None, password=None, verify=None):
        retry_strategy = Retry(total=4,backoff_factor=2,status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("http://", adapter)
        response = session.get(url, auth=(username, password), verify=verify)
        if response.status_code == 200:
            data = response.json()
        else:
            data = {
                "message": "Failed to load movies, please try again.",
                "status_code": response.status_code,
            }
        return data

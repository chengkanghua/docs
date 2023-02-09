import json
import requests

from config import HTTP_SERVER_URL


class Request(object):
    def __init__(self):
        self.server_url = HTTP_SERVER_URL

    def get(self, url, headers):
        result = requests.get(url=self.server_url+url, headers=headers)
        return result

    def post(self, url, data, headers):
        result = requests.post(url=self.server_url+url, headers=headers, data=json.dumps(data))
        return result

    def put(self, url, data, headers):
        result = requests.put(url=self.server_url+url, headers=headers, data=json.dumps(data))
        return result

    def patch(self, url, data, headers):
        result = requests.patch(url=self.server_url+url, headers=headers, data=json.dumps(data))
        return result

    def delete(self, url, headers):
        result = requests.delete(url=self.server_url+url, headers=headers)
        return result

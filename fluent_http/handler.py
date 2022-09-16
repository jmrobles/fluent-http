from logging import StreamHandler, LogRecord
import json

import requests
from requests.auth import HTTPBasicAuth

class FluentHttpHandler(StreamHandler):

    def __init__(self, url: str = 'localhost', port: int = 9880, tag: str = 'fluent.info', username: str = None, password: str = None):

        StreamHandler.__init__(self)
        self.url = url
        self.port = port
        self.tag = tag
        self.username = username
        self.password = password


    def emit(self, record: LogRecord) -> None:

        msg = self.format(record)
        data = self._serialize(msg)
        url = self._build_url()
        auth = None
        if self.username is not None and self.password is not None:
            auth = HTTPBasicAuth(self.username, self.password)
        headers = {
            'Content-type': 'application/json'
        }
        resp = requests.post(url, data, headers=headers, auth=auth)

    def _build_url(self):

        return f'{self.url}:{self.port}/{self.tag}'

    def _serialize(self, msg):

        try:
            json.loads(msg)
            return msg
        except ValueError:
            return json.dumps({'message': msg})

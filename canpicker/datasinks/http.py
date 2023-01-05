import logging
from requests import get
from string import Template
from urllib.parse import quote

LOGGER = logging.getLogger(__name__)

class Http:
    def __init__(self, url_template, username, password):
        self.template = Template(url_template)
        self.auth = (username, password) if username else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def send(self, values):
        for value in values:
            url = self.template.substitute({
                'timestamp': value[0].isoformat(),
                'name': quote(value[1]),
                'value': quote(value[2])
            })
            LOGGER.info(f'Send HTTP request to {url}')
            response = get(url, auth=self.auth)
            if (response.status_code != 200):
                LOGGER.error(f'Calling {url} returned status code {response.status_code}')

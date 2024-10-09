import json
import requests
import os
from dotenv import load_dotenv
import logging


class HttpController:
    def __init__(self) -> None:
        load_dotenv(dotenv_path="../.env")
        self.BASE_URL = os.getenv("API_BASE_URL")
        self.logger = logging.getLogger(__name__)

    def send_request(self, path, type="GET", headers={}, payload={}):
        url = self.BASE_URL + path
        response = requests.request(type, url, headers=headers, data=payload)

        return response.text

    def save_height(self, height):
        path = "/height/save"
        headers = {"height": str(height)}

        try:
            self.send_request(path, "POST", headers)
        except Exception as e:
            self.logger.exception("failed to save height: ", e)

    def get_current_height(self):
        path = "/height/current"
        try:
            json_string = self.send_request(path, "GET")
            data = json.loads(json_string)
            height = data["height"]

            return height
        except Exception as e:
            self.logger.exception("failed to load height: ", e)
            return 0


http_controller = HttpController()

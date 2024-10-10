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

    def send_request(self, path, type="GET", headers=None, payload=None):
        url = self.BASE_URL + path
        headers = headers or {}
        payload = payload or {}

        try:
            response = requests.request(type, url, headers=headers, data=payload)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"HTTP request failed: {e}")
            raise

    def save_height(self, height):
        path = "/height/save"
        headers = {"height": str(height)}

        try:
            self.send_request(path, "POST", headers)
        except Exception as e:
            self.logger.exception("failed to save height")

    def get_current_height(self):
        path = "/height/current"
        try:
            json_string = self.send_request(path, "GET")
            data = json.loads(json_string)

            if "height" not in data:
                self.logger.error(
                    "'height' key not found in get_current_height response"
                )
                return 0

            height = data["height"]

            return height
        except Exception as e:
            self.logger.exception("failed to load height")
            return 0


http_controller = HttpController()

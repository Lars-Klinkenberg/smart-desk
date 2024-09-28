import json
import requests
import os
from dotenv import load_dotenv


class HttpController:
    def __init__(self) -> None:
        load_dotenv(dotenv_path="../.env")
        self.BASE_URL = os.getenv("API_BASE_URL")

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
            print("ERROR - failed saving height: ", e)

    def get_current_height(self):
        path = "/height/current"
        try:
            json_string = self.send_request(path, "GET")
            data = json.loads(json_string)
            height = data["height"]

            return height
        except Exception as e:
            print("ERROR - failed to load start height: ", e)
            return 0


http_controller = HttpController()

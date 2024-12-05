import json
import os
from dotenv import load_dotenv
from shared.http_service import send_request
from shared.logger import log


class HttpController:
    def __init__(self) -> None:
        load_dotenv(dotenv_path="../.env")
        self.BASE_URL = os.getenv("API_BASE_URL")

    def save_height(self, height):
        path = "/height/save"
        headers = {"height": str(height)}

        try:
            send_request(self.BASE_URL + path, "POST", headers)
        except Exception:
            log("desk_controller", "ERROR", "failed to save height")

    def get_current_height(self):
        path = "/height/current"
        try:
            json_string = send_request(self.BASE_URL + path, "GET")
            data = json.loads(json_string)

            if "height" not in data:
                log(
                    "desk_controller",
                    "ERROR",
                    "'height' key not found in get_current_height response",
                )
                return 0

            height = data["height"]

            return height
        except Exception as e:
            log("desk_controller", "ERROR", f"failed to load height: {e}")
            return 0


http_controller = HttpController()

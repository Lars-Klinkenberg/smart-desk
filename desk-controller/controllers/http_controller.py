import requests
import os
from dotenv import load_dotenv

class HttpController:
    def __init__(self) -> None:
        load_dotenv(dotenv_path="../.env")
        self.BASE_URL = os.getenv("API_BASE_URL")
    
    def save_height(self, height):
        # TODO: add error handling
        # TODO: add response handling
        path = "/height/save"
        headers = {'height': str(height)}
        self.send_request(path, "POST", headers)
    
    def send_request(self, path, type = "GET", headers = {}, payload = {}):
        url = self.BASE_URL + path
        response = requests.request(type, url, headers=headers, data=payload)

        print(response.text)
        
        
http_controller = HttpController()
 


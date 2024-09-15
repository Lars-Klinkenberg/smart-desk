import requests
import os

class HttpController:
    BASE_URL = os.getenv("API_BASE_URL")
    
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
 


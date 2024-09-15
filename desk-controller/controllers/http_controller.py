import requests

class HttpController:
    def save_height(self, height):
        # TODO: add error handling
        # TODO: add response handling
        path = "/height/save/{}"
        self.send_request(path.format(height))
    
    def send_request(self, path, type = "GET", headers = {}, payload = {}):
        print(path)
        url = "http://localhost:8080" + path
        print(url)
        response = requests.request("GET", url, headers=headers, data=payload)



        print(response.text)
        
        
http_controller = HttpController()
 


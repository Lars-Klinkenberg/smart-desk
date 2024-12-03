import requests

def send_request(url, type="GET", headers=None, payload=None):
    headers = headers or {}
    payload = payload or {}

    try:
        response = requests.request(type, url, headers=headers, data=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.RequestException as e:
        raise 

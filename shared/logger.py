import logging
import os
import requests

from shared.http_service import send_request

def log(service_name, level, message):
    try:
        payload = {
            "service_name": service_name,
            "level": level,
            "message": message
        }
        url = os.getenv("API_BASE_URL")+ "/monitoring/logs/save_log"
        send_request(url, "POST", payload)
        return
    except requests.RequestException as e:
        logToFile(f"HTTP request failed: {e}")
    except Exception as e:
        logToFile(f"Error sending log: {e}")
        
def logToFile(message):
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="logger.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    logger.critical(message)
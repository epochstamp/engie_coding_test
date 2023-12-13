import requests
import json

from config import API_LINK

if __name__ == "__main__":
    api_url = API_LINK
    with open("payloads/payload2.json") as payload_file:
        payload = json.load(payload_file)
    response = requests.post(api_url, json=payload)
    print(response.json())
    print(response.status_code)
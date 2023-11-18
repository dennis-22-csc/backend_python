# api_client.py

import requests

class APIClient:
    def get_data(self):
        response = requests.get('https://denniscode.tech/data')
        return response

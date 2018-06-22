import json
import requests

class v1:
    key = None

    def __init__(self, key):
        self.key = key

    def holidays(self, parameters):
        url = 'https://holidayapi.com/v1/holidays?'

        if 'key' not in parameters:
            parameters['key'] = self.key

        response = requests.get(url, params=parameters);
        data     = json.loads(response.text)

        if response.status_code != 200:
            if 'error' not in data: 
                data['error'] = 'Unknown error.'

        return data


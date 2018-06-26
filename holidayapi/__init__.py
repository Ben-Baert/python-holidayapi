import requests


class Api:
    key = None

    def __init__(self, key):
        self.key = key

    def holidays(self, parameters):
        url = 'https://holidayapi.com/v1/holidays?'

        if 'key' not in parameters:
            parameters['key'] = self.key

        r = requests.get(url, params=parameters)
        json = r.json() 

        if r.status_code != 200:
            if 'error' not in data: 
                data['error'] = 'Unknown error.'

        return data


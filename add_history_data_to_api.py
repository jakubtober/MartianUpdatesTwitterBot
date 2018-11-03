import json
import requests
from app_auth import (
    API_USERNAME,
    API_PASSWORD,
)


class HistoryData():
    AUTH_URL = 'http://jakubtober.pythonanywhere.com/api/token-auth/'
    GET_URL = 'http://jakubtober.pythonanywhere.com/api/sols/'
    CREATE_URL = 'http://jakubtober.pythonanywhere.com/api/sols/create/'

    def __init__(self):
        try:
            self.my_file = open('mars_rems_data.json')
            self.my_json = json.load(self.my_file)
        except Exception as error:
            raise error

        try:
            data = {
                'username': API_USERNAME,
                'password': API_PASSWORD
            }
            self.response = requests.post(self.AUTH_URL, data)
            self.token = self.response.json()['token']
        except Exception as error:
            raise error

    def __len__(self):
        return len(self.my_json)

    @property
    def auth_headers(self):
        my_auth_headers = {
            'Authorization': 'Token {}'.format(self.token)
        }
        return my_auth_headers

    def get_single_sol(self, sol_number):
        return self.my_json[str(sol_number)]

    def add_single_sol_to_api(self, sol_number):
        data_to_add = self.get_single_sol(sol_number)

        if self.token:
            check_sol_exists_response = requests.get(self.GET_URL + str(sol_number))
            if check_sol_exists_response.status_code != 200:
                response = requests.post(self.CREATE_URL, data=data_to_add,
                                         headers=self.auth_headers)
                return True
            else:
                return False

    def add_all_sols_to_api(self):
        for counter, sol_number in enumerate(self.my_json):
            if self.add_single_sol_to_api(sol_number):
                print('Sols left: ' + str(len(self.my_json) - counter))
            else:
                print('Sol {} not added - already in the database, or data incorrect'.format(sol_number))


if __name__ == '__main__':
    data = HistoryData()
    data.add_all_sols_to_api()

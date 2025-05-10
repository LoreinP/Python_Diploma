import requests


class MainPage:
    BASE_URL = "https://api.kinopoisk.dev/v1.4"

    def get_token(self, user=' ', password=' '):
        creds = {
        'username': user,
        'password': password
        }
        resp = requests.post(BASE_URL + '/auth/login', json=creds)
        return resp.json()["user_token"]

    def authenticate_kinopoisk(self, kinopoisk):
        response = requests.post(f"{self.BASE_URL}/auth", json={"kinopoisk"})
        return response

    def get_kinopoisk_info(self, kinopoisk_id):
        response = requests.get(f"{self.BASE_URL}/kinopoisk/")
        return response
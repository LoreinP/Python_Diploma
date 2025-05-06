import requests


def test_api(url, expected_name=None):
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Тест на {url}: Статус код - {response.status_code} (ОК)")
    else:
        print(f"Тест на {url}: Ожидаемый статус код 200, получен {response.status_code}")

tests = [
    {
        "name": "Поиск по названию",
        "url": "https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10",
        "expected_name": "Матрица"
    },
    {
        "name": "Поиск по автору",
        "url": "https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10",
        "expected_name": "Лили Вачовски"
    },
    {
        "name": "Поиск по актеру в главной роли",
        "url": "https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10",
        "expected_name": "Киану Ривз"
    },
    {
        "name": "Поиск с пустым полем",
        "url": "https://api.kinopoisk.dev/v1.4//search?page=1&limit=10",
        "expected_name": " "
    },
    {
        "name": "Поиск с тире",
        "url": "https://api.kinopoisk.dev/v1.4/p-e-r-s-o-n/search?page=1&limit=10",
        "expected_name": "К-и-а-н-у Р-и-в-з"
    },
]





import allure
import requests
import pytest

BASE_URL = 'https://api.kinopoisk.dev'
API_KEY = 'KSPJCHK-S44MSGS-JADGFSB-92SEAC2'
HEADERS = {"X-API-KEY": API_KEY}

@allure.feature("Search API")
@allure.story("Поиск фильма по названию")
def test_search_movie_by_title():
    response = requests.get(f"{BASE_URL}/v1.4/movie/search", params={"query": "Интерстеллар"}, headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["docs"][0]["name"] == "Интерстеллар"

@allure.feature("Movie API")
@allure.story("Получение фильма по ID")
def test_get_movie_by_id():
    response = requests.get(f"{BASE_URL}/v1.4/movie/301", headers=HEADERS)  # ID "Матрицы"
    assert response.status_code == 200
    assert response.json()["name"] == "Матрица"

@allure.feature("Search API")
@allure.story("Проверка пагинации")
def test_search_pagination():
    response_page1 = requests.get(f"{BASE_URL}/v1.4/movie/search", params={"query": "Матрица", "limit": 2, "page": 1}, headers=HEADERS)
    response_page2 = requests.get(f"{BASE_URL}/v1.4/movie/search", params={"query": "Матрица", "limit": 2, "page": 2}, headers=HEADERS)
    assert response_page1.json()["docs"][0]["id"] != response_page2.json()["docs"][0]["id"]

@allure.feature("Search API")
@allure.story("Фильтрация по году")
def test_filter_by_year():
    response = requests.get(f"{BASE_URL}/v1.4/movie", params={"year": 1999, "limit": 1}, headers=HEADERS)
    movie = response.json()["docs"][0]
    assert str(movie.get("year")) == "1999"

@allure.feature("Auth API")
@allure.story("Проверка ошибки 401")
def test_invalid_api_key():
    response = requests.get(f"{BASE_URL}/v1.4/movie/301", headers={"X-API-KEY": "invalid"})
    assert response.status_code in [401, 403]

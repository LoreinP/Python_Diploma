import pytest
import allure


@allure.suite("API Tests")
@allure.sub_suite("КиноПоиск API")
class TestKinopoiskAPI:

    @allure.feature("Поиск")
    @allure.story("Поиск по названию")
    @pytest.mark.parametrize("test_case", [
{
    "url": "https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=10",
    "expected_name": "Матрица"
},
{
    "url": "https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10",
    "expected_name": "Лили Вачовски"
},
{
    "url": "https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=10",
    "expected_name": "Киану Ривз"
},
{
    "url": "https://api.kinopoisk.dev/v1.4//search?page=1&limit=10",
    "expected_name": " "
},
{
    "url": "https://api.kinopoisk.dev/v1.4/p-e-r-s-o-n/search?page=1&limit=10",
    "expected_name": "К-и-а-н-у Р-и-в-з"
},
])
    def test_api(self, test_case):
        url = test_case["url"]
        expected_name = test_case["expected_name"]

        with allure.step(f"Отправка GET-запроса на {url}"):
            response = requests.get(url)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Ожидаемый статус код 200, получен {response.status_code}"
            allure.attach(body=str(response.json()), name="Response JSON", attachment_type=allure.attachment_type.JSON)

        with allure.step(f"Проверка наличия ожидаемого имени '{expected_name}' в ответе"):
            response_json = response.json()
            assert expected_name in response_json.get("name", ""), f"'{expected_name}' не найден в ответе"

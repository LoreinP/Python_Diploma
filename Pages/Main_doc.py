import pytest
import allure


from Pages.Main_page import MainPage

@allure.suite("Kinopoisk API Tests")
class TestKinopoiskAPI:

    main_page = MainPage()

    @allure.story("Тестирование получения токена")
    @allure.testcase("https://example.com/testcase/token")
    def test_get_token(self):
        token = self.main_page.get_token(user='your_username', password='your_password')
        assert token is not None, "Токен не должен быть пустым"

    @allure.story("Тестирование аутентификации Kinopoisk")
    @allure.testcase("https://example.com/testcase/authentication")
    def test_authenticate(self):
        token = self.main_page.get_token(user='your_username', password='your_password')
        response = self.main_page.authenticate_kinopoisk(kinopoisk="your_kinopoisk_id")
        assert response.ok, "Аутентификация не удалась"

    @allure.story("Тестирование получения информации о Kinopoisk")
    @allure.testcase("https://example.com/testcase/kinopoisk_info")
    def test_get_kinopoisk_info(self):
        kinopoisk_id = "some_id"
        response = self.main_page.get_kinopoisk_info(kinopoisk_id=kinopoisk_id)
        assert response.ok, "Не удалось получить информацию о Kinopoisk"

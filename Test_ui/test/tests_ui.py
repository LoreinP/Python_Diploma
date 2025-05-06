import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestKinopoiskApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("URL_ВАШЕГО_ПРИЛОЖЕНИЯ")

    def test_login(self):
        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.ID, "submit_button")

        username_field.send_keys("логин")
        password_field.send_keys("пароль")
        login_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "welcome_message"))
        )
        self.assertIn("Добро пожаловать", self.driver.page_source)

    def test_invalid_login(self):

        username_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        password_field = self.driver.find_element(By.NAME, "password")
        login_button = self.driver.find_element(By.ID, "submit_button")

        username_field.send_keys("неверный_логин")
        password_field.send_keys("неверный_пароль")
        login_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "error_message"))
        )
        self.assertIn("Ошибка: неверный логин или пароль", self.driver.page_source)

    def test_view_movie_details(self):

        movie_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Матрица"))
        )
        movie_link.click()

        # Ожидаем отображение информации о фильме
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "movie_details"))
        )
        self.assertIn("Информация о фильме", self.driver.page_source)

    def test_search_movie(self):
        # Тест на поиск фильма
        search_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "search"))
        )
        search_button = self.driver.find_element(By.ID, "search_button")

        search_field.send_keys("Матрица")
        search_button.click()

        # Ожидаем отображение результатов поиска
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "search_results"))
        )
        self.assertIn("Матрица", self.driver.page_source)

    def test_logout(self):
        # Тест на выход из системы
        logout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_button"))
        )
        logout_button.click()

        # Ожидаем, что пользователь был выведен
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login_page"))
        )
        self.assertIn("Вход", self.driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
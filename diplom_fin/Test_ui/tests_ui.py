import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import allure
import time


@pytest.fixture(scope="function")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@allure.feature("UI Тесты Кинопоиска")
class TestKinopoiskUI:
    # ... (остальные методы остаются без изменений)

    @allure.story("Авторизация с обходом капчи")
    def test_login_bypass_captcha(self, browser):
        with allure.step("1. Открыть страницу авторизации"):
            browser.get("https://www.kinopoisk.ru/")
            self.accept_cookies(browser)
            self.wait_and_click(browser, "//button[contains(., 'Войти')]")

        with allure.step("2. Заполнить форму авторизации"):
            login = "Pozd-L@bk.ru"
            password = "dfcbkbr684"  # Пароль "василий684" в английской раскладке

            browser.find_element(By.NAME, "login").send_keys(login)
            browser.find_element(By.NAME, "password").send_keys(password)

        with allure.step("3. Попытка обхода капчи"):
            try:
                # Вариант 1: Ввод капчи вручную с ожиданием
                input("Решите капчу в браузере и нажмите Enter в консоли...")

                # Вариант 2: Автоматический обход через тестовый ключ (если поддерживается)
                browser.execute_script("""
                    if (window.grecaptcha) {
                        window.grecaptcha.execute = function() {
                            return Promise.resolve("test-token");
                        };
                    }
                """)

                # Клик по кнопке "Войти"
                self.wait_and_click(browser, "//button[@type='submit']")

            except Exception as e:
                allure.attach(browser.get_screenshot_as_png(),
                              name="captcha_error",
                              attachment_type=allure.attachment_type.PNG)
                pytest.fail(f"Ошибка при обходе капчи: {str(e)}")

        with allure.step("4. Проверка успешной авторизации"):
            assert self.is_element_present(browser, "//div[contains(@class, 'avatar')]", 15), "Авторизация не удалась"
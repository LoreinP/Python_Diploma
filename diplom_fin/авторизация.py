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


def accept_cookies(browser):
    """Принять куки, если появилось окно"""
    try:
        cookie_btn = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Принять') or contains(., 'Accept')]")))
        cookie_btn.click()
        time.sleep(1)
    except:
        pass


def wait_and_click(browser, xpath, timeout=20):
    """Улучшенное ожидание и клик"""
    try:
        element = WebDriverWait(browser, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        return True
    except Exception as e:
        allure.attach(browser.get_screenshot_as_png(),
                      name=f"error_{xpath}",
                      attachment_type=allure.attachment_type.PNG)
        pytest.fail(f"Не удалось найти или кликнуть элемент: {xpath}. Ошибка: {str(e)}")


def is_element_present(browser, xpath, timeout=10):
    """Проверка наличия элемента"""
    try:
        WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except:
        return False


@allure.story("Авторизация с обработкой reCAPTCHA")
def test_login_with_captcha(browser):
    with allure.step("1. Открыть страницу авторизации"):
        browser.get("https://www.kinopoisk.ru/")
        accept_cookies(browser)
        wait_and_click(browser, "//button[contains(., 'Войти')]")

    with allure.step("2. Заполнить форму авторизации"):
        login = "Pozd-L@bk.ru"
        password = "dfcbkbr684"

        browser.find_element(By.NAME, "login").send_keys(login)
        browser.find_element(By.NAME, "password").send_keys(password)

    with allure.step("3. Обработка reCAPTCHA"):
        try:
            # Ждем появления iframe reCAPTCHA
            WebDriverWait(browser, 10).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
            )

            # Клик по чекбоксу "Я не робот"
            captcha_checkbox = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
            )
            captcha_checkbox.click()

            # Возвращаемся к основному контенту
            browser.switch_to.default_content()

            # Если появится дополнительная проверка (аудио/визуальная)
            if is_element_present(browser, "//iframe[contains(@title, 'проверка')]", 3):
                print("Требуется дополнительная проверка. Введите капчу вручную.")
                input("Решите капчу и нажмите Enter...")

        except Exception as e:
            allure.attach(browser.get_screenshot_as_png(),
                          name="captcha_error",
                          attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Ошибка при обработке reCAPTCHA: {str(e)}")

    with allure.step("4. Отправить форму"):
        wait_and_click(browser, "//button[@type='submit']")

    with allure.step("5. Проверить успешную авторизацию"):
        assert is_element_present(browser, "//div[contains(@class, 'avatar')]", 15), "Авторизация не удалась"
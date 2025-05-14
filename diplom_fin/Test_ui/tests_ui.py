import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import allure


@pytest.fixture(scope="function")
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(50)
    yield driver
    driver.quit()


def test_search_movie_by_name(browser):
    with allure.step("Открыть страницу кинопоиска"):
        browser.get("https://www.kinopoisk.ru/")
        browser.find_element(By.NAME, "kp_query").send_keys("матрица")
    with allure.step("Проверка выпадающего списка"):
        assert browser.find_element(By.ID, "suggest-item-film-301").is_displayed()


def test_negative_search(browser):
    with allure.step("Открыть страницу кинопоиска"):
        browser.get("https://www.kinopoisk.ru/")
        browser.find_element(By.NAME, "kp_query").send_keys("%%%%%%%")
    with allure.step("Проверка выпадающего списка"):
        assert browser.find_element(By.CSS_SELECTOR, "class*='emptySuggest").is_displayed()

def test_negative_search_by_actor(browser):
    with allure.step("Открыть страницу кинопоиска"):
        browser.get("https://www.kinopoisk.ru/")
        browser.find_element(By.NAME, "kp_query").send_keys("Киану Ривз")
    with allure.step("Проверка выпадающего списка"):
        assert browser.find_element(By.ID, "suggest-item-person-7836").is_displayed()

def test_negative_search_by_producer(browser):
    with allure.step("Открыть страницу кинопоиска"):
        browser.get("https://www.kinopoisk.ru/")
        browser.find_element(By.NAME, "kp_query").send_keys("Лили Вачовски")
    with allure.step("Проверка выпадающего списка"):
        assert browser.find_element(By.ID, "suggest-item-person-23329").is_displayed()

def test_negative_search_by_actor2(browser):
    with allure.step("Открыть страницу кинопоиска"):
        browser.get("https://www.kinopoisk.ru/")
        browser.find_element(By.NAME, "kp_query").send_keys("Лоренс Фишберн")
    with allure.step("Проверка выпадающего списка"):
        assert browser.find_element(By.ID, "suggest-item-person-9838").is_displayed()
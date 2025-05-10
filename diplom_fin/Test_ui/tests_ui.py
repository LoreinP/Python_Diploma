import pytest
from allure import feature, story, title
import re


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class FormValidator:
    @staticmethod
    def validate_phone_number(phone):
        pattern = r"^\+7-\d{3}-\d{3}-\d{2}-\d{2}$"
        return re.match(pattern, phone) is not None

    @staticmethod
    def validate_card_code(card_code):
        return card_code.isdigit() and len(card_code) == 3

    @staticmethod
    def validate_login(email, password):
        return bool(email) and bool(password)

# Тесты

@feature("Валидация форм")
class TestFormValidator:

    @story("Проверка валидности телефонных номеров")
    @title("Корректный номер телефоне")
    def test_valid_phone_number(self):
        assert FormValidator.validate_phone_number("+7-914-712-31-32") == True

    @story("Проверка валидности телефонных номеров")
    @title("Некорректный номер телефоне")
    def test_invalid_phone_number(self):
        assert FormValidator.validate_phone_number("+7-914-712-31-3A") == False

    @story("Проверка кодов карт")
    @title("Корректный код карты")
    def test_valid_card_code(self):
        assert FormValidator.validate_card_code("123") == True

    @story("Проверка кодов карт")
    @title("Некорректный код карты")
    def test_invalid_card_code(self):
        assert FormValidator.validate_card_code("12A") == False

    @story("Проверка логина пользователя")
    @title("Валидный логин")
    def test_valid_login(self):
        user = User("Pozd-L@bk.ru", "strong_password")
        assert FormValidator.validate_login(user.email, user.password) == True

    @story("Проверка логина пользователя")
    @title("Недостаточный логин")
    def test_invalid_login_empty_email(self):
        user = User("", "strong_password")
        assert FormValidator.validate_login(user.email, user.password) == False


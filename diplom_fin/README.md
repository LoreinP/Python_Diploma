Автоматизированное тестирование веб-приложения [Кинопоиск]

Проект автоматизированного тестирования, включающий UI и API тесты для веб-приложения. Содержит:
- 5+ UI-тестов на Selenium
- 5+ API-тестов на Requests
- Подробную документацию всех методов
- Allure-отчеты с пошаговым описанием тестов

Предварительные требования:
- Python 3.9+
- pip 20+
- Браузер Chrome (для UI-тестов)

Установка:
Клонируем репозиторий:
git clone [ваш-репозиторий]
cd [папка-проекта]

Устанавливаем зависимости:
pip install -r requirements.txt

Установить Allure (для генерации отчетов)
Для Windows:
scoop install allure
Для MacOs:
brew install allure

project/
├── config/
│   ├── __init__.py
│   ├── settings.py           # Конфигурация среды (URL, таймауты)
│   └── test_data.py          # Тестовые данные (users, tokens)
├── pages/                    # PageObject pattern
│   ├── base_page.py
│   ├── login_page.py
│   └── profile_page.py
├── tests/
│   ├── __init__.py
│   ├── test_api/             # API тесты
│   │   ├── auth_test.py
│   │   └── profile_test.py
│   └── test_ui/              # UI тесты
│       ├── login_test.py
│       └── profile_test.py
├── utilities/
│   ├── api_client.py         # API клиент
│   └── logger.py             # Логирование
├── requirements.txt
└── README.md

 **Запуск тестов**
1. Запуск всех тестов с генерацией Allure-отчета
pytest tests/ -v --alluredir=allure-results
allure serve allure-results
2. Запуск только API тестов
pytest tests/test_api/ -m "api" --alluredir=allure-results
3. Запуск только UI тестов
pytest tests/test_ui/ -m "ui" --alluredir=allure-results

**API тесты:**
tests/test_api/auth_test.py
Пример:
@allure.feature("API: Аутентификация")
class TestAuthAPI:
    @allure.story("Успешная авторизация")
    @allure.description("""
    Проверка успешной авторизации с валидными данными
    
    Входные данные:
    - email: valid@example.com
    - password: Qwerty123!
    
    Ожидаемый результат:
    - Status code: 200
    - В ответе присутствует access_token
    """)
    def test_successful_auth(self, api_client):
        with allure.step("Отправка запроса на авторизацию"):
            response = api_client.auth(
                email=test_data.VALID_EMAIL,
                password=test_data.VALID_PASSWORD
            )

**UI тесты:**
tests/test_ui/login_test.py
Пример:
@allure.feature("UI: Авторизация")
class TestLoginUI:
    @allure.story("Неуспешная авторизация")
    @allure.description("""
    Проверка отображения ошибки при неверных данных
    
    Шаги:
    1. Открыть страницу логина
    2. Ввести неверный email
    3. Ввести неверный пароль
    4. Нажать кнопку входа
    
    Ожидаемый результат:
    - Отображается сообщение об ошибке
    - Цвет сообщения - красный
    """)
    def test_invalid_credentials(self, driver):
        login_page = LoginPage(driver)
        
        with allure.step("Открытие страницы логина"):
            login_page.open()
            
        with allure.step("Ввод неверных данных"):
            login_page.enter_email("invalid@example.com")
            login_page.enter_password("WrongPass123")



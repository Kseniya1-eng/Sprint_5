"""
Фикстуры для Selenium-автотестов Stellar Burgers.
Все фикстуры проекта собраны в одном файле.
"""

import os
import sys

# Добавляем корень проекта в sys.path, чтобы при любом способе запуска pytest
# были доступны модули locators, helpers и data.
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import data
import helpers


@pytest.fixture
def driver():
    """
    Создаёт драйвер браузера для каждого теста и закрывает его в конце.

    Каждый тест автономен: браузер открывается для теста и закрывается
    через driver.quit() в teardown фикстуры.

    Браузер выбирается переменной окружения BROWSER (chrome | firefox),
    по умолчанию — Google Chrome. ChromeDriver подтягивается автоматически
    через Selenium Manager (дополнительно ничего ставить не нужно).
    Для запуска без окна используйте HEADLESS=1.
    """
    browser = os.getenv("BROWSER", "chrome").lower()

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if os.getenv("HEADLESS", "0") == "1":
            options.add_argument("--headless=new")
        browser_instance = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        if os.getenv("HEADLESS", "0") == "1":
            options.add_argument("--headless")
        browser_instance = webdriver.Firefox(options=options)
    else:
        raise ValueError(
            f"Неизвестный браузер: {browser}. Используйте BROWSER=chrome "
            "или BROWSER=firefox."
        )

    browser_instance.implicitly_wait(data.IMPLICIT_WAIT)
    browser_instance.maximize_window()

    yield browser_instance

    browser_instance.quit()


@pytest.fixture
def email() -> str:
    """Уникальный email для регистрации (подключает генератор логина)."""
    return helpers.generate_login()


@pytest.fixture
def password() -> str:
    """Корректный пароль (6 и более символов)."""
    return helpers.generate_password()


@pytest.fixture
def short_password() -> str:
    """Некорректный пароль (меньше 6 символов)."""
    return helpers.generate_short_password()


@pytest.fixture
def registered_user(driver):
    """
    Регистрирует нового пользователя через UI.

    После регистрации приложение редиректит на /login — с этой страницы
    удобно начинать тесты входа. Возвращает (email, password).
    """
    user_email = helpers.generate_login()
    user_password = helpers.generate_password()
    helpers.register_user(driver, user_email, user_password)
    return user_email, user_password


@pytest.fixture
def logged_in_user(driver, registered_user):
    """
    Регистрирует и авторизует пользователя через UI.

    Возвращает драйвер уже авторизованным — пользователь находится
    на главной странице (видна кнопка «Оформить заказ»).
    """
    user_email, user_password = registered_user
    helpers.login_user(driver, user_email, user_password)
    return user_email, user_password

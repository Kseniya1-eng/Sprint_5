"""Генераторы тестовых данных и вспомогательные UI-функции для тестов."""

import random
import string

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import data
import locators


def transliterate(text: str) -> str:
    """Транслитерирует русский текст в латиницу (для генерации email)."""
    mapping = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    return ''.join(mapping.get(ch, ch) for ch in text)


def generate_login(first_name=None, last_name=None, cohort=None,
                   domain=None, suffix=None) -> str:
    """
    Генерирует уникальный логин (email) для регистрации.

    Формат: имя_фамилия_номер_когорты_три_цифры@домен
    Например: kseniya_abramova_52_847@yandex.ru

    Имя и фамилия транслитерируются в латиницу, поэтому email не содержит
    кириллицы (как требует задание — «генерировать имейл не на русском»).

    Args:
        first_name: имя (по умолчанию из data.py)
        last_name: фамилия (по умолчанию из data.py)
        cohort: номер когорты (по умолчанию из data.py)
        domain: домен почты (по умолчанию из data.py)
        suffix: три цифры для уникальности (генерируются, если не задано)

    Returns:
        Строка-email в нижнем регистре.
    """
    first = transliterate(first_name or data.DEFAULT_NAME).lower()
    last = transliterate(last_name or data.DEFAULT_LAST_NAME).lower()
    cohort = cohort or data.COHORT
    domain = domain or data.EMAIL_DOMAIN
    suffix = suffix if suffix is not None else random.randint(100, 999)
    return f"{first}_{last}_{cohort}_{suffix}@{domain}"


def generate_password(length: int = 10) -> str:
    """Генерирует корректный пароль (6 и более символов)."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_short_password() -> str:
    """Генерирует некорректный пароль (меньше 6 символов)."""
    return ''.join(random.choices(string.ascii_letters, k=5))


# ---------------------------------------------------------------------------
# UI-функции для пошаговых действий в тестах
# ---------------------------------------------------------------------------

def wait_element(driver, locator):
    """Ожидает, что элемент виден и кликабелен, и возвращает его."""
    return WebDriverWait(driver, data.EXPLICIT_WAIT).until(
        EC.element_to_be_clickable(locator)
    )


def fill(driver, locator, value):
    """Ожидает поле ввода и вводит в него значение."""
    element = wait_element(driver, locator)
    element.clear()
    element.send_keys(value)
    return element


def register_user(driver, email: str, password: str, name: str = None) -> None:
    """
    Регистрирует нового пользователя через форму /register.

    После успешной регистрации приложение редиректит на страницу /login —
    это и есть признак успеха, который ожидается функцией.
    """
    name = name or data.DEFAULT_NAME
    driver.get(data.BASE_URL + "/register")
    fill(driver, locators.INPUT_NAME_REGISTER, name)
    fill(driver, locators.INPUT_EMAIL_REGISTER, email)
    fill(driver, locators.INPUT_PASSWORD_REGISTER, password)
    wait_element(driver, locators.BUTTON_REGISTER).click()
    # Ждём редиректа на страницу входа — регистрация прошла успешно
    WebDriverWait(driver, data.EXPLICIT_WAIT).until(
        EC.url_contains("/login")
    )


def login_user(driver, email: str, password: str) -> None:
    """
    Выполняет вход с текущей страницы /login.

    После успешного входа открывается главная страница. Признак успеха —
    появление кнопки «Оформить заказ», которую видит только авторизованный
    пользователь. На этот признак функция и ожидает.
    """
    fill(driver, locators.INPUT_EMAIL_LOGIN, email)
    fill(driver, locators.INPUT_PASSWORD_LOGIN, password)
    wait_element(driver, locators.BUTTON_LOGIN).click()
    # Авторизованного пользователя на главной встречает кнопка «Оформить заказ»
    WebDriverWait(driver, data.EXPLICIT_WAIT).until(
        EC.visibility_of_element_located(locators.BUTTON_ORDER)
    )

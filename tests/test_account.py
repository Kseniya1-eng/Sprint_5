"""
Автотесты личного кабинета: переход в кабинет, переход в конструктор
и выход из аккаунта.
"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import data
import helpers
import locators


class TestPersonalCabinet:
    """Работа с личным кабинетом и навигация по приложению."""

    def test_navigate_to_personal_cabinet(self, driver, logged_in_user):
        """Переход в личный кабинет по клику на «Личный Кабинет»."""
        helpers.wait_element(driver, locators.LINK_PERSONAL_CABINET).click()

        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.url_contains("/account/profile")
        )
        # В личном кабинете доступна кнопка «Выход»
        assert driver.find_element(*locators.BUTTON_LOGOUT).is_displayed()

    def test_navigate_to_constructor_by_link(self, driver, logged_in_user):
        """
        Переход из личного кабинета в конструктор по клику на «Конструктор».

        Открываем личный кабинет, затем кликаем «Конструктор» в шапке —
        должны оказаться на главной (конструкторе).
        """
        helpers.wait_element(driver, locators.LINK_PERSONAL_CABINET).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.url_contains("/account/profile")
        )

        helpers.wait_element(driver, locators.LINK_CONSTRUCTOR).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(locators.TITLE_MAIN)
        )
        assert driver.current_url.rstrip("/") == data.BASE_URL

    def test_navigate_to_constructor_by_logo(self, driver, logged_in_user):
        """
        Переход из личного кабинета в конструктор по логотипу Stellar Burgers.

        Открываем личный кабинет, затем кликаем по логотипу в шапке —
        должны оказаться на главной (конструкторе).
        """
        helpers.wait_element(driver, locators.LINK_PERSONAL_CABINET).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.url_contains("/account/profile")
        )

        helpers.wait_element(driver, locators.LOGO_LINK).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(locators.TITLE_MAIN)
        )
        assert driver.current_url.rstrip("/") == data.BASE_URL

    def test_logout(self, driver, logged_in_user):
        """Выход из аккаунта по кнопке «Выход» в личном кабинете."""
        helpers.wait_element(driver, locators.LINK_PERSONAL_CABINET).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.url_contains("/account/profile")
        )

        helpers.wait_element(driver, locators.BUTTON_LOGOUT).click()
        # После выхода открывается страница входа /login
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.url_contains("/login")
        )

"""Автотесты входа в аккаунт Stellar Burgers (все способы входа)."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import data
import helpers
import locators


class TestLogin:
    """Вход в аккаунт разными способами."""

    def test_login_via_main_button(self, driver, registered_user):
        """
        Вход по кнопке «Войти в аккаунт» на главной странице.

        Клик по кнопке открывает страницу входа /login, после ввода
        данных происходит вход (на главной появляется «Оформить заказ»).
        """
        user_email, user_password = registered_user
        driver.get(data.BASE_URL)

        # «Войти в аккаунт» на главной открывает страницу входа
        helpers.wait_element(driver, locators.BUTTON_LOGIN_MAIN).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(locators.INPUT_EMAIL_LOGIN)
        )

        helpers.login_user(driver, user_email, user_password)

    def test_login_via_personal_cabinet(self, driver, registered_user):
        """
        Вход через кнопку «Личный Кабинет» в шапке.

        Для неавторизованного пользователя «Личный Кабинет» открывает
        страницу входа /login.
        """
        user_email, user_password = registered_user
        driver.get(data.BASE_URL)

        helpers.wait_element(driver, locators.LINK_PERSONAL_CABINET).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(locators.INPUT_EMAIL_LOGIN)
        )

        helpers.login_user(driver, user_email, user_password)

    def test_login_via_register_form(self, driver, registered_user):
        """
        Вход через кнопку «Войти» в форме регистрации.

        С главной переходим на страницу входа, затем в форму регистрации,
        оттуда по ссылке «Войти» возвращаемся на /login и входим.
        """
        user_email, user_password = registered_user
        driver.get(data.BASE_URL)

        # На главной → «Войти в аккаунт» → страница входа
        helpers.wait_element(driver, locators.BUTTON_LOGIN_MAIN).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(locators.LINK_REGISTER)
        ).click()

        # В форме регистрации жмём «Войти» и возвращаемся на /login
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(locators.LINK_LOGIN_FROM_REGISTER)
        ).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(locators.INPUT_EMAIL_LOGIN)
        )

        helpers.login_user(driver, user_email, user_password)

    def test_login_via_forgot_password_form(self, driver, registered_user):
        """
        Вход через кнопку «Войти» в форме восстановления пароля.

        С главной переходим на страницу входа, затем в форму
        восстановления пароля, оттуда по ссылке «Войти» возвращаемся
        на /login и входим.
        """
        user_email, user_password = registered_user
        driver.get(data.BASE_URL)

        helpers.wait_element(driver, locators.BUTTON_LOGIN_MAIN).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(locators.LINK_FORGOT_PASSWORD)
        ).click()

        # В форме восстановления пароля жмём «Войти» → возвращаемся на /login
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(locators.LINK_LOGIN_FROM_RECOVERY)
        ).click()
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(locators.INPUT_EMAIL_LOGIN)
        )

        helpers.login_user(driver, user_email, user_password)

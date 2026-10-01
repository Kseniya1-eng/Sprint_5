"""Автотесты регистрации пользователя в Stellar Burgers."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import data
import helpers
import locators


class TestRegistration:
    """Регистрация: успешная и ошибка для некорректного пароля."""

    def test_successful_registration(self, driver, email, password):
        """
        Успешная регистрация.

        Поле «Имя» не пустое, email в формате логин@домен,
        пароль от 6 символов. После успешной регистрации приложение
        редиректит на страницу входа /login.
        """
        helpers.register_user(driver, email, password)

        # Признак успешной регистрации — редирект на страницу входа
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.url_contains("/login")
        )
        # На странице входа должна быть кнопка «Войти»
        assert driver.find_element(*locators.BUTTON_LOGIN).is_displayed()

    def test_registration_short_password_error(self, driver, email):
        """
        Ошибка при регистрации с паролем короче 6 символов.

        Приложение показывает сообщение «Некорректный пароль»
        и остаётся на странице регистрации.
        """
        driver.get(data.BASE_URL + "/register")

        helpers.fill(driver, locators.INPUT_NAME_REGISTER, data.DEFAULT_NAME)
        helpers.fill(driver, locators.INPUT_EMAIL_REGISTER, email)
        helpers.fill(driver, locators.INPUT_PASSWORD_REGISTER,
                     helpers.generate_short_password())
        helpers.wait_element(driver, locators.BUTTON_REGISTER).click()

        # Появляется сообщение об ошибке валидации пароля
        error = WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(locators.ERROR_INVALID_PASSWORD)
        )
        assert "Некорректный пароль" in error.text
        # Остались на странице регистрации (регистрация не выполнена)
        assert "/register" in driver.current_url

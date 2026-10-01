"""Автотесты переходов к разделам конструктора: «Булки», «Соусы», «Начинки»."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import data
import locators


class TestConstructorSections:
    """Переключение вкладок разделов в конструкторе на главной странице."""

    def test_switch_to_buns_section(self, driver):
        """Переход к разделу «Булки»."""
        driver.get(data.BASE_URL)
        # Сначала уходим на «Соусы», чтобы проверить реальный переход на «Булки»
        self._switch_to_tab(driver, locators.TAB_SAUCES, locators.TAB_SAUCES_HEADER)
        self._switch_to_tab(driver, locators.TAB_BUNS, locators.TAB_BUNS_HEADER)

    def test_switch_to_sauces_section(self, driver):
        """Переход к разделу «Соусы»."""
        driver.get(data.BASE_URL)
        self._switch_to_tab(driver, locators.TAB_SAUCES, locators.TAB_SAUCES_HEADER)

    def test_switch_to_fillings_section(self, driver):
        """Переход к разделу «Начинки»."""
        driver.get(data.BASE_URL)
        self._switch_to_tab(driver, locators.TAB_FILLINGS, locators.TAB_FILLINGS_HEADER)

    def _switch_to_tab(self, driver, tab_locator, tab_header_locator):
        """Кликает по вкладке и ожидает, что она станет активной.

        Активная вкладка определяется приложением по позиции прокрутки
        списка, поэтому после клика ждём (поллинг), пока у контейнера
        вкладки появится класс активной вкладки.
        """
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(tab_locator)
        ).click()

        # Ждём, пока вкладка станет активной (позиция прокрутки обновляется)
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            lambda d: locators.TAB_ACTIVE_CLASS in
            (d.find_element(*tab_header_locator).get_attribute("class") or "")
        )

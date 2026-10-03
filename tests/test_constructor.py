"""Автотесты переходов к разделам конструктора: «Булки», «Соусы», «Начинки»."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import data
import locators


class TestConstructorSections:
    """Переключение вкладок разделов в конструкторе на главной странице."""

    def test_switch_to_buns_section(self, driver):
        """Переход к разделу «Булки»: активной становится вкладка «Булки»."""
        driver.get(data.BASE_URL)
        # Сначала уходим на «Соусы», чтобы проверить реальный переход на «Булки»
        self._open_tab(driver, locators.TAB_SAUCES)
        self._wait_active(driver, locators.TAB_SAUCES_HEADER, locators.TAB_BUNS_HEADER)

        self._open_tab(driver, locators.TAB_BUNS)
        self._wait_active(driver, locators.TAB_BUNS_HEADER, locators.TAB_SAUCES_HEADER)

    def test_switch_to_sauces_section(self, driver):
        """Переход к разделу «Соусы»: активной становится вкладка «Соусы»."""
        driver.get(data.BASE_URL)
        self._open_tab(driver, locators.TAB_SAUCES)
        self._wait_active(driver, locators.TAB_SAUCES_HEADER, locators.TAB_BUNS_HEADER)

    def test_switch_to_fillings_section(self, driver):
        """Переход к разделу «Начинки»: активной становится вкладка «Начинки»."""
        driver.get(data.BASE_URL)
        self._open_tab(driver, locators.TAB_FILLINGS)
        self._wait_active(driver, locators.TAB_FILLINGS_HEADER, locators.TAB_BUNS_HEADER)

    @staticmethod
    def _open_tab(driver, tab_locator):
        """Ожидает готовности конструктора и кликает по вкладке.

        Ожидаем видимый заголовок конструктора (страница загрузилась) и
        кликабельную вкладку — это покрывает и период анимации загрузки.
        Клик выполняем через JS: Selenium-клик по <span> вкладки может
        перехватываться родительским блоком (ошибка
        ElementClickInterceptedException).
        """
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(locators.TITLE_MAIN)
        )
        tab = WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.element_to_be_clickable(tab_locator)
        )
        driver.execute_script("arguments[0].click();", tab)

    @staticmethod
    def _is_active(driver, tab_header_locator) -> bool:
        """True, если контейнер вкладки помечен классом активной вкладки."""
        classes = driver.find_element(*tab_header_locator).get_attribute("class") or ""
        return locators.TAB_ACTIVE_CLASS in classes

    @staticmethod
    def _wait_active(driver, tab_header_locator, prev_header_locator):
        """Ожидает устоявшееся состояние: целевая вкладка активна, предыдущая — нет.

        Во время плавной прокрутки класс активной вкладки на короткое время
        появляется и у промежуточных вкладок (овершут/откат скролла), поэтому
        недостаточно дождаться первого появления класса у цели. Ждём, пока
        активной останется только целевая вкладка. Если это так и не наступило,
        WebDriverWait бросит TimeoutException — тест упадёт.
        """
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            lambda d: (
                TestConstructorSections._is_active(d, tab_header_locator)
                and not TestConstructorSections._is_active(d, prev_header_locator)
            )
        )

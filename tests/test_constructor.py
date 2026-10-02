"""Автотесты переходов к разделам конструктора: «Булки», «Соусы», «Начинки»."""

import time

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
        self._wait_active(driver, locators.TAB_SAUCES_HEADER)

        self._open_tab(driver, locators.TAB_BUNS)
        self._wait_active(driver, locators.TAB_BUNS_HEADER)

        # Ассерт: активна вкладка «Булки»
        assert self._is_active(driver, locators.TAB_BUNS_HEADER)

    def test_switch_to_sauces_section(self, driver):
        """Переход к разделу «Соусы»: активной становится вкладка «Соусы»."""
        driver.get(data.BASE_URL)
        self._open_tab(driver, locators.TAB_SAUCES)
        self._wait_active(driver, locators.TAB_SAUCES_HEADER)

        # Ассерт: активна вкладка «Соусы»
        assert self._is_active(driver, locators.TAB_SAUCES_HEADER)

    def test_switch_to_fillings_section(self, driver):
        """Переход к разделу «Начинки»: активной становится вкладка «Начинки»."""
        driver.get(data.BASE_URL)
        self._open_tab(driver, locators.TAB_FILLINGS)
        self._wait_active(driver, locators.TAB_FILLINGS_HEADER)

        # Ассерт: активна вкладка «Начинки»
        assert self._is_active(driver, locators.TAB_FILLINGS_HEADER)

    @staticmethod
    def _open_tab(driver, tab_locator):
        """Дожидается стабилизации страницы и кликает по вкладке конструктора.

        Сразу после загрузки страница ещё анимируется (могут быть наложенные
        элементы), поэтому перед кликом ждём заголовок конструктора и даём
        странице короткую паузу. Клик выполняем через JS: Selenium-клик по
        <span> вкладки может перехватываться родительским блоком (ошибка
        ElementClickInterceptedException).
        """
        WebDriverWait(driver, data.EXPLICIT_WAIT).until(
            EC.visibility_of_element_located(locators.TITLE_MAIN)
        )
        time.sleep(1)
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
    def _wait_active(driver, tab_header_locator):
        """Ожидает, пока вкладка станет активной.

        Активная вкладка в приложении определяется позицией прокрутки списка
        ингредиентов, а страница доскролливается плавно. Класс активной вкладки
        во время анимации может кратковременно появляться и исчезать, поэтому
        после первого срабатывания делаем короткую паузу и перепроверяем, что
        состояние стабильно. Если вкладка так и не стала активной — ошибка
        теста.
        """
        deadline = time.time() + data.EXPLICIT_WAIT
        while time.time() < deadline:
            try:
                WebDriverWait(driver, 1).until(
                    lambda d: TestConstructorSections._is_active(d, tab_header_locator)
                )
            except Exception:
                continue
            # Состояние поймано — убеждаемся, что оно устойчиво (не мид-скролл)
            time.sleep(0.5)
            if TestConstructorSections._is_active(driver, tab_header_locator):
                return
        raise AssertionError(
            "Вкладка не стала активной: %s" % (tab_header_locator,)
        )

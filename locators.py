"""
Описание локаторов элементов интерфейса Stellar Burgers.

Каждый локатор — кортеж (By.METHOD, 'значение'), совместимый с Selenium.
Локаторы собраны и проверены на реальном DOM сайта:
https://stellarburgers.education-services.ru

Особенности приложения, учтённые в локаторах:
- у полей ввода нет атрибута placeholder, поля различаются по name и индексу;
- поля «Имя» и «Email» в форме регистрации имеют одинаковый name='name',
  поэтому различаются индексом: [1] — Имя, [2] — Email;
- вкладки конструктора — это <div> с <span>, а не кнопки;
- кнопка выхода из аккаунта подписана «Выход»;
- текст внутри дочерних элементов ищется через contains(., ...).
"""

from selenium.webdriver.common.by import By

# ==================== ШАПКА (есть на всех страницах) ====================
# Ссылка «Конструктор» (ведёт на главную /)
LINK_CONSTRUCTOR = (By.XPATH, "//a[.//p[text()='Конструктор']]")
# Ссылка «Личный Кабинет» (ведёт на /account)
LINK_PERSONAL_CABINET = (By.XPATH, "//a[.//p[text()='Личный Кабинет']]")
# Логотип Stellar Burgers — клик возвращает на главную
LOGO_LINK = (By.XPATH, "//div[contains(@class, 'AppHeader_header__logo')]//a")

# ==================== ГЛАВНАЯ СТРАНИЦА (/) ====================
# Заголовок конструктора на главной
TITLE_MAIN = (By.XPATH, "//h1[text()='Соберите бургер']")
# Кнопка «Войти в аккаунт» — для неавторизованных пользователей
BUTTON_LOGIN_MAIN = (By.XPATH, "//button[contains(., 'Войти в аккаунт')]")
# Кнопка «Оформить заказ» — появляется у авторизованных пользователей
BUTTON_ORDER = (By.XPATH, "//button[contains(., 'Оформить заказ')]")

# ==================== СТРАНИЦА ВХОДА (/login) ====================
# Поле «Email»
INPUT_EMAIL_LOGIN = (By.XPATH, "//input[@type='text'][@name='name']")
# Поле «Пароль»
INPUT_PASSWORD_LOGIN = (By.XPATH, "//input[@type='password'][@name='Пароль']")
# Кнопка «Войти» (не путать с кнопкой «Войти в аккаунт» на главной)
BUTTON_LOGIN = (By.XPATH, "//button[contains(., 'Войти') and not(contains(., 'аккаунт'))]")
# Ссылка «Зарегистрироваться» на странице входа
LINK_REGISTER = (By.XPATH, "//a[text()='Зарегистрироваться']")
# Ссылка «Восстановить пароль» на странице входа
LINK_FORGOT_PASSWORD = (By.XPATH, "//a[text()='Восстановить пароль']")

# ==================== СТРАНИЦА РЕГИСТРАЦИИ (/register) ====================
# Поле «Имя» — первый текстовый input с name='name'
INPUT_NAME_REGISTER = (By.XPATH, "(//input[@type='text'][@name='name'])[1]")
# Поле «Email» — второй текстовый input с name='name'
INPUT_EMAIL_REGISTER = (By.XPATH, "(//input[@type='text'][@name='name'])[2]")
# Поле «Пароль»
INPUT_PASSWORD_REGISTER = (By.XPATH, "//input[@type='password'][@name='Пароль']")
# Кнопка «Зарегистрироваться»
BUTTON_REGISTER = (By.XPATH, "//button[contains(., 'Зарегистрироваться')]")
# Ссылка «Войти» в форме регистрации (возвращает на /login)
LINK_LOGIN_FROM_REGISTER = (By.XPATH, "//a[text()='Войти']")
# Ошибка валидации: пароль короче 6 символов
ERROR_INVALID_PASSWORD = (By.XPATH,
                          "//p[contains(@class, 'input__error') and text()='Некорректный пароль']")

# ==================== СТРАНИЦА ВОССТАНОВЛЕНИЯ ПАРОЛЯ (/forgot-password) ====================
# Поле «Email»
INPUT_EMAIL_RECOVERY = (By.XPATH, "//input[@type='text'][@name='name']")
# Кнопка «Восстановить»
BUTTON_RECOVER = (By.XPATH, "//button[contains(., 'Восстановить')]")
# Ссылка «Войти» в форме восстановления пароля (возвращает на /login)
LINK_LOGIN_FROM_RECOVERY = (By.XPATH, "//a[text()='Войти']")

# ==================== ЛИЧНЫЙ КАБИНЕТ (/account/profile) ====================
# Кнопка «Выход» в личном кабинете
BUTTON_LOGOUT = (By.XPATH, "//button[contains(., 'Выход')]")

# ==================== КОНСТРУКТОР: ВКЛАДКИ РАЗДЕЛОВ ====================
# Вкладка «Булки» (span внутри контейнера вкладки)
TAB_BUNS = (By.XPATH, "//span[text()='Булки']")
# Вкладка «Соусы»
TAB_SAUCES = (By.XPATH, "//span[text()='Соусы']")
# Вкладка «Начинки»
TAB_FILLINGS = (By.XPATH, "//span[text()='Начинки']")
# Контейнер вкладки — по классу проверяем, что вкладка стала активной
TAB_BUNS_HEADER = (By.XPATH, "//div[contains(@class, 'tab_tab') and .//span[text()='Булки']]")
TAB_SAUCES_HEADER = (By.XPATH, "//div[contains(@class, 'tab_tab') and .//span[text()='Соусы']]")
TAB_FILLINGS_HEADER = (By.XPATH, "//div[contains(@class, 'tab_tab') and .//span[text()='Начинки']]")
# Активная вкладка дополнительно получает этот класс
TAB_ACTIVE_CLASS = "tab_tab_type_current"

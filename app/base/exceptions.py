from app.base.common.general import FormException, StringEnum


class PlayWrightActionException(FormException):
    """Исключение PlayWrightAction."""


class PlayWrightActionMessages(StringEnum):
    """Сообщения для класса PlayWright."""

    INITIALIZE_BROWSER_ERROR: str = "Браузер не инициализирован!"
    INITIALIZE_PAGE_ERROR: str = "Страница браузера не инициализирован!"
    BROWSER_LAUNCH_ERROR: str = "Ошибка при запуске браузера: {msg}!"
    PAGE_TYPE_LOCATOR_ERROR: str = "Некорректный тип локатора страницы!"
    PAGE_LOCATOR_ERROR: str = "Ошибка при переходе на страницу браузера: {msg}!"
    PAGE_TYPE_ERROR: str = "Неверный тип страницы!"
    GET_SCREENSHOT_PAGE_ERROR: str = "Ошибка при получении скриншота страницы: {msg}!"

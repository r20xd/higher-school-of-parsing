"""Кастомные исключения для парсеров."""


class ParsingError(Exception):
    """Ошибка парсинга: элемент не найден или невалидные данные."""

    def __init__(self, message: str, url: str | None = None):
        self.url = url
        super().__init__(message)


class NetworkError(Exception):
    """Сетевая ошибка: таймаут, 5xx, недоступность."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)

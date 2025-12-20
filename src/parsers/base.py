"""Абстрактный базовый класс парсера."""

from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    """
    Базовый интерфейс парсера.
    
    Все парсеры должны наследоваться от этого класса
    и реализовывать метод parse().
    """

    @abstractmethod
    def parse(self, url: str) -> dict[str, Any]:
        """
        Парсит страницу по URL и возвращает словарь с данными.

        Args:
            url: URL страницы для парсинга.

        Returns:
            Словарь с распарсенными данными.

        Raises:
            ParsingError: Если не удалось извлечь данные.
            NetworkError: Если произошла сетевая ошибка.
        """
        pass

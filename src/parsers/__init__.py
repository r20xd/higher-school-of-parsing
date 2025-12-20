"""Модуль парсеров."""

from src.parsers.base import BaseParser
from src.parsers.browser import SeleniumParser
from src.parsers.exceptions import NetworkError, ParsingError
from src.parsers.http import HttpParser

__all__ = [
    "BaseParser",
    "HttpParser",
    "SeleniumParser",
    "ParsingError",
    "NetworkError",
]

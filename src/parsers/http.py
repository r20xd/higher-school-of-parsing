"""HTTP парсер на основе requests с поддержкой retry."""

import logging
from typing import Any

import requests
from bs4 import BeautifulSoup
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

from src.parsers.base import BaseParser
from src.parsers.exceptions import NetworkError, ParsingError

logger = logging.getLogger(__name__)


class HttpParser(BaseParser):
    """
    Парсер для статических сайтов и API.
    
    Использует requests для HTTP-запросов и BeautifulSoup для парсинга HTML.
    При сетевых ошибках автоматически делает повторные попытки (Tenacity).
    """

    def __init__(self, timeout: int = 10, max_retries: int = 3, retry_delay: int = 2):
        """
        Args:
            timeout: Таймаут HTTP-запроса в секундах.
            max_retries: Максимальное количество повторных попыток.
            retry_delay: Задержка между попытками в секундах.
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _create_retry_decorator(self):
        """Создаёт декоратор retry с текущими настройками."""
        return retry(
            stop=stop_after_attempt(self.max_retries),
            wait=wait_fixed(self.retry_delay),
            retry=retry_if_exception_type((requests.exceptions.RequestException,)),
            reraise=True,
        )

    def fetch(self, url: str) -> str:
        """
        Загружает HTML-страницу по URL с retry при ошибках.

        Args:
            url: URL страницы.

        Returns:
            HTML-код страницы.

        Raises:
            NetworkError: При сетевых ошибках после всех попыток.
        """
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def _fetch() -> str:
            logger.info(f"Fetching URL: {url}")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Successfully fetched {url}, status: {response.status_code}")
            return response.text

        try:
            return _fetch()
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            logger.error(f"HTTP error for {url}: {e}")
            raise NetworkError(f"HTTP ошибка: {e}", status_code=status_code) from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error for {url}: {e}")
            raise NetworkError(f"Сетевая ошибка: {e}") from e

    def parse(self, url: str) -> dict[str, Any]:
        """
        Парсит страницу и извлекает данные.

        Это базовая реализация, которая возвращает заголовок страницы.
        Для конкретных сайтов нужно переопределить этот метод.

        Args:
            url: URL страницы для парсинга.

        Returns:
            Словарь с данными: {"url": str, "title": str, "success": bool}.

        Raises:
            ParsingError: Если не удалось извлечь данные.
            NetworkError: При сетевых ошибках.
        """
        html = self.fetch(url)
        soup = BeautifulSoup(html, "html.parser")

        title_tag = soup.find("title")
        if title_tag is None:
            raise ParsingError("Не найден тег <title>", url=url)

        title = title_tag.get_text(strip=True)
        logger.info(f"Parsed {url}: title='{title}'")

        return {
            "url": url,
            "title": title,
            "success": True,
        }

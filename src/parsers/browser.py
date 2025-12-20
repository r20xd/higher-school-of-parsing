"""Selenium парсер для динамических сайтов."""

import logging
from typing import Any

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.parsers.base import BaseParser
from src.parsers.exceptions import NetworkError, ParsingError

logger = logging.getLogger(__name__)


class SeleniumParser(BaseParser):
    """
    Парсер для динамических сайтов с JavaScript.
    
    Использует Selenium Remote WebDriver для подключения
    к контейнеру selenium/standalone-chrome.
    """

    def __init__(
        self,
        selenium_url: str = "http://selenium:4444/wd/hub",
        timeout: int = 10,
        headless: bool = True,
    ):
        """
        Args:
            selenium_url: URL Selenium Remote WebDriver.
            timeout: Таймаут ожидания элементов в секундах.
            headless: Запускать браузер без GUI.
        """
        self.selenium_url = selenium_url
        self.timeout = timeout
        self.headless = headless
        self._driver: WebDriver | None = None

    def _create_driver(self) -> WebDriver:
        """Создаёт подключение к Remote WebDriver."""
        options = webdriver.ChromeOptions()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        logger.info(f"Connecting to Selenium at {self.selenium_url}")
        try:
            driver = webdriver.Remote(
                command_executor=self.selenium_url,
                options=options,
            )
            logger.info("Successfully connected to Selenium")
            return driver
        except WebDriverException as e:
            logger.error(f"Failed to connect to Selenium: {e}")
            raise NetworkError(f"Не удалось подключиться к Selenium: {e}") from e

    def _get_driver(self) -> WebDriver:
        """Возвращает драйвер, создаёт если не существует."""
        if self._driver is None:
            self._driver = self._create_driver()
        return self._driver

    def close(self) -> None:
        """Закрывает браузер и освобождает ресурсы."""
        if self._driver is not None:
            logger.info("Closing Selenium driver")
            self._driver.quit()
            self._driver = None

    def wait_for_element(self, by: By, value: str, timeout: int | None = None) -> Any:
        """
        Ожидает появления элемента на странице.

        Args:
            by: Тип локатора (By.CSS_SELECTOR, By.XPATH и т.д.).
            value: Значение локатора.
            timeout: Таймаут ожидания (по умолчанию self.timeout).

        Returns:
            Найденный элемент.

        Raises:
            ParsingError: Если элемент не найден за отведённое время.
        """
        driver = self._get_driver()
        wait_timeout = timeout or self.timeout

        try:
            element = WebDriverWait(driver, wait_timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException as e:
            raise ParsingError(
                f"Элемент не найден: {by}='{value}'",
                url=driver.current_url,
            ) from e

    def parse(self, url: str) -> dict[str, Any]:
        """
        Парсит динамическую страницу.

        Базовая реализация: загружает страницу и возвращает заголовок.
        Для конкретных сайтов нужно переопределить этот метод.

        Args:
            url: URL страницы для парсинга.

        Returns:
            Словарь с данными: {"url": str, "title": str, "success": bool}.

        Raises:
            ParsingError: Если не удалось извлечь данные.
            NetworkError: При проблемах с подключением к Selenium.
        """
        driver = self._get_driver()

        try:
            logger.info(f"Loading URL: {url}")
            driver.get(url)

            title = driver.title
            if not title:
                raise ParsingError("Не удалось получить заголовок страницы", url=url)

            logger.info(f"Parsed {url}: title='{title}'")

            return {
                "url": url,
                "title": title,
                "success": True,
            }

        except WebDriverException as e:
            logger.error(f"WebDriver error for {url}: {e}")
            raise NetworkError(f"Ошибка WebDriver: {e}") from e

    def __enter__(self):
        """Context manager: создаёт драйвер."""
        self._get_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager: закрывает драйвер."""
        self.close()
        return False

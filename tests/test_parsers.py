"""Тесты для модуля парсеров."""

from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

from src.parsers import HttpParser, NetworkError, ParsingError, SeleniumParser


class TestHttpParser:
    """Тесты для HttpParser."""

    def test_parse_success(self):
        """HttpParser возвращает dict при валидном HTML."""
        html = "<html><head><title>Test Page</title></head><body></body></html>"

        with patch("src.parsers.http.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = html
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            parser = HttpParser()
            result = parser.parse("https://example.com")

            assert result["url"] == "https://example.com"
            assert result["title"] == "Test Page"
            assert result["success"] is True
            mock_get.assert_called_once()

    def test_parse_no_title_raises_parsing_error(self):
        """ParsingError если нет тега title."""
        html = "<html><head></head><body></body></html>"

        with patch("src.parsers.http.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = html
            mock_response.raise_for_status = Mock()
            mock_get.return_value = mock_response

            parser = HttpParser()

            with pytest.raises(ParsingError) as exc_info:
                parser.parse("https://example.com")

            assert "title" in str(exc_info.value).lower()

    def test_retry_on_network_error(self):
        """При сетевой ошибке делается несколько попыток."""
        with patch("src.parsers.http.requests.get") as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

            parser = HttpParser(max_retries=3, retry_delay=0)

            with pytest.raises(NetworkError):
                parser.parse("https://example.com")

            assert mock_get.call_count == 3

    def test_retry_on_500_error(self):
        """При 500 ошибке делается несколько попыток."""
        with patch("src.parsers.http.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                response=mock_response
            )
            mock_get.return_value = mock_response

            parser = HttpParser(max_retries=3, retry_delay=0)

            with pytest.raises(NetworkError) as exc_info:
                parser.parse("https://example.com")

            assert exc_info.value.status_code == 500
            assert mock_get.call_count == 3


class TestSeleniumParser:
    """Тесты для SeleniumParser."""

    def test_parse_success(self):
        """SeleniumParser возвращает dict при успешной загрузке."""
        with patch("src.parsers.browser.webdriver.Remote") as mock_remote:
            mock_driver = MagicMock()
            mock_driver.title = "Selenium Test Page"
            mock_remote.return_value = mock_driver

            parser = SeleniumParser()
            result = parser.parse("https://example.com")

            assert result["url"] == "https://example.com"
            assert result["title"] == "Selenium Test Page"
            assert result["success"] is True
            mock_driver.get.assert_called_once_with("https://example.com")

    def test_parse_no_title_raises_parsing_error(self):
        """ParsingError если заголовок пустой."""
        with patch("src.parsers.browser.webdriver.Remote") as mock_remote:
            mock_driver = MagicMock()
            mock_driver.title = ""
            mock_remote.return_value = mock_driver

            parser = SeleniumParser()

            with pytest.raises(ParsingError):
                parser.parse("https://example.com")

    def test_context_manager_closes_driver(self):
        """Context manager закрывает драйвер."""
        with patch("src.parsers.browser.webdriver.Remote") as mock_remote:
            mock_driver = MagicMock()
            mock_driver.title = "Test"
            mock_remote.return_value = mock_driver

            with SeleniumParser() as parser:
                parser.parse("https://example.com")

            mock_driver.quit.assert_called_once()

    def test_connection_error_raises_network_error(self):
        """NetworkError при ошибке подключения к Selenium."""
        with patch("src.parsers.browser.webdriver.Remote") as mock_remote:
            from selenium.common.exceptions import WebDriverException

            mock_remote.side_effect = WebDriverException("Connection refused")

            parser = SeleniumParser()

            with pytest.raises(NetworkError):
                parser.parse("https://example.com")

import logging
from src.parsers.http import HttpParser
from src.parsers.browser import SeleniumParser

logger = logging.getLogger(__name__)

class ParserService:
    """
    Фасад (обертка) над парсерами Павла.
    Задача этого класса - выбрать правильный инструмент (Http или Selenium)
    и вернуть результат в едином формате.
    """

    def parse(self, url: str, method: str) -> dict:
        logger.info(f"SERVICE: Запрос на парсинг {url} методом {method}")

        try:
            if method == "http":
                parser = HttpParser()
                return parser.parse(url)
            
            elif method == "selenium":
                parser = SeleniumParser(selenium_url="http://selenium:4444/wd/hub")
                try:
                    return parser.parse(url)
                finally:
                    parser.close()
            
            else:
                raise ValueError(f"Неизвестный метод парсинга: {method}")

        except Exception as e:
            logger.error(f"SERVICE ERROR: Ошибка при парсинге {url}: {e}")
            raise e
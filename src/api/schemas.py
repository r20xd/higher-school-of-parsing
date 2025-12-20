from uuid import UUID
from pydantic import BaseModel, HttpUrl, Field

class ParsingRequest(BaseModel):
    """
    Схема входящего запроса.
    Pydantic автоматически проверит, что url - это действительно ссылка.
    """
    url: HttpUrl
    method: str = Field(default="http", description="Метод парсинга: http или selenium")

class ParsingResponse(BaseModel):
    """
    Схема ответа.
    Возвращаем только ID созданной задачи.
    """
    task_id: UUID
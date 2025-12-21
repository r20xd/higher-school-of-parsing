from src.db.database import Database
from src.db.models import Base, ScrapingTask
from src.db.session import get_db_session, create_session_dependency
from src.db.crud import (
    create_task,
    get_task,
    get_all_tasks,
    get_tasks_by_status,
    update_task_status,
    delete_task,
)

__all__ = [
    "Database",
    "Base",
    "ScrapingTask",
    "get_db_session",
    "create_session_dependency",
    "create_task",
    "get_task",
    "get_all_tasks",
    "get_tasks_by_status",
    "update_task_status",
    "delete_task",
]

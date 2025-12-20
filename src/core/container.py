from dependency_injector import containers, providers
from src.core.config import Settings
from src.db.database import Database
from src.repositories.task_repository import TaskRepository

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.main",
            "src.api.routes",
            "src.worker.tasks"
        ]
    )

    settings = Settings()

    # база данных
    db = providers.Singleton(
        Database, 
        db_url=settings.POSTGRES_DSN.unicode_string()
    )
    
    # Провайдер для engine (нужен для создания таблиц в main.py)
    db_engine = providers.Resource(
        lambda db: db.engine,
        db=db
    )

    # Провайдер для создания сессий
    session_factory = providers.Resource(
        lambda db: db.session_factory,
        db=db
    )

    task_repository = providers.Factory(
        TaskRepository,
        session_factory=session_factory,
    )
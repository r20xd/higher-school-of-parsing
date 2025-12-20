from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import Settings

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.main"])

    config = providers.Singleton(Settings)

    db_engine = providers.Singleton(
        create_engine,
        url=config.provided.POSTGRES_DSN.unicode_string(),
        echo=True,  # показывает sql запросы в терминале
    )

    session_factory = providers.Singleton(
        sessionmaker,
        bind=db_engine,
        autocommit=False, # ручное управление
        autoflush=False,
    )
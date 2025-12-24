import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from dependency_injector import providers

from src.main import app
from src.db.models import Base
from src.repositories.task_repository import TaskRepository

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool 
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Создает таблицы перед тестом и удаляет после.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def repository(db_session):
    """
    Фикстура репозитория для юнит-тестов (test_repository.py).
    Использует ту же сессию, что и db_session.
    """

    return TaskRepository(session_factory=lambda: db_session)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Клиент для тестов API.
    Подменяет провайдер task_repository, чтобы API использовало тестовую базу.
    """

    test_repo_provider = providers.Factory(
        TaskRepository,
        session_factory=TestingSessionLocal
    )

    with app.container.task_repository.override(test_repo_provider):
        with TestClient(app) as c:
            yield c
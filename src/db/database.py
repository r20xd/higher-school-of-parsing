from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Database:
    """
    Класс, отвечающий за подключение к PostgreSQL.
    """
    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=False)

        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    @property
    def engine(self):
        return self._engine

    @property
    def session_factory(self):
        return self._session_factory
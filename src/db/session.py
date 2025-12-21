from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session


@contextmanager
def get_db_session(session_factory) -> Generator[Session, None, None]:
    session: Session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_session_dependency(session_factory):
    def get_db() -> Generator[Session, None, None]:
        session = session_factory()
        try:
            yield session
        finally:
            session.close()
    
    return get_db

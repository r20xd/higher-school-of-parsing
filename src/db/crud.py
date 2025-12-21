from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from src.db.models import ScrapingTask


def create_task(session: Session, url: str) -> ScrapingTask:
    task = ScrapingTask(url=url)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: str) -> Optional[ScrapingTask]:
    return session.query(ScrapingTask).filter(ScrapingTask.id == task_id).first()


def get_all_tasks(
    session: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[ScrapingTask]:
    return session.query(ScrapingTask).offset(skip).limit(limit).all()


def get_tasks_by_status(session: Session, status: str) -> List[ScrapingTask]:
    return session.query(ScrapingTask).filter(ScrapingTask.status == status).all()


def update_task_status(
    session: Session,
    task_id: str,
    status: str,
    result: Optional[dict] = None,
    error_message: Optional[str] = None
) -> Optional[ScrapingTask]:
    task = get_task(session, task_id)
    if task:
        task.status = status
        if result is not None:
            task.result = result
        if error_message is not None:
            task.error_message = error_message
        if status in ("done", "error"):
            task.completed_at = datetime.utcnow()
        session.commit()
        session.refresh(task)
    return task


def delete_task(session: Session, task_id: str) -> bool:
    task = get_task(session, task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False

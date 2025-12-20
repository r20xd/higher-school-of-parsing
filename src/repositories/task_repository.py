from sqlalchemy.orm import Session
from src.db.models import ScrapingTask

class TaskRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, url: str) -> ScrapingTask:
        try:
            with self.session_factory() as session:
                task = ScrapingTask(url=url)
                session.add(task)
                session.commit()
                session.refresh(task)
                return task
        except Exception as e:
            raise e

    def update_status(self, task_id: str, status: str, result: dict = None):
        with self.session_factory() as session:
            task = session.query(ScrapingTask).filter(ScrapingTask.id == task_id).first()
            if task:
                task.status = status
                if result:
                    task.result = result
                session.commit()
    
    def get_by_id(self, task_id: str) -> ScrapingTask:
        with self.session_factory() as session:
            return session.query(ScrapingTask).filter(ScrapingTask.id == task_id).first()
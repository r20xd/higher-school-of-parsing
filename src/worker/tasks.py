import time
from celery import Celery
from src.core.config import Settings
from src.core.container import Container
from src.services.parser import ParserService

settings = Settings()

celery_app = Celery(
    "worker",
    broker=str(settings.REDIS_URL),
    backend=str(settings.REDIS_URL)
)

container = Container()

@celery_app.task(bind=True) 
def parse_url_task(
    self, 
    url: str, 
    method: str,
):
    task_repository = container.task_repository()

    task_id = self.request.id

    try:
        task_repository.update_status(task_id, "processing")
        
        parser = ParserService()
        result_data = parser.parse(url, method)

        task_repository.update_status(task_id, "done", result=result_data)
        
        return result_data

    except Exception as e:
        task_repository.update_status(task_id, "error", result={"error": str(e)})
        raise e
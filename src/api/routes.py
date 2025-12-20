import traceback
from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide
from src.core.container import Container
from src.api.schemas import ParsingRequest, ParsingResponse
from src.repositories.task_repository import TaskRepository
from uuid import UUID

router = APIRouter()

@router.post("/parse", response_model=ParsingResponse)
@inject
def parse_url(
    request: ParsingRequest,
    task_repository: TaskRepository = Depends(Provide[Container.task_repository]),
):
    try:
        url_str = str(request.url)

        from src.worker.tasks import parse_url_task


        task = task_repository.add(url_str)

        parse_url_task.apply_async(
            args=[url_str, request.method],
            task_id=str(task.id)
        )
        
        return ParsingResponse(task_id=task.id)
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed at step ???: {e}")

@router.get("/tasks/{task_id}", response_model=dict)
@inject
def get_task_status(
    task_id: UUID,
    task_repository: TaskRepository = Depends(Provide[Container.task_repository]),
):
    task = task_repository.get_by_id(str(task_id))
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    return {
        "id": task.id,
        "status": task.status,
        "result": task.result,
        "created_at": task.created_at
    }
import pytest
from unittest.mock import MagicMock, patch
from src.worker.tasks import parse_url_task

def test_celery_task_success():
    """
    Проверяем успешный сценарий:
    pending -> processing -> (парсинг) -> done
    """
    url = "http://test-celery.com"
    method = "http"
    task_id = "test-task-id"

    mock_repo = MagicMock()
    mock_parser_service = MagicMock()
    mock_parser_service.parse.return_value = {"title": "Test Page"}

    with patch("src.worker.tasks.container") as mock_container, \
         patch("src.worker.tasks.ParserService", return_value=mock_parser_service):

        mock_container.task_repository.return_value = mock_repo

        parse_url_task.apply(args=[url, method], task_id=task_id)

        mock_parser_service.parse.assert_called_once_with(url, method)
        mock_repo.update_status.assert_any_call(task_id, "processing")
        mock_repo.update_status.assert_called_with(task_id, "done", result={"title": "Test Page"})

def test_celery_task_failure():
    """
    Проверяем сценарий ошибки
    """
    task_id = "fail-id"

    mock_repo = MagicMock()
    mock_parser_service = MagicMock()
    mock_parser_service.parse.side_effect = Exception("Parsing Failed!")

    with patch("src.worker.tasks.container") as mock_container, \
         patch("src.worker.tasks.ParserService", return_value=mock_parser_service):
        
        mock_container.task_repository.return_value = mock_repo

        with pytest.raises(Exception, match="Parsing Failed!"):
            parse_url_task.apply(
                args=["http://bad-url.com", "http"], 
                task_id=task_id, 
                throw=True
            )

        mock_repo.update_status.assert_called_with(
            task_id, 
            "error", 
            result={"error": "Parsing Failed!"}
        )
from unittest.mock import patch

def test_create_parse_task(client):
    payload = {
        "url": "https://python.org",
        "method": "http"
    }

    # MOCK: Подменяем вызов Celery, чтобы не нужен был Redis
    with patch("src.worker.tasks.parse_url_task.apply_async") as mock_celery:
        mock_celery.return_value = None  # Celery ничего не возвращает в синхронном режиме

        response = client.post("/parse", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert "task_id" in data

        mock_celery.assert_called_once()
        call_args = mock_celery.call_args[1]
        assert call_args['args'] == ["https://python.org/", "http"]

def test_get_task_status_404(client):
    fake_id = "12345678-1234-5678-1234-567812345678"
    response = client.get(f"/tasks/{fake_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Задача не найдена"

def test_get_task_status_success(client, db_session):
    from src.db.models import ScrapingTask
    import uuid

    task_id = str(uuid.uuid4())
    new_task = ScrapingTask(
        id=task_id, 
        url="http://manual-test.com", 
        status="done", 
        result={"data": "ok"}
    )
    db_session.add(new_task)
    db_session.commit()

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["status"] == "done"
    assert data["result"] == {"data": "ok"}
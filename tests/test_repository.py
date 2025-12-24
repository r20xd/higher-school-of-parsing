from src.db.models import ScrapingTask


def test_add_task(repository, db_session):
    """
    Добавление задачи
    """
    url = "http://test.com"
    task = repository.add(url)

    assert task.id is not None
    assert task.url == url
    assert task.status == "pending"

    in_db = db_session.query(ScrapingTask).filter_by(id=task.id).first()
    assert in_db is not None

def test_get_by_id(repository):
    """
    Получение задачи по id
    """
    task = repository.add("http://google.com")
    found = repository.get_by_id(task.id)
    
    assert found is not None
    assert found.url == "http://google.com"
    assert found.id == task.id

def test_update_status(repository):
    """
    Обновление статуса задачи
    """
    task = repository.add("http://example.com")
    repository.update_status(task.id, "done", result={"foo": "bar"})
    
    updated_task = repository.get_by_id(task.id)
    assert updated_task.status == "done"
    assert updated_task.result == {"foo": "bar"}
    assert updated_task.completed_at is not None
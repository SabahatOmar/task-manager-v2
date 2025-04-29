import pytest
from app.services.task_service import TaskService
from app.services.user_service import UserService

task_service = TaskService()

@pytest.fixture
def task_data():
    return {
        "title": "Test Task",
        "description": "Some description",
        "priority": "low",
        "user_id": 1,
        "deadline": "2025-12-31"
    }

def test_valid_task_creation(app, task_data):
    with app.app_context():
        response ,status = task_service.create_task(task_data)
        assert status == 200
        assert response['message'] == "Task created successfully"


def test_invalid_task_creation(app, task_data):
    with app.app_context():
        task_data.pop('title')
        response, status = task_service.create_task(task_data)
        assert status == 400
        assert 'title' in response["error"]

def test_get_task_user(app, task_data):
    with app.app_context():
        response ,status = task_service.create_task(task_data)
        tasks = task_service.get_task_by_user(1)
        assert len(tasks) > 0
       # assert tasks['user_id'] == 1
        assert isinstance(tasks, list)

def test_delete_existing_task(app, task_data):
    with app.app_context():
        response ,status = task_service.create_task(task_data)
        success = task_service.delete_task(1)
        assert success is True

def test_delete_nonexisting_task(app, task_data):
    with app.app_context():
        success = task_service.delete_task(000)
        assert success is False

def test_serialize_task(app, task_data):
    with app.app_context():
        task_service.create_task(task_data)
        tasks = task_service.get_task_by_user(task_data["user_id"])
        task = tasks[0]
        serialized = task_service.serialize_task(task)
        assert serialized["title"] == task_data["title"]
        assert "id" in serialized
        assert serialized["user_id"] == task_data["user_id"]



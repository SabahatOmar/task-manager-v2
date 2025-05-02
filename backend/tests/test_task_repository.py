import pytest
from backend.app import create_app, db
from backend.app.models.task_model import Task
from backend.app.repositories.task_repository import TaskRepository
from backend.app.repositories.task_repository_interface import TaskRepositoryInterface

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def task_repository(app):
    return TaskRepository()

@pytest.fixture
def new_task():
    return Task(title = "Test Task" , description = 'Test Description', user_id = 1)

def test_create_task(task_repository, new_task):
    task = task_repository.create(new_task)
    assert task is True
    assert new_task.id is not None

def test_get_task_by_user_id(task_repository, new_task):
    task = task_repository.create(new_task)
    tasks = task_repository.get_by_user(new_task.user_id)
    assert len(tasks) > 0
    assert new_task.user_id == tasks[0].user_id

def test_delete_task(task_repository, new_task):
    """Test deleting a task."""
    task_repository.create(new_task)
    task = task_repository.get_by_id_for_user(new_task.id,1)
    task_repository.delete(task)

    deleted_task = task_repository.get_by_id_for_user(new_task.id,1)
    assert deleted_task is None  # Ensure the task was deleted

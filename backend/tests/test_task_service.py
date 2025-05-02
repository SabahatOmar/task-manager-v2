from datetime import datetime

import pytest
from backend.app.services.task_service import TaskService
from backend.app.services.user_service import UserService
from backend.app.models.tag_model import Tag
from backend.app.models.task_model import Task
from backend.app import db
from backend.app.repositories.task_repository import TaskRepository

task_repo = TaskRepository()
task_service = TaskService()

@pytest.fixture
def sample_tags(app):
    with app.app_context():
        tag1 = Tag(name='urgent')
        tag2 = Tag(name='home')
        db.session.add_all([tag1, tag2])
        db.session.commit()
        return Tag.query.all()  # re-fetch so they’re bound to current session

@pytest.fixture
def test_user(app):
    with app.app_context():
        user_data = {"username": "testuser", "password": "testpass"}
        UserService.register_user(user_data)
        user = UserService.get_user_by_name("testuser")
        return user

@pytest.fixture
def task_data(test_user):
    return {
        "title": "Test Task",
        "description": "Some description",
        "priority": "low",
        "user_id": 1
        #"deadline": "2025-12-31"
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
        success = task_service.delete_task(1,1)
        assert success is True

def test_delete_nonexisting_task(app, task_data):
    with app.app_context():
        success = task_service.delete_task(000,1)
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

def test_task_belongs_to_user(app,task_data):
    with app.app_context():
        response, status = task_service.create_task(task_data)
        task = task_service.get_task_by_user(task_data["user_id"])
        assert task[0].users.username == 'testuser'

def test_task_user_backref(app, task_data, test_user):
    with app.app_context():
        response, status = task_service.create_task(task_data)
        user, code = UserService.get_user_by_id(1)
        assert len(user.tasks) == 1

        assert user.tasks[0].title == "Test Task"

        #assert user.tasks[0].get("title") == "Test Task"

def test_delete_user(app, test_user, task_data):
    with app.app_context():
        response, status = task_service.create_task(task_data)
        assert len(task_service.get_task_by_user(1)) == 1

        UserService.delete_user(1)
        assert task_service.get_task_by_user(1) == []
        assert len(task_service.get_task_by_user(1)) == 0

def test_assign_tags_to_task(app, task_data, sample_tags):
    with app.app_context():
        # Create a new task
        task = Task(**task_data)
        task.tags.extend(sample_tags)  # correct: call extend()
        #db.session.add(task)
        #db.session.commit()
        task_repo.create(task)

        # Fetch the task again
        tasknew = task_repo.get_by_user(1)[0]
        assert len(tasknew.tags) == 2
        assert any(tag.name == "urgent" for tag in tasknew.tags)

def test_tag_has_tasks(app, task_data, sample_tags):
    with app.app_context():
        # Create a new task
        task = Task(**task_data)
        task.tags.extend(sample_tags)  # correct: call extend()
        task_repo.create(task)

        tag = Tag.query.filter_by(name = 'urgent').first()
        assert tag.tasks[0].title == task.title
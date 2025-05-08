# task_service.py
from datetime import datetime
from typing import List, Optional
from backend.app.services.user_service import UserService
from backend.app.models.task_model import Task
from backend.app.repositories.task_repository import TaskRepository
from backend.app.schemas.task_schema import TaskSchema
from flask_mail import Message
from backend.app.extensions import mail, task_queue
#from flask import current_app

use_service = UserService()
task_repo = TaskRepository()
task_schema = TaskSchema()


class TaskService:

    def send_deadline_email(self, recipient_email, task_title, deadline):
        from backend.app import create_app

        app = create_app()
        with app.app_context():

            msg = Message(f"Reminder: {task_title} is due",
                          recipients=[recipient_email])
            msg.body = f"Don't forget! Your task '{task_title}' is due on {deadline}."
            mail.send(msg)

    # def __init__(self, task_repo: TaskRepository):
       # self.task_repo = task_repo

    def get_task_by_user(self, user_id: int) -> Optional[Task]:
        """Fetch a task by its ID"""
        tasks = task_repo.get_by_user(user_id)
        print(tasks)
        if tasks:
            return tasks
        else:
            return []

    def create_task(self, data):
        """Create a new task"""
        errors = task_schema.validate(data)
        if errors:
            return {"error": errors}, 400
        task_data = {
            'title': data['title'],
            'user_id': data['user_id'],
            'description': data.get('description'),  # Will be None if not provided
            'priority': data.get('priority'),
            'deadline': datetime.strptime(data['deadline'], '%Y-%m-%d').date() if data.get('deadline') else None
        }
        new_task = Task(**task_data)
        user, status = use_service.get_user_by_id(int(task_data["user_id"]))
        task_queue.enqueue(self.send_deadline_email, user.email, task_data["title"], task_data["deadline"])

        done = task_repo.create(new_task)
        if done:
            return {"message":"Task created successfully"}, 200
        else:
            return {"message": "Task not created"}, 400

    def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete a task by ID"""
        task = task_repo.get_by_id_for_user(task_id, user_id)
        if task:
            return task_repo.delete(task)
        return False

    def serialize_task(self, task):
        return {
            key: value
            for key, value in {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "deadline": task.deadline.isoformat() if task.deadline else None,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                "user_id": task.user_id
            }.items() if value is not None}

    def update_task(self, task_id, user_id, update_data):
        # Fetch the task first (via repository)
        task = task_repo.get_by_id_for_user(task_id, user_id)
        if not task:
            return None  # Task not found or unauthorized

        # Delegate field updates to repository
        updated_task = task_repo.update_fields(task, update_data)
        return updated_task

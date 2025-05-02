# task_repository.py

from app.models.task_model import Task
from typing import List, Optional
from app.extensions import db
from app.repositories.task_repository_interface import TaskRepositoryInterface

class TaskRepository(TaskRepositoryInterface):
    def get_all(self) -> List[Task]:
        """Fetch all tasks from the database"""
        return Task.query.all()

    def get_by_user(self, user_id):
        return Task.query.filter_by(user_id=user_id).all()

    def get_by_id_for_user(self, task_id: int, user_id: int) -> Optional[Task]:
        print (task_id, user_id)
        return Task.query.filter_by(id=task_id, user_id=user_id).first()

    def create(self, task: Task) -> Task:
        """Create a new task in the database"""
        db.session.add(task)
        db.session.commit()
        return True

    def update(self, task: Task) -> Task:
        """Update an existing task in the database"""
        db.session.commit()
        return True

    def delete(self, task: Task) -> bool:
        """Delete a task from the database"""
        db.session.delete(task)
        db.session.commit()
        return True

    def update_fields(self, task, update_data):
        for field, value in update_data.items():
            if hasattr(task, field):
                setattr(task, field, value)
        db.session.commit()
        return task

# task_repository.py
from abc import ABC, abstractmethod
from app.models.task_model import Task
from typing import List, Optional

class TaskRepositoryInterface(ABC):

    @abstractmethod
    def get_all(self) -> List[Task]:
        """Fetch all tasks from the database"""
        pass

    @abstractmethod
    def get_by_user(self, user_id):
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Fetch a task by its ID"""
        pass

    @abstractmethod
    def create(self, task: Task) -> Task:
        """Create a new task in the database"""
        pass

    @abstractmethod
    def update(self, task: Task) -> Task:
        """Update an existing task in the database"""
        pass

    @abstractmethod
    def delete(self, task: Task) -> bool:
        """Delete a task from the database"""
        pass
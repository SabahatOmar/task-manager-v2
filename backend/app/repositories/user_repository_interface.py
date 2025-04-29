# app/repositories/user_repository_interface.py

from abc import ABC, abstractmethod
from typing import Optional
from app.models.user_model import User

class UserRepositoryInterface(ABC):

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a user by their ID"""
        pass

    @abstractmethod
    def get_by_username(self, email: str) -> Optional[User]:
        """Fetch a user by their email"""
        pass

    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user"""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user"""
        pass

    @abstractmethod
    def delete(self, user: User) -> bool:
        """Delete a user"""
        pass

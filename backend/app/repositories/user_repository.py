# user_repository.py

from app.models.user_model import User
from typing import Optional
from app.extensions import db
from app.repositories.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a user by their ID"""
        return User.query.get(user_id)

    def get_by_username(self, email: str) -> Optional[User]:
        """Fetch a user by their email"""
        return User.query.filter_by(username=email).first()

    def create(self, user: User) -> User:
        """Create a new user in the database"""
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user: User) -> User:
        """Update an existing user in the database"""
        db.session.commit()
        return user

    def delete(self, user: User) -> bool:
        """Delete a user from the database"""
        db.session.delete(user)
        db.session.commit()
        return True

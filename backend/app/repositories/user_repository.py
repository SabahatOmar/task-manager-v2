# user_repository.py

from backend.app.models.user_model import User
from typing import Optional
from backend.app.extensions import db
from backend.app.repositories.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Fetch a user by their ID"""
        return User.query.get(user_id)

    def get_by_username(self, email: str) -> Optional[User]:
        """Fetch a user by their email"""
        return User.query.filter_by(username=email).first()
        #return User.query.filter_by(username=email)

    def create(self, user: User) -> User:
        """Create a new user in the database"""
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user: User) -> User:
        """Update an existing user in the database"""
        db.session.commit()
        return user

    def delete(self, user_id: int) -> bool:
        """Delete a user from the database"""
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return True

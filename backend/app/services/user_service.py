#user_service.py
from backend.app.repositories.user_repository import UserRepository
from backend.app.models.user_model import User
from backend.app.schemas.user_schema import UserSchema
from flask_jwt_extended import create_access_token, create_refresh_token

user_schema = UserSchema()
user_repo = UserRepository()
class UserService:
    @staticmethod
    def register_user(data):
        # Validate input
        errors = user_schema.validate(data)
        if errors:
            return {"error": errors}, 400
        # Check if user already exists
        if user_repo.get_by_username(data['username']):
            return {"error": "Username already exists"}, 400
        # Create new user and set password using model method
        new_user = User(username=data['username'])
        new_user.set_password(data['password'])
        new_user.email = data['email']
        user_repo.create(new_user)
        return {"message": "User registered successfully"}, 201

    @staticmethod
    def login_user(data):
        # Validate input
        #errors = user_schema.validate(data, partial=("username", "password"))
        #if errors:
            #return {"error": errors}, 400
        user = user_repo.get_by_username(data['username'])

        # Check password using model method
        if not user or not user.check_password(data['password']):
            return {"error": "Invalid username or password"}, 400
        token = create_access_token(identity=str(user.id))  # Use flask_jwt_extended
        refresh_token = create_refresh_token(identity=str(user.id))
        return {"token": token, "refresh_token": refresh_token, "user_id": user.id}, 200

    @staticmethod
    def get_user_by_id(user_id):
        user = user_repo.get_by_id(user_id)
        if not user:
            return {"error": "User not found"}, 404
        #return user_schema.dump(user), 200
        return user, 200

    @staticmethod
    def get_user_by_name(username):
        user = user_repo.get_by_username(username)
        if not user:
            return None
        else:
            return user

    @staticmethod
    def delete_user(user_id):
        success = user_repo.delete(user_id)
        if success:
            return True
        else:
            return False

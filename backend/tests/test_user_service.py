import pytest
from backend.app.services.user_service import UserService

from backend.app.models.user_model import User
from backend.app import db

@pytest.fixture
def valid_user_data():
    return {'username':'testuser', 'password': 'testpassword'}

def test_register_user_success(app, valid_user_data):
    with app.app_context():
        response, status = UserService.register_user(valid_user_data)
        assert status == 201
        assert response["message"] == "User registered successfully"

def test_register_user_duplicate(app, valid_user_data):
    with app.app_context():
        response, status = UserService.register_user(valid_user_data)
        response, status = UserService.register_user(valid_user_data)
        assert status == 400
        assert "Username already exists" in response["error"]

def test_login_invalid_username(app):
    with app.app_context():
        data = {'username': 'nonexistent', 'password':'nonexistent'}
        response, status = UserService.login_user(data)
        assert status == 400
        assert "Invalid username or password" in response["error"]

def test_login_invalid_password(app, valid_user_data):
    with app.app_context():
        response, status = UserService.register_user(valid_user_data)
        data = {'username': 'testuser', 'password':'nonexistent'}
        response, status = UserService.login_user(data)
        assert status == 400
        assert "Invalid username or password" in response["error"]


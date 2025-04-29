# api/routes.py

from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.services.task_service import TaskService

from flask_jwt_extended import jwt_required, get_jwt_identity

api_bp = Blueprint("api", __name__)

# Register individual blueprints inside this

auth_blueprint = Blueprint("auth", __name__)
task_blueprint = Blueprint("tasks", __name__)

# Initialize services
user_service=UserService()
task_service=TaskService()

# Route to register a user
@auth_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data["username"] or not data["password"]:
        return jsonify({"error": "Email and password are required"}), 401
    response, status_code = user_service.register_user(data)
    if status_code == 201:
        return jsonify({"message": "User registered successfully"}), 201
    if status_code == 400:
        return jsonify({"message": "Username already exists"}), 400

# Route to login a user
@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    message, status_code= user_service.login_user(data)
    if status_code==400:
        return jsonify(message), 400
    elif status_code==200:
        return jsonify(message), 200

# Protected route to get all tasks
@task_blueprint.route('/tasks/<int:user_id>', methods=['GET'])

#@task_blueprint.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks(user_id):
    current_user_id = int(get_jwt_identity())
    tasks = task_service.get_task_by_user(current_user_id)  # You might need to filter tasks per user
    serialized_tasks = [task_service.serialize_task(task) for task in tasks]
    return jsonify(serialized_tasks), 200

# Protected route to create a new task
@task_blueprint.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = current_user_id
    message, status_code = task_service.create_task(data)
    if status_code == 200:
        return jsonify(message) , 200
    else:
        return jsonify(message), 400

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()

def delete_task(task_id):
    success =task_service.delete_task(task_id)
    if success:
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not deleted'}), 400

api_bp.register_blueprint(auth_blueprint, url_prefix="/auth")
api_bp.register_blueprint(task_blueprint, url_prefix="")


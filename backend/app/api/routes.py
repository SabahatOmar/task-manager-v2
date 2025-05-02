# api/routes.py

from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.services.task_service import TaskService
from app.services.tag_service import TagService

from flask_jwt_extended import jwt_required, get_jwt_identity

api_bp = Blueprint("api", __name__)

# Register individual blueprints inside this

auth_blueprint = Blueprint("auth", __name__)
task_blueprint = Blueprint("tasks", __name__)
tag_blueprint = Blueprint('tags', __name__)


# Initialize services
user_service=UserService()
task_service=TaskService()
tag_service = TagService()

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
@task_blueprint.route('/tasks', methods=['GET'])

#@task_blueprint.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
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
    current_user_id = get_jwt_identity()
    success =task_service.delete_task(task_id,current_user_id)
    if success:
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not deleted'}), 400

@api_bp.route('/deleteuser/<int:user_id>', methods=['DELETE'])
@jwt_required()

def delete_user(user_id):
    success =user_service.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not deleted'}), 400

@api_bp.route('/tags', methods=['POST'])
@jwt_required()
def create_tag():
    data = request.get_json()
    tag_name = data.get('name')
    if not tag_name:
        return jsonify({"error": "Tag name is required"}), 400
    success = tag_service.create_tag(data)
    if success:
        return jsonify({"message": "Tag created"}), 201
    return jsonify({"error": "Tag already exists"}), 400

@api_bp.route('/tags/<int:task_id>', methods=['GET'])
@jwt_required()
def get_tags(task_id):
    current_user_id = int(get_jwt_identity())
    print(current_user_id ," this is the id", task_id)
    tags = tag_service.get_all_tags(task_id, current_user_id)
    print ("this is tags" , tags)
    if tags:
        tag_names = [tag.name for tag in tags]
        return jsonify({"tags": tag_names}), 200
    return jsonify({"error" :"tags cannot be fetched"}), 400

@api_bp.route('/tags/<int:task_id>', methods=['POST'])
@jwt_required()
def add_tag_to_task(task_id):
    data = request.get_json()
    current_user_id = int(get_jwt_identity())
    success = tag_service.set_tag_by_name(data, task_id, current_user_id)
    if success:
        return jsonify({"message": "Tag added"}), 201
    return jsonify({"error": "Tag couldn't be set"}), 400

@api_bp.route('/tags/<int:task_id>', methods=['DELETE'])
@jwt_required()
def remove_tag_from_task(task_id):
    data = request.get_json()
    current_user_id = int(get_jwt_identity())
    success = tag_service.remove_tag(task_id, data , current_user_id)
    if success:
        return jsonify({"message": "Tag removed"}), 201
    return jsonify({"error": "Tag couldn't be removed"}), 400

@api_bp.route('/tags', methods=['DELETE'])
@jwt_required()
def delete_tag():
    data = request.get_json()
    success = tag_service.delete_tag(data)
    if success:
        return jsonify({"message": "Tag deleted"}), 201
    return jsonify({"error": "Tag couldn't be deleted"}), 400


api_bp.register_blueprint(tag_blueprint, url_prefix="/tags")
api_bp.register_blueprint(auth_blueprint, url_prefix="/auth")
api_bp.register_blueprint(task_blueprint, url_prefix="")


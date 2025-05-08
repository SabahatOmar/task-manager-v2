from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from backend.app.services.user_service import UserService
from backend.app.services.task_service import TaskService
from backend.app.services.tag_service import TagService
from flask_restx import fields
from backend.app.extensions import redis_client
import json


auth_ns = Namespace('auth', description='Authentication operations')
tasks_ns = Namespace('tasks', description='Task operations')
tags_ns = Namespace('tags', description='Tag operations')
user_service=UserService()
task_service=TaskService()
tag_service = TagService()

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

register_model = auth_ns.model('Register', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password'),
    'email': fields.String(required=True, description='The email')

})

# Create namespaces

# Authentication routes
@auth_ns.route('/register')
class RegisterResource(Resource):
    @auth_ns.expect(register_model)

    def post(self):
        print("after docking")
        data = request.get_json()
        if not data.get('username') or not data.get('password'):
            return {'error': 'Username and password are required'}, 400
        response, status_code = user_service.register_user(data)
        return response, status_code

@auth_ns.route('/login')
class LoginResource(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        response, status_code = user_service.login_user(data)
        return response, status_code

@auth_ns.route('/refresh')
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = int(get_jwt_identity())
        new_access_token = create_access_token(identity = current_user_id)
        return {'token':new_access_token}, 200

@auth_ns.route('/delete/<int:user_id>')
class DeleteUserResource(Resource):
    @jwt_required()
    def delete(self, user_id):
        success = user_service.delete_user(user_id)
        if success:
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User not deleted'}, 400

# Task routes
@tasks_ns.route('/')
class TaskListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = int(get_jwt_identity())
        cache_key = f"user:{current_user_id}:tasks"
        cached_tasks = redis_client.get(cache_key)
        print (cached_tasks)

        if cached_tasks is not None:
            print("Serving from cache")
            serialized_tasks = json.loads(cached_tasks)
        else:
            print("Fetching from DB")
            tasks = task_service.get_task_by_user(current_user_id)
            serialized_tasks = [task_service.serialize_task(task) for task in tasks]
            redis_client.set(cache_key, json.dumps(serialized_tasks), ex=60)  # expires in 60 seconds

        return serialized_tasks, 200

    @jwt_required()
    def post(self):
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        data['user_id'] = current_user_id
        message, status_code = task_service.create_task(data)
        return message, status_code

@tasks_ns.route('/<int:task_id>')
class TaskResource(Resource):
    @jwt_required()
    def delete(self, task_id):
        current_user_id = int(get_jwt_identity())
        success = task_service.delete_task(task_id, current_user_id)
        if success:
            return {'message': 'Task deleted successfully'}, 200
        else:
            return {'message': 'Task not deleted'}, 400

# Tag routes
@tags_ns.route('/')
class TagListResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        data['user_id'] = current_user_id
        success = tag_service.create_tag(data)
        if success:
            return {'message': 'Tag created'}, 201
        return {'error': 'Tag already exists'}, 400

    @jwt_required()
    def delete(self):
        data = request.get_json()
        success = tag_service.delete_tag(data)
        if success:
            return {'message': 'Tag deleted'}, 201
        return {'error': "Tag couldn't be deleted"}, 400

@tags_ns.route('/<int:task_id>')
class TaskTagResource(Resource):
    @jwt_required()
    def get(self, task_id):
        current_user_id = int(get_jwt_identity())
        tags = tag_service.get_all_tags(task_id, current_user_id)
        if tags:
            tag_names = [tag.name for tag in tags]
            return {'tags': tag_names}, 200
        return {'error': 'Tags cannot be fetched'}, 400

    @jwt_required()
    def post(self, task_id):
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        success = tag_service.set_tag_by_name(data, task_id, current_user_id)
        if success:
            return {'message': 'Tag added'}, 201
        return {'error': "Tag couldn't be set"}, 400

    @jwt_required()
    def delete(self, task_id):
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        success = tag_service.remove_tag(task_id, data, current_user_id)
        if success:
            return {'message': 'Tag removed'}, 201
        return {'error': "Tag couldn't be removed"}, 400

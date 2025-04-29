from flask import request, session, url_for, flash
import requests

from frontend.services.token_service import get_userid


class ApiService:
    def login_user(self, username, password):
        data = {'username': username, 'password': password}
        try:
            response= requests.post('http://127.0.0.1:5000/api/auth/login', json=data)
            print("cehcking response" , response)
            print("response code ", response.status_code)
            message = response.json()
            if message[1]== 200:
                return True, message[0]
            elif message[1] == 400:
                return False, message[0]
        except requests.exceptions.RequestException as e:
            return False, {str(e)}

    def register_user(self, username, password):
        data = {'username': username, 'password': password}
        try:
            response = requests.post('http://127.0.0.1:5000/api/auth/register', json=data)
            #response.raise_for_status()  # Raise an error for bad status codes

            if response.status_code == 201:
                return True, response.json()
            elif response.status_code == 400:  # If the username already exists
                return False, response.json()
            else:
                return False, response.json()
        except requests.exceptions.RequestException as e:
            return False, {str(e)}

    def logout(self):
        session.pop('user_id', None)
        session.pop('access_token', None)  # <— also remove the JWT!

    def get_tasks(self, headers):
        # Fetch tasks using the API
        user_id = get_userid()
        print (user_id)
        response = requests.get(f'http://127.0.0.1:5000/api/tasks/{user_id}', headers=headers)
        #response = requests.get(f'http://127.0.0.1:5000/api/tasks', headers=headers)
        print ("great" , response)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, []

    def create_task(self, data, headers):
        try:
            response = requests.post('http://127.0.0.1:5000/api/tasks', json=data, headers=headers)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json()
        except requests.exceptions.RequestException as e:
            return False, {str(e)}

    def delete_task(self, task_id, headers):
        try:
            # Attempt to delete the task
            response = requests.delete(f'http://127.0.0.1:5000/api/tasks/{task_id}', headers=headers)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json()
        except requests.exceptions.RequestException as e:
            return False, {str(e)}
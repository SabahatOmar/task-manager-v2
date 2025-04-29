from http.client import responses

from flask import Blueprint, render_template, redirect, request, url_for, flash
import requests
from datetime import datetime
from services.api_service import ApiService

#from services.api_service import login_user, register_user, create_task, get_tasks
from services.token_service import get_headers, set_session, logout_user

api_service = ApiService()
frontend_bp = Blueprint('frontend', __name__, template_folder="../templates")

@frontend_bp.route('/')
def home():
    print ("in home")
    user_id, headers = get_headers()
    print (headers,"user id", user_id)
    if not user_id or not headers:
        return redirect(url_for('frontend.login'))
    success, task_list = api_service.get_tasks(headers)
    print(task_list)
    return render_template('home.html', tasks=task_list)

@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success , response = api_service.login_user(username , password)
        response_data = response
        print(response_data)
        if success:
            set_session(response_data)
            return redirect(url_for('frontend.home'))
        flash(response_data, 'danger')
    return render_template('login.html')

@frontend_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, response = api_service.register_user(username,password)
        response_message = response
        if success:
            flash(response_message, 'success')
            return redirect(url_for('frontend.login'))
        else:  # If the username already exists
            flash(response_message, 'danger')
    return render_template('register.html')


@frontend_bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('frontend.login'))


@frontend_bp.route('/tasks', methods=['GET', 'POST'])
def tasks():
    user_id, headers = get_headers()
    if request.method == 'POST':
        # Add a new task via API
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'user_id': user_id,  # Ensure user_id is passed correctly as an integer
            'priority': request.form['priority'],  # Get priority from the form
            'deadline': request.form['deadline']  # Get deadline from the form
        }
        # Convert the deadline to the proper format
        if data['deadline']:
            try:
                data['deadline'] = datetime.strptime(data['deadline'], '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
                return redirect(url_for('frontend.tasks'))
        success, response = api_service.create_task(data,headers)
        response_message = response
        if success:
            flash(response_message, 'success')
        else:
            flash(response_message, 'danger')
        return redirect(url_for('frontend.tasks'))

    # Fetch tasks using the API
    success, response = api_service.get_tasks(headers)
    task_list = response
    if success:
        return render_template('home.html', tasks=task_list)
    else:
        flash(task_list, "danger")
        return render_template('home.html', tasks=[])

@frontend_bp.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    user_id, headers = get_headers()
    success, response = api_service.delete_task(task_id,headers)
    response_message = response
    # If delete succeeded without error
    if success:
        flash(response_message, 'success')
    else:
        flash(response_message, "danger")
    return redirect(url_for('frontend.tasks'))


import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
    #'postgresql+psycopg2://postgres:postgres@db:5432/task_manager')
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sabahatomar:newpassword@localhost/task_manager'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql+psycopg2://sabahatomar:newpassword@localhost:5432/task_manager')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # seconds
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # seconds
    JWT_TOKEN_LOCATION = ["headers"]
    #JWT_HEADER_NAME = "Authorization"
    #JWT_HEADER_TYPE = "Bearer"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sabahatomar2@gmail.com'
    MAIL_PASSWORD = 'zhhfgeefqdrjfqyn'
    MAIL_DEFAULT_SENDER = 'sabahatomar2@gmail.com'


class DevelopmentConfig(Config):
    #SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sabahatomar:newpassword@localhost/task_manager'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql+psycopg2://sabahatomar:newpassword@localhost:5432/task_manager')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sabahatomar2@gmail.com'
    MAIL_PASSWORD = 'zhhfgeefqdrjfqyn'
    MAIL_DEFAULT_SENDER = 'sabahatomar2@gmail.com'

    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
    #'postgresql+psycopg2://postgres:postgres@db:5432/task_manager')
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # <- very important for fast tests
    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF for tests if you're using Flask-WTF

import os

from flask import Flask
from .config import TestingConfig, DevelopmentConfig
from backend.app.extensions import db, jwt, migrate, redis_client
#from backend.app.api.routes import api_bp
from backend.app.api.routes import auth_ns, tasks_ns, tags_ns

from flask_restx import Api
from backend.app.extensions import mail

def create_app(config_name = 'development'):
    app = Flask(__name__)
    if config_name == 'testing':
        from backend.app.config import TestingConfig
        app.config.from_object(TestingConfig)
    elif config_name == 'development':
        from backend.app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    else:
        from backend.app.config import Config
        app.config.from_object(Config)
    app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # Initialize extensions
    redis_client.init_app(app)
    mail.init_app(app)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    api = Api(app, version='1.0', title='Task Manager Api', description='Api for managing tasks and tags')
    api.add_namespace(auth_ns, path='/auth')
    api.add_namespace(tasks_ns, path='/tasks')
    api.add_namespace(tags_ns, path='/tags')

    # Register blueprints
    #app.register_blueprint(api_bp, url_prefix='/api')

    return app
__all__ = ['create_app', 'redis_client']


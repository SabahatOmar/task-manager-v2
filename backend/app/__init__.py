from flask import Flask
from .config import TestingConfig, DevelopmentConfig
from backend.app.extensions import db, jwt, migrate
#from backend.app.api.routes import api_bp
from backend.app.api.routes import auth_ns, tasks_ns, tags_ns

from flask_restx import Api
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

    # Initialize extensions
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

from flask import Flask
from .config import TestingConfig, DevelopmentConfig
from .extensions import db, jwt, migrate
from app.api.routes import api_bp

def create_app(config_name = 'development'):
    app = Flask(__name__)
    if config_name == 'testing':
        from app.config import TestingConfig
        app.config.from_object(TestingConfig)
    elif config_name == 'development':
        from app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    else:
        from app.config import Config
        app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

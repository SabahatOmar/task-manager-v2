from flask import Flask
from flask_bcrypt import Bcrypt
from .routes.auth_routes import frontend_bp

bcrypt = Bcrypt()

def create_frontend():
    app = Flask(__name__)
    bcrypt.init_app(app)
    # Register Blueprints
    app.register_blueprint(frontend_bp, url_prefix='/')
    return app

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_mail import Mail
import redis
from rq import Queue

redis_conn = redis.from_url('redis://localhost:6379/0')  # or your Docker Redis URL
task_queue = Queue(connection=redis_conn)

mail = Mail()

redis_client = FlaskRedis()

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

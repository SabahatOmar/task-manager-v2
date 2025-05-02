from app.extensions import db
from datetime import datetime, timezone
from app.models.tag_model import task_tags

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(50))
    deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tags = db.relationship('Tag',
                           secondary = task_tags,
                           backref  = db.backref('tasks',lazy = 'dynamic'),
                           lazy = 'subquery')
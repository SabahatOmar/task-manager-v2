from backend.app.extensions import db
from backend.app.models.tag_model import Tag
from backend.app.models.task_model import Task
from backend.app.repositories.task_repository import TaskRepository

class TagRepository:
    def __init__(self):
        self.task_repo = TaskRepository()

    def get_all_tags(self, task_id , user_id  ):
        task = self.task_repo.get_by_id_for_user(task_id, user_id)
        return task.tags if task else []

    def set_tag(self, tag_name, task_id, user_id):
        task = self.task_repo.get_by_id_for_user(task_id, user_id)
        self.create_tag(tag_name)
        tag = self.get_tag_by_name(tag_name)
        if task and tag not in task.tags:
            task.tags.append(tag)
            db.session.commit()
            return True
        return False

    def get_all_tasks(self, tag_id):
        tag = Tag.query.get(tag_id)
        return tag.tasks.all() if tag else []

    def create_tag(self, tag_name):
        if self.get_tag_by_name(tag_name):
            return False  # Already exists
        new_tag = Tag(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()
        return True

    def get_tag_by_name(self, name):
        tag = Tag.query.filter_by(name = name).first()
        return tag

    def delete_tag(self, tag_name):
        tag = self.get_tag_by_name(tag_name)
        if tag:
            db.session.delete(tag)
            db.session.commit()
            return True
        return False

    def remove_tag(self, task_id, tag_name, user_id):
        task = self.task_repo.get_by_id_for_user(task_id, user_id)
        tag =  self.get_tag_by_name(tag_name)
        if task and tag in task.tags:
            task.tags.remove(tag)
            db.session.commit()
            return True
        return False



from backend.app.repositories.tag_repository import TagRepository
from backend.app.repositories.task_repository import TaskRepository

class TagService:
    def __init__(self):
        self.tag_repo = TagRepository()
        self.task_repo = TaskRepository()

    def get_all_tags(self, task_id, user_id):
        print(task_id, user_id)
        task = self.task_repo.get_by_id_for_user(task_id, user_id)
        if task is None:
            return None  # or raise TaskNotFoundError
        return task.tags

    def set_tag_by_name(self, tag_data, task_id, user_id):
        success = self.tag_repo.set_tag(tag_data["name"] , task_id , user_id)
        return success

    def remove_tag(self,task_id, tag_data, user_id):
        success = self.tag_repo.remove_tag(task_id, tag_data["name"], user_id)
        return success

    def delete_tag(self, tag_data):
        success = self.tag_repo.delete_tag(tag_data["name"])
        return success

    def create_tag(self , tag_data):
        success = self.tag_repo.create_tag(tag_data["name"])
        return success


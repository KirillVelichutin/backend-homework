from schemas import BaseTask, AddTask, UpdateTask

tasks = []

class TaskService:
    def __init__(self):
        self.tasks_mock_db = tasks
    
    def add_task(self, new_task: AddTask):
        for task in self.tasks_mock_db:
            if task.id == new_task.id:
                return {"status": "failed", "message": "task with this id already exists"}
        
        self.tasks_mock_db.append(new_task)
        return BaseTask(**new_task.model_dump())
    
    def get_all_tasks(self):
        return [BaseTask(**task.model_dump()) for task in self.tasks_mock_db]
    
    def get_task_by_id(self, task_id):
        for task in self.tasks_mock_db:
            if task.id == task_id:
                return BaseTask(**task.model_dump())

    def update_specific_task(self, task_id, task_update: UpdateTask):
        for i, task in enumerate(self.tasks_mock_db):
            if task.id == task_id:
                task.about = task_update.about
                task.done = task_update.done
                updated_task = task
                return BaseTask(**updated_task.model_dump())
        
    def delete_task_by_id(self, task_id):
        for i, task in enumerate(self.tasks_mock_db):
            if task.id == task_id:
                removed_task = self.tasks_mock_db.pop(i)
                return BaseTask(**removed_task.model_dump())
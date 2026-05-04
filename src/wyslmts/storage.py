import json
from pathlib import Path
from typing import List
from wyslmts.models import Task

class Storage:
    def __init__(self, data_path: Path = Path.home() / ".wyslmts" / "tasks.json"):
        self.data_path = data_path
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_path.exists():
            self.save_tasks([])

    def load_tasks(self) -> List[Task]:
        try:
            with open(self.data_path, "r") as f:
                data = json.load(f)
                return [Task(**task) for task in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self, tasks: List[Task]):
        temp_path = self.data_path.with_suffix(".tmp")
        try:
            with open(temp_path, "w") as f:
                json.dump([task.model_dump(mode='json') for task in tasks], f, indent=4)
            temp_path.replace(self.data_path)
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise e

    def add_task(self, task: Task):
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)

import pytest
import json
from pathlib import Path
from wyslmts.storage import Storage
from wyslmts.models import Task

@pytest.fixture
def temp_storage(tmp_path):
    db_path = tmp_path / "test_tasks.json"
    return Storage(data_path=db_path)

def test_storage_add_and_load(temp_storage):
    task = Task(title="Persistent Task")
    temp_storage.add_task(task)
    
    loaded_tasks = temp_storage.load_tasks()
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0].title == "Persistent Task"
    assert str(loaded_tasks[0].id) == str(task.id)

def test_storage_save_tasks(temp_storage):
    tasks = [Task(title="Task 1"), Task(title="Task 2")]
    temp_storage.save_tasks(tasks)
    
    loaded_tasks = temp_storage.load_tasks()
    assert len(loaded_tasks) == 2
    assert loaded_tasks[1].title == "Task 2"

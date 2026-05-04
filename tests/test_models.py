import pytest
from wyslmts.models import Task, Priority, TaskStatus

def test_task_creation():
    task = Task(title="Test Task")
    assert task.title == "Test Task"
    assert task.priority == Priority.MEDIUM
    assert task.status == TaskStatus.TODO

def test_task_mark_done():
    task = Task(title="Test Task")
    task.mark_done()
    assert task.status == TaskStatus.DONE
    assert task.updated_at >= task.created_at

from pymongo.errors import DuplicateKeyError, PyMongoError
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from models.TaskClasses import TaskManager, Task
import pytest
from unittest.mock import MagicMock, patch

#------Test TaskManager Class------#
@patch('models.TaskClasses.MongoClient')
def test_add_task(mock_mongo):
    manager = TaskManager()
    task = Task("Sleep","Go to bed by 8PM")
    manager.add_task(task)
    manager.collection.insert_one.assert_called_once_with(task.to_dict())

@patch('models.TaskClasses.MongoClient')
def test_add_task_duplicate(mock_mongo):
    manager = TaskManager()
    task = Task("Sleep","Go to bed by 8PM")
    manager.collection.insert_one.side_effect = DuplicateKeyError("duplicate")
    with pytest.raises(DuplicateKeyError):
        manager.add_task(task)

@patch('models.TaskClasses.MongoClient')
def test_add_task_failed_mongo_connection(mock_mongo):
    manager = TaskManager()
    task = Task("Sleep","Go to bed by 8PM")
    manager.collection.insert_one.side_effect = PyMongoError("connection failed")
    with pytest.raises(PyMongoError):
        manager.add_task(task)


@patch('models.TaskClasses.MongoClient')
def test_get_tasks(mock_mongo):
    manager = TaskManager()
    task = Task("Sleep","Go to bed by 8PM")
    manager.collection.find.return_value = [task.to_dict()]
    outcome = manager.get_tasks()
    assert len(outcome) == 1
    assert outcome[0].title == "Sleep"
    

@patch('models.TaskClasses.MongoClient')
def test_get_tasks_no_existing_tasks_in_db(mock_mongo):
    manager = TaskManager()
    manager.collection.find.return_value = []
    with pytest.raises(ValueError):
        manager.get_tasks()

@patch('models.TaskClasses.MongoClient')
def test_get_tasks_failed_mongo_connection(mock_mongo):
    manager = TaskManager()
    manager.collection.find.side_effect = PyMongoError("connection failed")
    with pytest.raises(PyMongoError):
        manager.get_tasks()

@patch('models.TaskClasses.MongoClient')
def test_delete_task(mock_mongo):
    manager = TaskManager()
    myTask = Task("Sleep","Go to bed by 8PM")
    manager.collection.delete_one.return_value = MagicMock(deleted_count = 1)
    manager.delete_task(myTask.id)
    manager.collection.delete_one.assert_called_once_with({"id": myTask.id})

@patch('models.TaskClasses.MongoClient')
def test_delete_task_no_existing_task_in_db(mock_mongo):
    manager = TaskManager()
    myTask = Task("Sleep", "Go to bed by 8PM")
    manager.collection.delete_one.return_value = MagicMock(deleted_count=0)
    with pytest.raises(ValueError):
        manager.delete_task(myTask.id)

@patch('models.TaskClasses.MongoClient')
def test_delete_task_failed_mongo_connection(mock_mongo):
    manager = TaskManager()
    myTask = Task("Sleep", "Go to bed by 8PM")
    manager.collection.delete_one.side_effect = PyMongoError("connection failed")
    with pytest.raises(PyMongoError):
        manager.delete_task(myTask.id)


@patch('models.TaskClasses.MongoClient')
def test_update_status(mock_mongo):
    manager = TaskManager()
    myTask = Task("Sleep","Go to bed by 8PM")
    manager.collection.update_one.return_value = MagicMock(matched_count = 1)
    manager.update_status(myTask.id, "Completed")
    manager.collection.update_one.assert_called_once_with({"id": myTask.id}, {"$set": {"status": "Completed"}})

@patch('models.TaskClasses.MongoClient')
def test_update_status_no_existing_task_in_db(mock_mongo):
    manager = TaskManager()
    myTask = Task("Sleep", "Go to bed by 8PM")
    manager.collection.update_one.return_value = MagicMock(matched_count=0)
    with pytest.raises(ValueError):
        manager.update_status(myTask.id, "Completed")


@patch('models.TaskClasses.MongoClient')
def test_update_status_failed_mongo_connection(mock_mongo):
    manager = TaskManager()
    myTask = Task("Sleep", "Go to bed by 8PM")
    manager.collection.update_one.side_effect = PyMongoError("connection failed")
    with pytest.raises(PyMongoError):
        manager.update_status(myTask.id, "Completed")


@patch('models.TaskClasses.MongoClient')
def test_update_priority(mock_mongo):
    manager = TaskManager()
    myTask = Task("Sleep", "Go to bed by 8PM")
    manager.collection.update_one.return_value = MagicMock(matched_count=1)
    manager.update_priority(myTask.id, "High")
    manager.collection.update_one.assert_called_once_with({"id": myTask.id}, {"$set": {"priority": "High"}})

@patch('models.TaskClasses.MongoClient')
def test_update_priority_no_existing_task_in_db(mock_mongo):
    manager = TaskManager()
    myTask = Task("Sleep", "Go to bed by 8PM")
    manager.collection.update_one.return_value = MagicMock(matched_count=0)
    with pytest.raises(ValueError):
        manager.update_priority(myTask.id, "High")

@patch('models.TaskClasses.MongoClient')
def test_update_priority_failed_mongo_connection(mock_mongo):
    manager = TaskManager()
    myTask = Task("Sleep", "Go to bed by 8PM")
    manager.collection.update_one.side_effect = PyMongoError("connection failed")
    with pytest.raises(PyMongoError):
        manager.update_priority(myTask.id, "High")


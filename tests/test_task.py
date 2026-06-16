import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from models.TaskClasses import Task
import pytest

#------Test Task Class------#

#Make a task  with missing optional inputs
def test_task_creation_with_defaults():
    myTask = Task("Baking","Make Cookies")
    assert myTask.title == "Baking"
    assert myTask.description == "Make Cookies"
    assert myTask.priority == "unassigned"
    assert myTask.status == "pending"
    assert isinstance(myTask.id,str)
    assert isinstance(myTask.timestamps,str)

#Make a task with optional inputs
def test_task_creation_without_defaults():
    myTask = Task("Study","Study For Exam", "High","Complete")
    assert myTask.title == "Study"
    assert myTask.description == "Study For Exam"
    assert myTask.priority == "High"
    assert myTask.status == "Complete"
    assert isinstance(myTask.id,str)
    assert isinstance(myTask.timestamps,str)


#Add a priority to a task
def test_set_priority():
    myTask = Task("Study","Study For Exam")
    assert myTask.priority == "unassigned"
    myTask.set_priority("Urgent")
    assert myTask.priority == "Urgent"


#Overwrite an existing priority
def test_set_priority2():
    myTask = Task("Sleep","Go to bed at 8PM","High")
    assert myTask.priority == "High"
    myTask.set_priority("low")
    assert myTask.priority == "low"


def test_to_dict():
    myTask = Task("Sleep","Go to bed at 8PM","High","Complete")
    result = myTask.to_dict()
    assert result["title"] == myTask.title
    assert result["description"] == myTask.description
    assert result["priority"] == myTask.priority
    assert result["status"] == myTask.status
    assert result["id"] == myTask.id
    assert result["timestamps"] == myTask.timestamps

def test_str():
    myTask = Task("Sleep","Go to bed at 8PM","High","Complete")
    resulting_string = str(myTask)
    assert f"ID: {myTask.id}" in resulting_string
    assert f"Task Name: {myTask.title}" in resulting_string
    assert f"Description: {myTask.description}" in resulting_string
    assert f"Priority: {myTask.priority}" in resulting_string
    assert f"Status: {myTask.status}" in resulting_string
    assert f"Timestamps: {myTask.timestamps}" in resulting_string

def test_from_dict():
    myTask = Task("Sleep","Go to bed at 8PM","High","Complete")
    myDict = myTask.to_dict()
    myNewTask = Task.from_dict(myDict)
    #Check if all attributes are preserved after creating a task from a dict
    assert myNewTask.title == myDict["title"]
    assert myNewTask.description == myDict["description"]
    assert myNewTask.priority == myDict["priority"]
    assert myNewTask.status == myDict["status"]
    assert myNewTask.id == myDict["id"]
    assert myNewTask.timestamps == myDict["timestamps"]



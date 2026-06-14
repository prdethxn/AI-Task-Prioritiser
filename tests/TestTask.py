import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.TaskClasses import Task,TaskManager
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










#------Test TaskManager Class------#
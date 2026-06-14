import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.AILayer import AIAnalyser
from models.TaskClasses import Task, TaskManager


def add_task(task_manager,analyser):
    while True:
        try:
            title,description = input("Enter the task title and description (seperated by a comma): ").split(",")
            newTask = Task(title.strip(),description.strip())
            analyser.prioritise_task(newTask)
            task_manager.add_task(newTask)
            print(f"The Following Task Has Been Added: {newTask} ")
            break
        except ValueError:
            print("Invalid Input(s), Try Again")


def view_tasks(task_manager,getPending = False):
    myTasks = task_manager.get_tasks(getPending)
    print(*myTasks, sep="\n----\n")


def delete(task_manager):
    try:
        id = input("Enter the task ID: ")
        task_manager.delete_task(id)
        print(f"Task With {id} Was Deleted")
    except ValueError:
        print("Invalid Input. Try again")
    
def complete_task(task_manager):
    try:
        id = input("Enter the task ID: ")
        task_manager.update_status(id,"Completed")
        print(f"Task With {id} Was Completed")

            
    except ValueError:
        print("Invalid Input. Try again")

def reprioritise_tasks(task_manager,ai_analyser):
    all_tasks = task_manager.get_tasks()
    ai_analyser.prioritise_all(all_tasks)

def summarise_tasks(task_manager,ai_analyser):
    pending_tasks = task_manager.get_tasks(True)
    ai_analyser.summarise(pending_tasks)
    

def main():
    manager = TaskManager()
    analyser = AIAnalyser()
    running = True
    options = [
        "1. Create A New Task", "2. View All Tasks", "3. View Pending Tasks", "4. Delete A Task", "5. Complete A Task",
        "6. Re-prioritise All Tasks",  "7. Summarise All Tasks", "8. Exit"
    ]
    while running:
        print("======= AI Task Prioritiser =======")
        print(*options, sep="\n")
        print("==============")

        try:
            choice = int(input("Select An Option: "))
            if choice == 1:
                add_task(manager,analyser)
            elif choice == 2:
                view_tasks(manager)
            elif choice == 3:
                view_tasks(manager,True)
            elif choice == 4:
                delete(manager)
            elif choice == 5:
                complete_task(manager)
            elif choice == 6:
                reprioritise_tasks(manager,analyser)
            elif choice == 7:
                summarise_tasks(manager, analyser)
            elif choice == 8:
                running = False
        except:
            print("Invalid Input, Try again")


if __name__ == "__main__":
    main()
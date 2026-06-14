import uuid
import os
from datetime import datetime 
from pymongo import MongoClient
from dotenv import load_dotenv
from pymongo.errors import DuplicateKeyError, PyMongoError

load_dotenv()

class Task:
    def __init__(self,title,description,priority = "null",status = "pending"):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.timestamps = datetime.now().isoformat()
        self.id = str(uuid.uuid4())


    #Turn A Task Objects Into A Dictionary, So It Can Be Stored In MongoDB.
    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "priority": self.priority, "status": self.status, "timestamps": self.timestamps}
    
    def setPriority(self,newPriority):
        self.priority = newPriority


    #Convert A Dict Into A Task Object. This Is Used To Turn Tasks Stored In MongoDB Into Task Objects.
    @classmethod
    def from_dict(cls, data):
        task = cls(title = data["title"], description = data["description"], priority = data["priority"], status = data["status"]) 
        task.timestamps = data["timestamps"]
        task.id = data["id"]
        return task
     
        
    #Return Task Objects Into A Neatly Fromatted String For the CLI.
    def __str__(self):
        return (f"ID: {self.id} \n" 
                f"Task Name: {self.title} \n"
                f"Description:  {self.description} \n" 
                f"Priority:  {self.priority} \n" 
                f"Status:  {self.status} \n" 
                f"Timestamps {self.timestamps} \n")

class TaskManager:
    def __init__(self):
        self.uri = os.getenv("MONGODB_URI")
        self.db_name = os.getenv("DB_NAME")
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        self.collection = self.db["Tasks"]

    def add_task(self,task):
        try:
            return self.collection.insert_one(task.to_dict())
        except DuplicateKeyError as dke:
            print(f"Failed to add task: task already exists. {dke}")
            raise
        except PyMongoError as pe:
            print(f"Failed to connect to database: {pe}")
            raise
        except Exception as e:
            print(f"Client-side error occured: {e}")
            raise
        
    def get_tasks(self, getPending = False): #either get all tasks, or ones that don't have a status yet.
    
        try:
            if getPending:
                outcome = [Task.from_dict(task) for task in self.collection.find({"status": "pending"})]
            else:
                outcome = [Task.from_dict(task) for task in self.collection.find({})]
            if not outcome: #If tasks aren't found in the database, throw an exception.
                raise ValueError("Error: Task cannot be found")
            return outcome
        
        except ValueError as mi:
            print(mi)
            raise
        except PyMongoError as pe:
            print(f"Failed to connect to database: {pe}")
            raise
        except Exception as e:
            print(f"Client-side error occured: {e}")
            raise

   

    def delete_task(self,id):
        try:
            result = self.collection.delete_one({"id": id})
            if result.deleted_count == 0: #check if task was actually deleted
                raise ValueError(f"No task found with ID: {id}")
            print(f"Task {id} deleted sucessfully")
            return result

        except ValueError as ve:
            print(ve)
            raise
        except PyMongoError as pe:
            print(f"Failed to connect to database: {pe}")
            raise
        except Exception as e:
            print(f"Client-side error occured: {e}")
            raise
        

    #Update the status of a task
    def update_status(self, id, newStatus):
        try:
            result = self.collection.update_one(
            {"id": id},
            {"$set": {"status": newStatus}})

            if result.matched_count == 0: #throw an error if the targeted task doesn't exist
                raise ValueError(f"Failed to update task with id: {id}")
            return result
        except ValueError as ve:
            print(ve)
            raise
        except PyMongoError as pe:
            print(f"Failed to connect to database: {pe}")
            raise
        except Exception as e:
            print(f"Client-side error occured: {e}")
            raise
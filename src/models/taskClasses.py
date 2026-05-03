import uuid #Used To Give Each Task A Custom ID.
from datetime import datetime #Used To Automatically Allocate Timestamps For Each Task 

class Task:
    def __init__(self,title,description,priority,status):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.timestamps = datetime.now().isoformat()
        self.id = str(uuid.uuid4())


    #Turn A Task Objects Into A Dictionary, So It Can Be Stored In MongoDB.
    def to_dict(self):
        return {"id": self.id, "title": self.title, "description": self.description, "priority": self.priority, "status": self.status, "timestamps": self.timestamps}


    #Convert A Dict Into A Task Object. This Is Used To Turn Tasks Stored In MongoDB Into Task Objects.
    @classmethod
    def from_dict(cls, data):
        Task = cls(title = data["title"], description = data["description"], priority = data["priority"], status = data["status"]) 
        Task.timestamps = data["timestamps"]
        Task.id = data["id"]
        return Task
     
        
    #Return Task Objects Into A Neatly Fromatted String For the CLI.
    def __str__(self):
        return (f"ID: {self.id} \n" 
                f"Task Name: {self.title} \n"
                f"Description:  {self.description} \n" 
                f"Priority:  {self.priority} \n" 
                f"Status:  {self.status} \n" 
                f"Timestamps {self.timestamps} \n")



        
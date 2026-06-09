
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import threading
from concurrent.futures import ThreadPoolExecutor
#Load vatiables from the .env file
load_dotenv()

class AIAnalyser:

    def __init__(self, model_name = "gemini-2.5-flash"):
        self.model_name = model_name
        self.client = genai.Client() #automatically gets the API key from the env file.



    def prioritiseTask(self,task): #Set the priority for a single task. Helps achieve multi-threading.
        prompt = (f"Prioritise the task based on the information (return the existing priority, only if one is present). Reply with one word only; that being the priority: {task}")
        chat = self.client.chats.create(model = self.model_name)
        response = chat.send_message(prompt)
        task.setPriority(response.text)


    #Based on tasks details, get the AI to prioritise it. 
    #Sending one message at a time is slow, so we use multi-threading to concurrently prioritise multiple tasks
    def prioritise(self,tasks):
        with ThreadPoolExecutor(max_workers = 4) as executor: #Only prioritise 4 tasks at a time to respect Gemini's API rate limiting.
             executor.map(self.prioritiseTask,tasks)
            
    
    def summarise(self,pendingTasks): #Print out a summary for pending task.
        taskInfo = "\n".join(f"- {task}" for task in pendingTasks) #Make a list contaning the info fro each task.
        prompt = (f"Provide a clear, neat summary of each task, based on the information provided: \n {taskInfo}")
        response = self.client.models.generate_content(model=self.model_name,contents=prompt)
        print(response.text)

    

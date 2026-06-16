import os
from google import genai
from google.genai.errors import APIError
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

# Load variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))


class AIAnalyser:

    def __init__(self, model_name="gemini-2.5-flash"):
        self.model_name = model_name
        try:
            self.client = genai.Client()
            self.client.models.get(model=model_name)
        except ValueError as ve:
            print(f"Configuration File Error: {ve}")
            raise
        except APIError as ae:
            print(f"API authentication/connection failed {ae}")
            raise
        except Exception as e:
            print(f"An unknown error occurred: {e}")
            raise

    def prioritise_task(self, task):
        prompt = (
            f"Prioritise the task based on the information "
            f"(return the existing priority, only if one is present). "
            f"Reply with one word only; that being the priority: {task}"
        )
        try:
            chat = self.client.chats.create(model=self.model_name)
            response = chat.send_message(prompt)
            task.set_priority(response.text)
        except APIError as ae:
            print(f"API error occurred: {ae}")
            raise
        except Exception as e:
            print(f"Client side error: {e}")
            raise

    # Use multi-threading to concurrently prioritise multiple tasks
    def prioritise_all(self, tasks):
        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(self.prioritise_task, tasks)

    def summarise(self, pendingTasks):
        try:
            taskInfo = "\n".join(f"- {task}" for task in pendingTasks)
            prompt = (
                f"Provide a clear, neat summary of each task, "
                f"based on the information provided: \n {taskInfo}"
            )
            response = self.client.models.generate_content(
                model=self.model_name, contents=prompt
            )
            print(response.text)
        except APIError as ae:
            print(f"API error occurred: {ae}")
            raise
        except Exception as e:
            print(f"Client side error: {e}")
            raise
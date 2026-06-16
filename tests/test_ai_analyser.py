import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src'))
from models.AILayer import AIAnalyser
from models.TaskClasses import Task
import pytest
from unittest.mock import MagicMock, patch

#------AIAnalyser------#
@patch('models.AILayer.genai.Client')
def test_invalid_api_key(mock_client):
    mock_client.return_value.models.get.side_effect = ValueError("Invalid API Key")
    with pytest.raises(ValueError):
        AIAnalyser()

@patch('models.AILayer.genai.Client')
def test_prioritise_task(mock_client):
    analyser = AIAnalyser()
    task = Task("Sleep", "Bed before 8PM")
    mock_chat = mock_client.return_value.chats.create.return_value
    mock_chat.send_message.return_value.text = "High"
    analyser.prioritise_task(task)
    assert task.priority == "High"


@patch('models.AILayer.genai.Client')
def test_prioritise_task_with_failed_API_connection(mock_client):
    analyser = AIAnalyser()
    task = Task("Sleep", "Bed before 8PM")
    mock_client.return_value.chats.create.side_effect = Exception("Unable To Use The API")
    with pytest.raises(Exception):
        analyser.prioritise_task(task)

@patch('models.AILayer.genai.Client')
def test_prioritise_all(mock_client):
   analyser = AIAnalyser()
   tasks = [Task("Sleep","Bed by 7PM"), Task("Study","Study for math exam")]
   mock_chat = mock_client.return_value.chats.create.return_value
   mock_chat.send_message.return_value.text = "High"
   analyser.prioritise_all(tasks)
   assert tasks[0].priority == "High"  
   assert tasks[1].priority == "High"


@patch('models.AILayer.genai.Client')
def test_summarise(mock_client):
    analyser = AIAnalyser()
    tasks = [Task("Sleep","Bed by 7PM"), Task("Study","Study for math exam")]
    mock_client.return_value.models.generate_content.return_value.text = "Summary"
    analyser.summarise(tasks)
    mock_client.return_value.models.generate_content.assert_called_once()


@patch('models.AILayer.genai.Client')
def test_summarise_failed_api_connection(mock_client):
      analyser = AIAnalyser()
      tasks = [Task("Sleep","Bed by 7PM"), Task("Study","Study for math exam")]
      mock_client.return_value.models.generate_content.side_effect = Exception("Failed to connect to API")
      with pytest.raises(Exception):
          analyser.summarise(tasks)

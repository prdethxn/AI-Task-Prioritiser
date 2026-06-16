# AI Task Prioritiser

A Python CLI application that allows users to manage tasks, store them in MongoDB, and uses the Gemini API to auto-prioritise and summarise tasks. Built using OOP principles, a CI/CD pipeline via GitHub Actions, and unit testing via pytest.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| Database | MongoDB Atlas |
| AI Layer | Google Gemini API |
| Testing | pytest |
| CI/CD | GitHub Actions |

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/prdethxn/AI-Task-Prioritiser
cd AI-Task-Prioritiser
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**
```bash
cp .env.example .env
```
Fill in `.env` with your Gemini API key, MongoDB URI, and database name.

**4. Run the app**
```bash
python3 src/CLI/main.py
```

## Usage
======= AI Task Prioritiser =======
1. Create A New Task
....

When adding a task, Gemini will automatically assign a priority based on the task description.

## Running Unit Tests & CI/CD

```bash
pytest tests/
```

28 unit tests cover the Task, TaskManager, and AIAnalyser classes with mocked API and database responses, ensuring all code is functional.
GitHub Actions installs dependencies and runs all tests on every push to main and on every pull request, ensuring only functional code reaches the main repository.

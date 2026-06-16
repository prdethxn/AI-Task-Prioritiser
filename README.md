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

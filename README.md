# 🧠 LifeCoach AI

AI-powered multi-agent life planning app using FastAPI + Streamlit + CrewAI.

## Features

- 🎯 Personalized Health, Finance, Learning, Motivation plans
- 🗂️ Save, Edit, and Delete plans
- 🤖 Chat with individual domain agents
- 📊 Uses LLMs and CrewAI to coordinate tasks
- 🔒 Local file storage (JSON-based)

## Getting Started

```bash
# Run backend
cd backend
uvicorn main:app --reload

# Run frontend
cd frontend
streamlit run app.py

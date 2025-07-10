# 🧠 LifeCoach AI — Your Personalized Life Planner, Powered by AI Agents

**LifeCoach AI** is an AI-powered personal productivity assistant that helps users plan and improve their **Health**, **Finance**, **Learning**, and **Motivation** through goal-driven, multi-agent collaboration. Built using **FastAPI**, **Streamlit**, and **CrewAI**, it simulates an AI life coach who coordinates specialized domain experts to generate actionable life plans.

---

## 🚀 Why I Built This

As someone deeply passionate about building **human-centered AI tools**, I wanted to create a smart assistant that:
- Feels personalized, not generic
- Doesn’t just *chat*, but plans, remembers, adapts
- Helps people live better across health, money, learning, and mindset

---

## 🔍 Key Features

### 🧠 Multi-Agent Life Planner (LLM-powered)
- Uses **CrewAI** to orchestrate 4 agents:
  - `HealthAgent`: suggests workouts, meals
  - `FinanceAgent`: builds budgets based on income (₹)
  - `LearningAgent`: generates learning paths
  - `MotivationAgent`: offers personalized mindset tips

### ✍️ Editable Plans
- Plans are saved as `.json` files per user
- You can load, **edit**, **delete**, and **save** them from the frontend

### 💬 Domain-specific Chat Agents
- Talk directly to the Finance, Health, Learning, or Motivation coach
- Uses keyword-aware prompting guardrails to ensure relevant responses

### 🔄 Persistent Chat History
- Stores conversations by user ID
- Chat history can be viewed and cleared anytime

### 📊 Streamlit UI
- Clean, minimal design with separate sections for planning and chatting
- Responsive inputs for customizing your plan

---

## 🛠️ Tech Stack

| Layer         | Tech                     |
|--------------|--------------------------|
| Backend       | FastAPI (REST APIs)       |
| Frontend      | Streamlit (UI)            |
| AI Agents     | CrewAI +  Ollama |
| Storage       | JSON-based file system    |
| Auth (simple) | User ID-based local state |

---


## 🧪 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/<your-username>/lifecoach-ai.git
cd lifecoach-ai

# Setup backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Setup frontend
cd ../frontend
pip install streamlit requests
streamlit run app.py

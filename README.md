#  LifeCoach AI — Your Personalized Life Planner, Powered by AI Agents

**LifeCoach AI** is an AI-powered personal productivity assistant that helps users plan and improve their **Health**, **Finance**, **Learning**, and **Motivation** through goal-driven, multi-agent collaboration. Built using **FastAPI**, **Streamlit**, and **CrewAI**, it simulates an AI life coach who coordinates specialized domain experts to generate actionable life plans.

---

##  Why I Built This

As someone deeply passionate about building **human-centered AI tools**, I wanted to create a smart assistant that:
- Feels personalized, not generic
- Doesn’t just *chat*, but plans, remembers, adapts
- Helps people live better across health, money, learning, and mindset

---

##  Key Features

###  Multi-Agent Life Planner (LLM-powered)
- Uses **CrewAI** to orchestrate 4 agents:
  - `HealthAgent`: suggests workouts, meals
  - `FinanceAgent`: builds budgets based on income (₹)
  - `LearningAgent`: generates learning paths
  - `MotivationAgent`: offers personalized mindset tips

### ✍ Editable Plans
- Plans are saved as `.json` files per user
- You can load, **edit**, **delete**, and **save** them from the frontend

###  Domain-specific Chat Agents
- Talk directly to the Finance, Health, Learning, or Motivation coach
- Uses keyword-aware prompting guardrails to ensure relevant responses

###  Persistent Chat History
- Stores conversations by user ID
- Chat history can be viewed and cleared anytime

###  Streamlit UI
- Clean, minimal design with separate sections for planning and chatting
- Responsive inputs for customizing your plan

---

## 🛠 Tech Stack

| Layer         | Tech                     |
|--------------|--------------------------|
| Backend       | FastAPI (REST APIs)       |
| Frontend      | Streamlit (UI)            |
| AI Agents     | CrewAI +  Ollama |
| Storage       | JSON-based file system    |
| Auth (simple) | User ID-based local state |

---


##  How to Run Locally

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



## Sample Use Case
Enter your ID (e.g., rohit).

Input your goals (e.g., "Lose fat", "Earn ₹100,000", "Learn Python").

Generate a plan.

Chat with agents like the Finance Coach or Learning Coach.

Save, edit, or delete the plan any time.

## What's Happening Under the Hood?
CrewAI: Coordinates a Manager agent and 4 domain agents

LLMs: You can plug in OpenAI, Gemini, or run Ollama locally

Persistence: Uses local JSON for chats and plans

Context Management: Keyword-based filtering ensures agent relevance

Editing: Allows real-time editing of plan components via Streamlit forms

## What's Next?
- Vector-based memory for deeper personalization

- OAuth or simple auth layer

- Smart reminders via Telegram/Email

- Timeline-based visualizations for goals


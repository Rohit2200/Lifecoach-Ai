# backend/main.py

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from backend.workflows.lifecoach_workflow import generate_full_lifecoach_plan as v1_plan
from backend.workflows.lifecoach_workflow_v2 import generate_full_lifecoach_plan as v2_plan
from backend.agents.health_agent import health_agent
from backend.agents.finance_agent import finance_agent
from backend.agents.learning_agent import learning_agent
from backend.agents.motivation_agent import motivation_agent
from backend.utils.chat_storage import save_chat, load_chat, clear_chat
from backend.utils.plan_storage import (
    save_plan, load_plan, list_saved_plans,
    delete_plan, update_plan
)
from crewai import Task

app = FastAPI()

# ✅ Input models
class LifePlanInput(BaseModel):
    goal: str
    income: str
    learning_goal: str
    duration: int = 1
    preferences: Optional[Dict[str, str]] = None

class AgentChatInput(BaseModel):
    user_id: str
    agent: str
    message: str

# ✅ Keywords for basic input validation
topic_keywords = {
    "health": ["workout", "diet", "exercise", "fitness", "calorie", "protein", "weight", "meal"],
    "finance": ["budget", "income", "saving", "invest", "money", "loan", "expense", "debt"],
    "learning": ["learn", "study", "course", "dsa", "python", "machine learning", "skills", "language"],
    "motivation": ["motivate", "lazy", "discipline", "focus", "inspire", "consistency", "mindset"]
}

# ✅ Generate plan
@app.post("/life-plan")
def life_plan(input: LifePlanInput, request: Request):
    version = request.query_params.get("v2", "false").lower()
    use_v2 = version == "true"
    save_name = request.query_params.get("save_name")
    user_id = request.query_params.get("user_id")

    if use_v2:
        print("⚙️ Using V2 LifeCoach workflow with Manager Agent")
        result = v2_plan(
            input.goal,
            input.income,
            input.learning_goal,
            input.duration,
            input.preferences or {}
        )
    else:
        print("⚙️ Using V1 flat workflow")
        result = v1_plan(
            input.goal,
            input.income,
            input.learning_goal,
            input.duration
        )

    if save_name and user_id:
        save_plan(user_id, save_name, result["plan"] if "plan" in result else result)

    return result

# ✅ Chat with individual agent
@app.post("/agent-chat")
def agent_chat(input: AgentChatInput):
    agent_map = {
        "health": health_agent,
        "finance": finance_agent,
        "learning": learning_agent,
        "motivation": motivation_agent
    }

    selected_agent = agent_map.get(input.agent.lower())
    if not selected_agent:
        return {"error": "❌ Invalid agent name. Choose from: health, finance, learning, motivation."}

    keywords = topic_keywords.get(input.agent.lower(), [])
    if not any(word in input.message.lower() for word in keywords):
        return {
            "response": f"❌ Your question doesn't seem related to the {input.agent.title()} domain. Please switch to the right agent."
        }

    task = Task(
        description=input.message,
        expected_output=f"A helpful, concise, and personalized answer to the user's {input.agent.lower()}-related question.",
        agent=selected_agent
    )

    task.execute()
    response = task.output.result().strip()

    save_chat(input.user_id, {
        "user": input.message,
        "agent": response,
        "type": input.agent.lower()
    })

    return {"response": response}

# ✅ Load chat history
@app.get("/chat-history/{user_id}")
def get_chat_history(user_id: str):
    return load_chat(user_id)

# ✅ Clear chat history
@app.delete("/clear-chat/{user_id}")
def clear_chat_history(user_id: str):
    deleted = clear_chat(user_id)
    if deleted:
        return {"message": "✅ Chat history cleared."}
    else:
        raise HTTPException(status_code=404, detail="❌ No chat history found.")

# ✅ Load a saved plan
@app.get("/load-plan/{user_id}/{plan_name}")
def load_named_plan(user_id: str, plan_name: str):
    plan = load_plan(user_id, plan_name)
    if plan:
        return {"plan": plan}
    else:
        raise HTTPException(status_code=404, detail="❌ Plan not found.")

# ✅ List saved plan names
@app.get("/load-plan-names/{user_id}")
def get_plan_names(user_id: str):
    plans = list_saved_plans(user_id)
    return {"plans": plans}

# ✅ Delete saved plan
@app.delete("/delete-plan/{user_id}/{plan_name}")
def delete_saved_plan(user_id: str, plan_name: str):
    if delete_plan(user_id, plan_name):
        return {"message": f"✅ Plan '{plan_name}' deleted."}
    raise HTTPException(status_code=404, detail="❌ Plan not found.")

# ✅ Update saved plan
@app.put("/update-plan/{user_id}/{plan_name}")
def update_saved_plan(user_id: str, plan_name: str, updated_plan: dict):
    if update_plan(user_id, plan_name, updated_plan):
        return {"message": f"✅ Plan '{plan_name}' updated."}
    raise HTTPException(status_code=404, detail="❌ Plan not found.")

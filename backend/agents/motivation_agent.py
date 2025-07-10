# backend/agents/motivation_agent.py

from crewai import Agent
from backend.config import llm
from backend.utils.memory_manager import get_agent_memory

motivation_agent = Agent(
    role="Motivational Coach",
    goal="Inspire the user daily to stay consistent with their health, finance, and learning goals",
    backstory=(
        "You're a motivational coach and mindset expert. You help users stay focused, overcome laziness, and remain disciplined "
        "by sending them daily personalized motivation based on their goals."
    ),
    allow_delegation=False,
    verbose=True,
    memory=True,
    llm=llm,

)
motivation_agent.memory = get_agent_memory("motivation")

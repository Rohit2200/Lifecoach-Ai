
from crewai import Agent
from backend.config import llm
from backend.utils.memory_manager import get_agent_memory

manager_agent = Agent(
    role="Life Coach Manager",
    goal="Coordinate agents to generate a complete personalized life improvement plan",
    backstory=(
        "You are a senior life strategist responsible for overseeing the creation of personalized plans. "
        "You review the user's overall goals and assign responsibilities to each specialized agent (health, finance, learning, motivation)."
    ),
    allow_delegation=True,
    verbose=True,
    llm=llm,
    memory=True,
    
)
manager_agent.memory = get_agent_memory("manager")

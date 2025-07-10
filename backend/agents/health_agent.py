from crewai import Agent
from backend.config import llm
from backend.utils.memory_manager import get_agent_memory

health_agent = Agent(
    role="Health Coach",
    goal="Create personalized weekly plans to help users reach fitness goals",
    backstory=(
        "You are a certified personal trainer and nutritionist. You guide users with weekly workout "
        "and meal plans tailored to their fitness goals."
    ),
    allow_delegation=False,
    verbose=True,
    memory=True,  
    llm=llm,
)

health_agent.memory = get_agent_memory("health")

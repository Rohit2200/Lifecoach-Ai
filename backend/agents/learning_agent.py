
from crewai import Agent
from backend.config import llm
from backend.utils.memory_manager import get_agent_memory

learning_agent = Agent(
    role="Learning Mentor",
    goal="Guide users to upgrade their skills with a structured weekly learning plan",
    backstory=(
        "You are a veteran educator and learning strategist. "
        "You specialize in breaking down complex topics into simple daily tasks tailored to a user’s learning goal."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm,
    memory=True,

)

learning_agent.memory = get_agent_memory("learning")



from crewai import Agent
from backend.config import llm
from backend.utils.memory_manager import get_agent_memory

finance_agent = Agent(
    role="Financial Advisor",
    goal="Help users manage their monthly income with effective budgeting and savings strategies",
    backstory=(
        "You're a personal finance expert specializing in budgeting, expense tracking, and savings. "
        "You create monthly financial plans based on the user's income, fixed costs, and goals using methods like the 50/30/20 rule."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm,
    memory=True,
)
finance_agent.memory = get_agent_memory("finance")

# backend/workflows/lifecoach_workflow_v2.py

from crewai import Crew, Task
from backend.agents.manager_agent import manager_agent
from backend.agents.health_agent import health_agent
from backend.agents.finance_agent import finance_agent
from backend.agents.learning_agent import learning_agent
from backend.agents.motivation_agent import motivation_agent

def generate_full_lifecoach_plan(
    goal: str,
    income: str,
    learning_goal: str,
    duration: int = 1,
    preferences: dict = {}
):
    #  Extract optional preferences
    diet_pref = preferences.get("diet", "no dietary preference")
    workout_pref = preferences.get("workout_type", "no specific workout type")
    learning_style = preferences.get("learning_style", "no specific learning style")

    #  Subtask prompts (compressed + bullet-based)
    health_task = Task(
        description=(
            f"Give 3–4 concise health tips in bullet points for goal: '{goal}' "
            f"over {duration} day(s). Include diet (pref: {diet_pref}) and workout (pref: {workout_pref}). "
            "Avoid generic advice and keep it short."
        ),
        expected_output="3–4 actionable bullet points on meals, workout, or routines.",
        agent=health_agent
    )

    learning_task = Task(
        description=(
            f"Generate a {duration}-day learning plan for: '{learning_goal}', "
            f"with preferred style: {learning_style}. Give 3–4 bullet points only—brief, clear, and useful."
        ),
        expected_output="3–4 bullet points: daily topics or resources + 1 extra tip.",
        agent=learning_agent
    )

    motivation_task = Task(
        description=(
            f"Give {duration} motivational bullet tips to help user stay consistent "
            f"with their health, learning, and finance goals. Avoid quotes or repetition."
        ),
        expected_output=f"{duration} quick motivational bullet points.",
        agent=motivation_agent
    )

    finance_task = Task(
        description=(
            f"Break down a budget using ₹{income} income per month. "
            "Apply 50/30/20 rule and give 1 practical savings/investment tip. "
            "Use 3–4 clear bullet points, avoid jargon."
        ),
        expected_output="3–4 bullets: savings, essentials, discretionary, and 1 budgeting tip.",
        agent=finance_agent
    )

    #  High-level manager task
    high_level_task = Task(
        description=(
            f"The user wants a {duration}-day improvement plan.\n"
            f"Health Goal: {goal}\n"
            f"Monthly Income: ₹{income}\n"
            f"Learning Goal: {learning_goal}\n\n"
            "Coordinate 4 experts (health, learning, finance, motivation) to generate a final personalized plan.\n"
            "Ensure the final report has only short, actionable bullet points in each section."
        ),
        expected_output="Final formatted plan: Health, Learning, Motivation, Finance — each with 3–4 bullets.",
        agent=manager_agent,
        context=[health_task, learning_task, motivation_task, finance_task]
    )

    #  Launch CrewAI
    crew = Crew(
        agents=[manager_agent, health_agent, learning_agent, motivation_agent, finance_agent],
        tasks=[high_level_task],
        verbose=True
    )

    result = crew.kickoff()

    return {
        "plan": result.strip()
    }

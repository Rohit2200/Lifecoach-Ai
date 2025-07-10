
from crewai import Crew, Task
from backend.agents.health_agent import health_agent
from backend.agents.finance_agent import finance_agent
from backend.agents.learning_agent import learning_agent
from backend.agents.motivation_agent import motivation_agent

def generate_full_lifecoach_plan(goal: str, income: str, learning_goal: str, duration: int = 1):
    health_outputs = []
    learning_outputs = []
    motivation_outputs = []

    for day in range(1, duration + 1):
        # Health
        health_task = Task(
            description=(
                f"Day {day}: Give 3–4 bullet points with health tips for the goal '{goal}'. "
                "Include 1 meal idea, 1 workout suggestion, and 1 motivation/discipline tip. Keep it very concise."
            ),
            expected_output="• 3–4 short bullet points max",
            agent=health_agent
        )

        # Learning: topic + resource + tip
        learning_task = Task(
            description=(
                f"Day {day}: Suggest a micro-learning plan for the goal '{learning_goal}' in 3–4 bullets. "
                "Include topic, resource (video/article), and 1 productivity/study tip."
            ),
            expected_output="• Learning topic\n• Link or resource\n• 1 daily learning tip",
            agent=learning_agent
        )

        # Motivation: personalized, not cliche
        motivation_task = Task(
            description=(
                f"Day {day}: Write a **very short** motivational message to keep user focused on health, finance, and learning. "
                "Avoid cliches/quotes. Make it actionable or mindset-based."
            ),
            expected_output="• 1 short motivational bullet (max 1–2 lines)",
            agent=motivation_agent
        )

        # Kick off daily agents
        crew = Crew(
            agents=[health_agent, learning_agent, motivation_agent],
            tasks=[health_task, learning_task, motivation_task],
            verbose=False
        )

        crew.kickoff()

        health_outputs.append(f"**Day {day}**\n{health_task.output.result().strip()}")
        learning_outputs.append(f"**Day {day}**\n{learning_task.output.result().strip()}")
        motivation_outputs.append(f"**Day {day}**\n{motivation_task.output.result().strip()}")

    # Finance plan (only once)
    finance_task = Task(
        description=(
            f"User earns ₹{income}/month. Build a budget using 50/30/20 rule (Essentials, Wants, Savings). "
            "Give a very short tip on saving or investing. Output in 3–4 bullets."
        ),
        expected_output="• 3–4 bullet points: budget breakdown + 1 savings/investing tip",
        agent=finance_agent
    )

    Crew(
        agents=[finance_agent],
        tasks=[finance_task],
        verbose=False
    ).kickoff()

    return {
        "health_plan": "\n\n".join(health_outputs),
        "learning_plan": "\n\n".join(learning_outputs),
        "motivation_plan": "\n\n".join(motivation_outputs),
        "finance_plan": finance_task.output.result().strip()
    }

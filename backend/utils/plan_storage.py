
import os
import json

def get_user_plan_dir(user_id: str) -> str:
    """
    Returns the directory path for storing user-specific plans.
    Creates it if it doesn't exist.
    """
    directory = f"saved_plans/{user_id}"
    os.makedirs(directory, exist_ok=True)
    return directory

def save_plan(user_id: str, plan_name: str, plan_data: dict | str) -> None:
    """
    Save a plan (dict or str) as a JSON file for the user.
    """
    directory = get_user_plan_dir(user_id)
    path = os.path.join(directory, f"{plan_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plan_data, f, ensure_ascii=False, indent=2)

def load_plan(user_id: str, plan_name: str) -> dict | str | None:
    """
    Load a saved plan (returns dict or str depending on how it was saved).
    """
    path = os.path.join(get_user_plan_dir(user_id), f"{plan_name}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None

def list_saved_plans(user_id: str) -> list[str]:
    """
    List all saved plan names (excluding .json extension) for a user.
    """
    directory = get_user_plan_dir(user_id)
    return [f[:-5] for f in os.listdir(directory) if f.endswith(".json")]


def delete_plan(user_id: str, plan_name: str) -> bool:
    """
    Delete a specific saved plan file.
    Returns True if deleted, False if it didn't exist.
    """
    path = os.path.join(get_user_plan_dir(user_id), f"{plan_name}.json")
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def update_plan(user_id: str, plan_name: str, new_plan_data: dict) -> bool:
    """
    Update an existing plan with new data.
    Returns True if updated, False if the plan does not exist.
    """
    path = os.path.join(get_user_plan_dir(user_id), f"{plan_name}.json")
    if os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(new_plan_data, f, ensure_ascii=False, indent=2)
        return True
    return False

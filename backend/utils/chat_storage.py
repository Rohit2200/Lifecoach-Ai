import os
import json
from typing import List, Dict

CHAT_DIR = "backend/data/chat_logs"
os.makedirs(CHAT_DIR, exist_ok=True)

def get_chat_filepath(user_id: str) -> str:
    return os.path.join(CHAT_DIR, f"{user_id}.json")

def save_chat(user_id: str, message: Dict):
    filepath = get_chat_filepath(user_id)
    history = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            history = json.load(f)
    history.append(message)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def load_chat(user_id: str) -> List[Dict]:
    filepath = get_chat_filepath(user_id)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def clear_chat(user_id: str) -> bool:
    filepath = get_chat_filepath(user_id)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

import json
from datetime import datetime
from config import HISTORY_FILE

def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

def log_change(category, old_value, new_value):
    if old_value == new_value:
        return  # Loguj pouze změněné hodnoty
    
    history = load_history()
    history.append({
        "category": category,
        "old_value": old_value,
        "new_value": new_value,
        "timestamp": datetime.now().isoformat()
    })
    save_history(history)

def clear_history():
    save_history([])

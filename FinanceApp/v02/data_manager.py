import json
from config import DATA_FILE

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_entry(category, description, amount):
    data = load_data()
    if category not in data:
        data[category] = []
    data[category].append({"description": description, "amount": amount})
    save_data(data)

def remove_entry(category, description):
    data = load_data()
    if category in data:
        data[category] = [item for item in data[category] if item["description"] != description]
        if not data[category]:
            del data[category]
        save_data(data)

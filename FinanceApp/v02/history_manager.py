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

def delete_history_entries(criteria=None):
    """
    Delete specific history entries based on provided criteria.
    
    Parameters:
    - criteria (dict, optional): A dictionary with conditions for deletion.
      Supported keys: 'category', 'before_date', 'after_date', 'id' (index)
      
    Returns:
    - int: Number of entries deleted
    
    Examples:
    - delete_history_entries({'category': 'price'})  # Delete all price changes
    - delete_history_entries({'before_date': '2023-01-01'})  # Delete old entries
    - delete_history_entries({'id': 5})  # Delete entry with index 5
    """
    if criteria is None:
        return 0
        
    history = load_history()
    original_length = len(history)
    
    if 'id' in criteria and isinstance(criteria['id'], int):
        # Delete by specific index
        if 0 <= criteria['id'] < len(history):
            del history[criteria['id']]
    else:
        # Filter based on criteria
        new_history = []
        for entry in history:
            should_keep = True
            
            # Filter by category - pokud kategorie odpovídá, NEUCHOVÁME záznam
            if 'category' in criteria and entry['category'] == criteria['category']:
                should_keep = False
            
            # Filter by date range - zachováme původní funkcionalitu
            elif 'before_date' in criteria:
                entry_date = datetime.fromisoformat(entry['timestamp'])
                before_date = datetime.fromisoformat(criteria['before_date'])
                if entry_date < before_date:
                    should_keep = False
                    
            elif 'after_date' in criteria:
                entry_date = datetime.fromisoformat(entry['timestamp'])
                after_date = datetime.fromisoformat(criteria['after_date'])
                if entry_date > after_date:
                    should_keep = False
            
            if should_keep:
                new_history.append(entry)
        
        history = new_history
    
    save_history(history)
    return original_length - len(history)



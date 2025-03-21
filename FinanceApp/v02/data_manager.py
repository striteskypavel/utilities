import json
import os
import pandas as pd
from config import DATA_FILE, HISTORY_FILE

def load_data(file_path=None):
    try:
        path = file_path or DATA_FILE
        with open(path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(data, file_path=None):
    path = file_path or DATA_FILE
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as file:
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

def export_data(file_path):
    """Exportuje všechna data do zadaného souboru."""
    data = {
        "finance_data": load_data(DATA_FILE),
        "history_data": load_data(HISTORY_FILE)
    }
    save_data(data, file_path)

def import_data(file_path):
    """Importuje data ze zadaného souboru."""
    try:
        if file_path.endswith('.json'):
            data = load_data(file_path)
            if "finance_data" in data:
                save_data(data["finance_data"], DATA_FILE)
            if "history_data" in data:
                save_data(data["history_data"], HISTORY_FILE)
            return True
        elif file_path.endswith('.csv'):
            # Načtení CSV souboru
            df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')
            
            # Převod DataFrame na formát aplikace
            data = {}
            for _, row in df.iterrows():
                category = row['Kategorie']
                amount = float(str(row['Částka']).replace(' Kč', '').replace(' ', ''))
                description = row['Popis'] if 'Popis' in df.columns else category
                
                if category not in data:
                    data[category] = []
                data[category].append({
                    "description": description,
                    "amount": amount
                })
            
            # Uložení dat
            save_data(data, DATA_FILE)
            return True
            
    except Exception as e:
        print(f"Error importing data: {e}")
        return False

def change_data_location(new_path):
    """Změní umístění datových souborů."""
    global DATA_FILE, HISTORY_FILE
    DATA_FILE = os.path.join(new_path, "finance_data.json")
    HISTORY_FILE = os.path.join(new_path, "history_data.json")
    
    # Vytvoří novou složku, pokud neexistuje
    os.makedirs(new_path, exist_ok=True)
    
    # Zkopíruje existující data do nového umístění
    old_data = load_data()
    if old_data:
        save_data(old_data)

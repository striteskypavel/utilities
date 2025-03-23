import json
import csv
import os
from datetime import datetime
import tempfile
import pandas as pd

# Cesta k datovým souborům
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_user_data_file(username):
    """Vrátí cestu k datovému souboru uživatele."""
    return os.path.join(DATA_DIR, f"{username}_data.json")

def get_user_history_file(username):
    """Vrátí cestu k souboru s historií uživatele."""
    return os.path.join(DATA_DIR, f"{username}_history.json")

def load_data(username):
    """Načte data pro konkrétního uživatele."""
    data_file = get_user_data_file(username)
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(username, data):
    """Uloží data pro konkrétního uživatele."""
    data_file = get_user_data_file(username)
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_history(username):
    """Načte historii pro konkrétního uživatele."""
    history_file = get_user_history_file(username)
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(username, history):
    """Uloží historii pro konkrétního uživatele."""
    history_file = get_user_history_file(username)
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_entry(username: str, category: str, entry_data: dict) -> bool:
    """Přidá nový záznam do historie"""
    try:
        # Načtení existujících dat
        data = load_data(username)
        
        # Přidání nového záznamu
        if category in data:
            if isinstance(data[category], list):
                data[category].append(entry_data)
            else:
                data[category] = [data[category], entry_data]
        else:
            data[category] = entry_data
        
        # Uložení aktualizovaných dat
        save_data(username, data)
        return True
    except Exception as e:
        print(f"Chyba při přidávání záznamu: {str(e)}")
        return False

def export_data(username: str, file_path: str, *, format: str = "json") -> bool:
    """Exportuje data uživatele do zvoleného formátu."""
    try:
        data = load_data(username)
        
        if format == "json":
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif format == "csv":
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Kategorie', 'Částka', 'Datum', 'Poznámka'])
                
                for category, entries in data.items():
                    for entry in entries:
                        writer.writerow([
                            category,
                            entry['amount'],
                            entry['timestamp'],
                            entry.get('note', '')
                        ])
        else:
            raise ValueError(f"Nepodporovaný formát: {format}")
        
        return True
    except Exception as e:
        print(f"Chyba při exportu dat: {e}")
        return False

def import_data(username: str, path: str, *, format: str = "json") -> bool:
    """Importuje data z JSON nebo CSV souboru"""
    try:
        if format == "json":
            with open(path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
                
            # Převedení JSON dat do správného formátu
            formatted_data = {}
            for category, entries in imported_data.items():
                if not isinstance(entries, list):
                    entries = [entries]
                formatted_data[category] = []
                for entry in entries:
                    formatted_data[category].append({
                        "amount": float(entry["amount"]),
                        "timestamp": entry.get("timestamp") or entry.get("Datum") or entry.get("date") or datetime.now().isoformat(),
                        "note": entry.get("note") or entry.get("Poznámka", "")
                    })
        else:  # CSV
            df = pd.read_csv(path)
            formatted_data = {}
            
            # Převedení CSV dat do formátu aplikace
            for _, row in df.iterrows():
                category = row['Kategorie']
                if category not in formatted_data:
                    formatted_data[category] = []
                
                formatted_data[category].append({
                    "amount": float(row['Částka']),
                    "timestamp": row.get('Datum') or datetime.now().isoformat(),
                    "note": row.get('Poznámka', '')
                })
        
        # Načtení existujících dat
        current_data = load_data(username)
        
        # Aktualizace dat
        for category, entries in formatted_data.items():
            if category not in current_data:
                current_data[category] = []
            current_data[category].extend(entries)
        
        # Uložení aktualizovaných dat
        save_data(username, current_data)
        return True
        
    except Exception as e:
        print(f"Chyba při importu dat: {e}")
        return False

def clear_history(username: str) -> bool:
    """Vymaže celou historii uživatele"""
    try:
        history_file = get_user_history_file(username)
        if os.path.exists(history_file):
            os.remove(history_file)
        return True
    except Exception as e:
        print(f"Chyba při mazání historie: {e}")
        return False

import json
import csv
import os
from datetime import datetime
import tempfile
import pandas as pd

# Cesta k datovým souborům
DATA_DIR = os.getenv("DATA_DIR", "data")
USER_DATA_DIR = os.getenv("USER_DATA_DIR", os.path.join(DATA_DIR, "users"))

# Vytvoření všech potřebných adresářů
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(USER_DATA_DIR, exist_ok=True)

def get_user_data_file(username):
    """Vrátí cestu k datovému souboru uživatele."""
    return os.path.join(DATA_DIR, f"{username}_data.json")

def get_user_history_file(username):
    """Vrátí cestu k souboru s historií uživatele."""
    return os.path.join(DATA_DIR, f"{username}_history.json")

def get_user_file_path(username):
    """Vrátí cestu k souboru s daty uživatele"""
    return os.path.join(USER_DATA_DIR, f"{username}.json")

def load_data(username):
    """Načte data pro konkrétního uživatele."""
    data_file = get_user_data_file(username)
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Pokud neexistují investiční data, vytvoříme výchozí strukturu
            if not any(key in data for key in ["ETF", "Akcie", "Kryptoměny", "Nemovitosti", "Dluhopisy", "Hotovost", "Důchodové"]):
                data.update({
                    "ETF": [
                        {"amount": 500000, "timestamp": datetime.now().isoformat(), "note": "Vanguard S&P 500 ETF"},
                        {"amount": 300000, "timestamp": datetime.now().isoformat(), "note": "iShares MSCI World ETF"}
                    ],
                    "Akcie": [
                        {"amount": 200000, "timestamp": datetime.now().isoformat(), "note": "Apple Inc."},
                        {"amount": 150000, "timestamp": datetime.now().isoformat(), "note": "Microsoft Corp."}
                    ],
                    "Kryptoměny": [
                        {"amount": 100000, "timestamp": datetime.now().isoformat(), "note": "Bitcoin"},
                        {"amount": 50000, "timestamp": datetime.now().isoformat(), "note": "Ethereum"}
                    ],
                    "Nemovitosti": [
                        {"amount": 2000000, "timestamp": datetime.now().isoformat(), "note": "Byt v centru"}
                    ],
                    "Dluhopisy": [
                        {"amount": 400000, "timestamp": datetime.now().isoformat(), "note": "Státní dluhopisy"}
                    ],
                    "Hotovost": [
                        {"amount": 300000, "timestamp": datetime.now().isoformat(), "note": "Běžný účet"},
                        {"amount": 200000, "timestamp": datetime.now().isoformat(), "note": "Termínovaný vklad"}
                    ],
                    "Důchodové": [
                        {"amount": 600000, "timestamp": datetime.now().isoformat(), "note": "Penzijní připojištění"}
                    ]
                })
                save_data(username, data)
            
            return data
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

def add_entry(username: str, category: str, entry_data: any) -> bool:
    """Přidá nový záznam do historie"""
    try:
        # Načtení existujících dat
        data = load_data(username)
        print(f"Existing data: {data}")
        
        # Příprava záznamu
        if isinstance(entry_data, (int, float)):
            entry = {
                "amount": float(entry_data),
                "timestamp": datetime.now().isoformat(),
                "note": ""
            }
        else:
            entry = entry_data
        print(f"New entry: {entry}")
        
        # Přidání nového záznamu
        if category not in data:
            data[category] = []
        elif not isinstance(data[category], list):
            data[category] = [data[category]]
        
        data[category].append(entry)
        print(f"Updated data: {data}")
        
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
                    if not isinstance(entries, list):
                        entries = [entries]
                    for entry in entries:
                        if isinstance(entry, (int, float)):
                            writer.writerow([
                                category,
                                entry,
                                datetime.now().isoformat(),
                                ''
                            ])
                        elif isinstance(entry, dict):
                            writer.writerow([
                                category,
                                entry['amount'],
                                entry.get('timestamp', datetime.now().isoformat()),
                                entry.get('note', '')
                            ])
                        else:
                            print(f"Přeskočen nepodporovaný formát záznamu: {entry}")
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
        
        # Uložení nových dat (přepsání existujících)
        save_data(username, formatted_data)
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

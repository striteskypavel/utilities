import json
import csv
import os
from datetime import datetime
import tempfile
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
import re

# Cesta k datovým souborům
DATA_DIR = os.getenv("DATA_DIR", "data")
USER_DATA_DIR = os.getenv("USER_DATA_DIR", os.path.join(DATA_DIR, "users"))

# Vytvoření všech potřebných adresářů
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(USER_DATA_DIR, exist_ok=True)

class DataManager:
    def __init__(self):
        """Inicializace DataManager."""
        self.data_dir = DATA_DIR
        self.user_data_dir = USER_DATA_DIR
        os.makedirs(self.user_data_dir, exist_ok=True)

    def get_user_data_file(self, username):
        """Vrátí cestu k datovému souboru uživatele."""
        return os.path.join(self.data_dir, f"{username}_data.json")

    def get_user_history_file(self, username):
        """Vrátí cestu k souboru s historií uživatele."""
        return os.path.join(self.data_dir, f"{username}_history.json")

    def get_user_file_path(self, username):
        """Vrátí cestu k souboru s daty uživatele."""
        return os.path.join(self.user_data_dir, f"{username}.json")

    def validate_password(self, password):
        """Validace hesla."""
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):  # Velké písmeno
            return False
        if not re.search(r"[a-z]", password):  # Malé písmeno
            return False
        if not re.search(r"\d", password):     # Číslo
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Speciální znak
            return False
        return True

    def validate_email(self, email):
        """Validace emailu."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))

    def validate_username(self, username, check_existence=False):
        """Validace uživatelského jména."""
        # Kontrola délky
        if len(username) < 3:
            return False
        
        # Kontrola povolených znaků (písmena, čísla, podtržítko)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False
        
        # Kontrola existence uživatele (volitelná)
        if check_existence:
            try:
                user_file = self.get_user_file_path(username)
                if os.path.exists(user_file):
                    return False
            except Exception as e:
                print(f"Chyba při validaci uživatelského jména: {str(e)}")
                return False
        
        return True

    def is_email_unique(self, email):
        """Kontrola unikátnosti emailu."""
        try:
            for filename in os.listdir(self.user_data_dir):
                if filename.endswith('.json'):
                    try:
                        with open(os.path.join(self.user_data_dir, filename), 'r') as f:
                            user_data = json.load(f)
                            if isinstance(user_data, dict) and user_data.get('email') == email:
                                return False
                    except (json.JSONDecodeError, IOError, Exception) as e:
                        print(f"Chyba při čtení souboru {filename}: {str(e)}")
                        continue
            return True
        except Exception as e:
            print(f"Chyba při kontrole unikátnosti emailu: {str(e)}")
            return False  # Pokud nelze ověřit, předpokládáme, že email není unikátní

    def create_user(self, username, password, email):
        """Vytvoří nového uživatele s validací."""
        try:
            # Vytvoření adresářů
            os.makedirs(self.data_dir, exist_ok=True)
            os.makedirs(self.user_data_dir, exist_ok=True)
            
            # Validace vstupů
            if not self.validate_username(username, check_existence=True):
                return False
            if not self.validate_password(password):
                return False
            if not self.validate_email(email):
                return False
            if not self.is_email_unique(email):
                return False
            
            # Vytvoření uživatele
            user_file = self.get_user_file_path(username)
            password_hash = generate_password_hash(password, method='pbkdf2:sha256:600000')
            
            user_data = {
                "username": username,
                "password": password_hash,
                "email": email,
                "created_at": datetime.now().isoformat()
            }
            
            with open(user_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=2)
            
            # Vytvoření výchozích souborů pro data
            self.save_data(username, {})
            self.save_history(username, [])
            
            return True
        except Exception as e:
            print(f"Chyba při vytváření uživatele: {str(e)}")
            return False

    def get_user(self, username):
        """Získá data uživatele."""
        user_file = self.get_user_file_path(username)
        if os.path.exists(user_file):
            with open(user_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def get_user_investments_file(self, username):
        """Vrátí cestu k souboru s investicemi uživatele."""
        return os.path.join(self.user_data_dir, f"{username}_investments.json")

    def get_user_expenses_file(self, username):
        """Vrátí cestu k souboru s výdaji uživatele."""
        return os.path.join(self.user_data_dir, f"{username}_expenses.json")

    def load_data(self, username):
        """Načte data pro konkrétního uživatele."""
        data_file = self.get_user_data_file(username)
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
                    self.save_data(username, data)
                
                return data
        return {}

    def save_data(self, username, data):
        """Uloží data pro konkrétního uživatele."""
        data_file = self.get_user_data_file(username)
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_history(self, username):
        """Načte historii pro konkrétního uživatele."""
        history_file = self.get_user_history_file(username)
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_history(self, username, history):
        """Uloží historii pro konkrétního uživatele."""
        history_file = self.get_user_history_file(username)
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def add_entry(self, username: str, category: str, entry_data: any) -> bool:
        """Přidá nový záznam do historie"""
        try:
            # Načtení existujících dat
            data = self.load_data(username)
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
            self.save_data(username, data)
            return True
        except Exception as e:
            print(f"Chyba při přidávání záznamu: {str(e)}")
            return False

    def export_data(self, username: str, file_path: str, *, format: str = "json") -> bool:
        """Exportuje data uživatele do zvoleného formátu."""
        try:
            data = self.load_data(username)
            
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

    def import_data(self, username: str, path: str, *, format: str = "json") -> bool:
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
            self.save_data(username, formatted_data)
            return True
            
        except Exception as e:
            print(f"Chyba při importu dat: {e}")
            return False

    def clear_history(self, username: str) -> bool:
        """Vymaže celou historii uživatele"""
        try:
            history_file = self.get_user_history_file(username)
            if os.path.exists(history_file):
                os.remove(history_file)
            return True
        except Exception as e:
            print(f"Chyba při mazání historie: {e}")
            return False

    def load_investments(self, username):
        """Načte investice pro konkrétního uživatele."""
        investments_file = self.get_user_investments_file(username)
        try:
            if os.path.exists(investments_file):
                with open(investments_file, 'r', encoding='utf-8') as f:
                    try:
                        return json.load(f)
                    except json.JSONDecodeError:
                        print(f"Poškozený soubor s investicemi pro uživatele {username}")
                        backup_file = investments_file + '.backup'
                        if os.path.exists(investments_file):
                            os.rename(investments_file, backup_file)
                        return []
            return []
        except Exception as e:
            print(f"Chyba při načítání investic: {str(e)}")
            return []

    def load_expenses(self, username):
        """Načte výdaje pro konkrétního uživatele."""
        expenses_file = self.get_user_expenses_file(username)
        try:
            if os.path.exists(expenses_file):
                with open(expenses_file, 'r', encoding='utf-8') as f:
                    try:
                        return json.load(f)
                    except json.JSONDecodeError:
                        print(f"Poškozený soubor s výdaji pro uživatele {username}")
                        backup_file = expenses_file + '.backup'
                        if os.path.exists(expenses_file):
                            os.rename(expenses_file, backup_file)
                        return []
            return []
        except Exception as e:
            print(f"Chyba při načítání výdajů: {str(e)}")
            return []

    def save_investments(self, username, investments):
        """Uloží investice pro konkrétního uživatele."""
        investments_file = self.get_user_investments_file(username)
        with open(investments_file, 'w', encoding='utf-8') as f:
            json.dump(investments, f, ensure_ascii=False, indent=2)

    def save_expenses(self, username, expenses):
        """Uloží výdaje pro konkrétního uživatele."""
        expenses_file = self.get_user_expenses_file(username)
        with open(expenses_file, 'w', encoding='utf-8') as f:
            json.dump(expenses, f, ensure_ascii=False, indent=2)

    def verify_user(self, username, password):
        """Ověří přihlašovací údaje uživatele."""
        user = self.get_user(username)
        if not user or 'password' not in user:
            return False
        try:
            return check_password_hash(user['password'], password)
        except ValueError:
            # If the hash method is invalid, try to rehash the password
            try:
                # Generate a new hash with the correct method
                new_hash = generate_password_hash(password, method='pbkdf2:sha256:600000')
                # Update the user's password hash
                user['password'] = new_hash
                with open(self.get_user_file_path(username), 'w', encoding='utf-8') as f:
                    json.dump(user, f, ensure_ascii=False, indent=2)
                return True
            except:
                return False

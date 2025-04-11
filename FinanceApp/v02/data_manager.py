import json
import csv
import os
from datetime import datetime
import tempfile
import pandas as pd
from werkzeug.security import check_password_hash, generate_password_hash
import re

class DataManager:
    # Default paths for data storage
    DEFAULT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    DEFAULT_USER_DATA_DIR = None  # Will be set based on DATA_DIR

    def __init__(self, data_dir=None):
        """Initialize the DataManager with specified or default directories."""
        self.data_dir = data_dir or os.getenv("DATA_DIR", self.DEFAULT_DATA_DIR)
        self.user_data_dir = os.path.join(self.data_dir, "users")
        
        self.expense_file = os.path.join(self.data_dir, "expenses.json")
        self.investment_file = os.path.join(self.data_dir, "investments.json")
        self.history_file = os.path.join(self.data_dir, "history.json")
        self.users_file = os.path.join(self.user_data_dir, "users.json")
        
        self.ensure_directories()
        self.ensure_files()
        
    def ensure_directories(self):
        """Ensure data directories exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.user_data_dir, exist_ok=True)
        
    def ensure_files(self):
        """Ensure data files exist with empty lists"""
        for file_path in [self.expense_file, self.investment_file, self.history_file, self.users_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f)

    def create_user(self, username, password, email):
        """Vytvoří nového uživatele."""
        try:
            # Validace vstupních dat
            if not self.validate_username(username) or not self.validate_password(password) or not self.validate_email(email):
                return False

            users = self.load_users()
            if username in users:
                return False
            if any(user['email'] == email for user in users.values()):
                return False

            # Vytvoření nového uživatele
            users[username] = {
                'username': username,
                'password': generate_password_hash(password),
                'email': email,
                'created_at': datetime.now().isoformat()
            }
            
            # Uložení uživatele
            self.save_users(users)
            
            # Vytvoření výchozí struktury dat
            self.save_data(username, {'expense': [], 'investment': []})
            
            return True
        except Exception as e:
            print(f"Chyba při vytváření uživatele: {str(e)}")
            return False

    def verify_user(self, username, password):
        """Ověří uživatele."""
        try:
            users = self.load_users()
            if username not in users:
                return False
            user = users[username]
            return check_password_hash(user['password'], password)
        except Exception as e:
            print(f"Chyba při ověřování uživatele: {str(e)}")
            return False

    def update_user_password(self, username, new_password):
        """Aktualizuje heslo uživatele."""
        try:
            if not self.validate_password(new_password):
                return False

            users = self.load_users()
            if username not in users:
                return False

            users[username]['password'] = generate_password_hash(new_password, method='pbkdf2:sha256')
            self.save_users(users)
            return True
        except Exception as e:
            print(f"Chyba při aktualizaci hesla: {str(e)}")
            return False

    def validate_username(self, username):
        """Validuje uživatelské jméno."""
        return bool(username and len(username) >= 3 and re.match(r'^[a-zA-Z0-9_]+$', username))

    def validate_password(self, password):
        """Validuje heslo."""
        if not password or len(password) < 8:
            return False
        # Check for at least one number
        if not any(c.isdigit() for c in password):
            return False
        # Check for at least one letter
        if not any(c.isalpha() for c in password):
            return False
        # Check for at least one uppercase letter
        if not any(c.isupper() for c in password):
            return False
        # Check for at least one special character
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            return False
        return True

    def validate_email(self, email):
        """Validuje email."""
        return bool(email and re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

    def load_users(self):
        """Načte data uživatelů."""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Chyba při načítání uživatelů: {str(e)}")
            return {}

    def save_users(self, users):
        """Uloží data uživatelů."""
        try:
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Chyba při ukládání uživatelů: {str(e)}")
            return False

    def load_data(self, username):
        """Načte data uživatele."""
        try:
            data_file = os.path.join(self.data_dir, f"{username}_data.json")
            if os.path.exists(data_file):
                with open(data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {'expense': [], 'investment': []}
        except Exception as e:
            print(f"Chyba při načítání dat: {str(e)}")
            return {'expense': [], 'investment': []}

    def save_data(self, username, data):
        """Uloží data uživatele."""
        try:
            data_file = os.path.join(self.data_dir, f"{username}_data.json")
            os.makedirs(os.path.dirname(data_file), exist_ok=True)
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Chyba při ukládání dat: {str(e)}")
            return False

    def add_entry(self, username, category, entry):
        """Přidá nový záznam pro daného uživatele."""
        try:
            # Kontrola prázdné kategorie
            if not category or category.strip() == "":
                raise ValueError("Kategorie nemůže být prázdná")

            # Načtení existujících dat
            data = self.load_data(username)

            # Inicializace kategorie, pokud neexistuje
            if category not in data:
                data[category] = []

            # Kontrola duplicitního záznamu
            for existing_entry in data[category]:
                if (existing_entry.get('type') == entry.get('type') and
                    abs(float(existing_entry.get('amount', 0)) - float(entry.get('amount', 0))) < 0.01 and
                    existing_entry.get('timestamp') == entry.get('timestamp')):
                    return True  # Duplicitní záznam nalezen

            # Přidání nového záznamu
            data[category].append(entry)
            self.save_data(username, data)
            return True
        except Exception as e:
            print(f"Chyba při přidávání záznamu: {str(e)}")
            return False

    def get_history(self, username: str) -> dict:
        """Načte historii pro konkrétního uživatele."""
        try:
            history_file = self.get_user_history_file(username)
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    return history
            return {}
        except Exception as e:
            print(f"Chyba při načítání historie: {str(e)}")
            return {}

    def get_user_file_path(self, username):
        """Vrátí cestu k souboru uživatele."""
        return os.path.join(self.user_data_dir, f"{username}.json")

    def get_user_investments_file(self, username):
        """Vrátí cestu k souboru s investicemi uživatele."""
        return os.path.join(self.data_dir, f"{username}_investments.json")

    def get_user_expenses_file(self, username):
        """Vrátí cestu k souboru s výdaji uživatele."""
        return os.path.join(self.data_dir, f"{username}_expenses.json")

    def get_user_history_file(self, username):
        """Vrátí cestu k souboru s historií uživatele."""
        return os.path.join(self.data_dir, f"{username}_history.json")

    def load_expenses(self, username):
        """Načte výdaje uživatele."""
        try:
            # Nejprve zkusíme načíst z nové struktury
            data = self.load_data(username)
            expenses = []
            for category, entries in data.items():
                for entry in entries:
                    if entry['type'] == 'Výdaj':
                        expenses.append({
                            'category': category,
                            'amount': float(entry['amount']),
                            'timestamp': entry['timestamp'],
                            'note': entry.get('note', '')
                        })
            return expenses
        except Exception as e:
            print(f"Chyba při načítání výdajů: {str(e)}")
            return []

    def load_investments(self, username):
        """Načte investice uživatele."""
        try:
            # Nejprve zkusíme načíst z nové struktury
            data = self.load_data(username)
            investments = data.get('investment', [])
            if investments:
                return investments

            # Pokud nejsou v nové struktuře, zkusíme starou
            investments_file = self.get_user_investments_file(username)
            if os.path.exists(investments_file):
                with open(investments_file, 'r', encoding='utf-8') as f:
                    try:
                        investments = json.load(f)
                        # Uložíme do nové struktury pro příští použití
                        data['investment'] = investments
                        self.save_data(username, data)
                        return investments
                    except json.JSONDecodeError:
                        # Pokud je soubor poškozen, vytvoříme zálohu
                        backup_file = investments_file + '.backup'
                        os.rename(investments_file, backup_file)
                        return []
            return []
        except Exception as e:
            print(f"Chyba při načítání investic: {str(e)}")
            return []

    def get_user_data(self, username):
        """Získá kompletní data uživatele."""
        try:
            # Načtení základních údajů o uživateli
            users = self.load_users()
            if username not in users:
                return None
            
            user_data = users[username].copy()
            
            # Načtení dodatečných dat uživatele
            data = self.load_data(username)
            if data:
                user_data.update(data)
            
            # Pokud chybí created_at, přidáme aktuální čas
            if 'created_at' not in user_data:
                user_data['created_at'] = datetime.now().isoformat()
                users[username]['created_at'] = user_data['created_at']
                self.save_users(users)
            
            # Přidání stavu přihlášení
            user_data['is_authenticated'] = True
            user_data['last_activity'] = datetime.now().isoformat()
            
            return user_data
        except Exception as e:
            print(f"Chyba při načítání dat uživatele: {str(e)}")
            return None

    def save_expenses(self, username, expenses):
        """Uloží výdaje uživatele."""
        try:
            # Uložení do nové struktury
            data = self.load_data(username)
            data['expense'] = expenses
            self.save_data(username, data)

            # Uložení do starého formátu pro zpětnou kompatibilitu
            expenses_file = self.get_user_expenses_file(username)
            os.makedirs(os.path.dirname(expenses_file), exist_ok=True)
            with open(expenses_file, 'w', encoding='utf-8') as f:
                json.dump(expenses, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Chyba při ukládání výdajů: {str(e)}")
            return False

    def save_investments(self, username, investments):
        """Uloží investice uživatele."""
        try:
            # Uložení do nové struktury
            data = self.load_data(username)
            data['investment'] = investments
            self.save_data(username, data)

            # Uložení do starého formátu pro zpětnou kompatibilitu
            investments_file = self.get_user_investments_file(username)
            os.makedirs(os.path.dirname(investments_file), exist_ok=True)
            with open(investments_file, 'w', encoding='utf-8') as f:
                json.dump(investments, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Chyba při ukládání investic: {str(e)}")
            return False

    def import_data(self, username, file_path, format="json"):
        """Importuje data z JSON nebo CSV souboru."""
        try:
            if format == "json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif format == "csv":
                df = pd.read_csv(file_path)
                data = {}
                for _, row in df.iterrows():
                    category = row['Kategorie']
                    if category not in data:
                        data[category] = []
                    data[category].append({
                        "amount": float(row['Částka']),
                        "timestamp": row['Datum'],
                        "note": row['Poznámka']
                    })
            else:
                return False

            self.save_data(username, data)
            return True
        except Exception as e:
            print(f"Chyba při importu dat: {str(e)}")
            return False

    def export_data(self, username, file_path, format="json"):
        """Exportuje data do JSON nebo CSV souboru."""
        try:
            data = self.load_data(username)
            if format == "json":
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            elif format == "csv":
                rows = []
                for category, entries in data.items():
                    for entry in entries:
                        row = {
                            'Kategorie': category,
                            'Částka': entry.get('amount', ''),
                            'Datum': entry.get('timestamp', ''),
                            'Poznámka': entry.get('note', '')
                        }
                        rows.append(row)
                df = pd.DataFrame(rows)
                df.to_csv(file_path, index=False, encoding='utf-8')
            else:
                return False
            return True
        except Exception as e:
            print(f"Chyba při exportu dat: {str(e)}")
            return False 

    def get_user(self, username):
        """Získá data uživatele."""
        users = self.load_users()
        return users.get(username)
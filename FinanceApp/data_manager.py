import json
import os
from datetime import datetime
import shutil
from typing import Dict, List, Optional
from config import (
    get_user_expenses_file,
    get_user_investments_file,
    get_backup_file,
    USER_DATA_DIR,
    BACKUP_DIR
)

class DataManager:
    def __init__(self):
        """Inicializace správce dat"""
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.ensure_directories()

    def ensure_directories(self):
        """Zajistí existenci potřebných adresářů"""
        os.makedirs(USER_DATA_DIR, exist_ok=True)
        os.makedirs(BACKUP_DIR, exist_ok=True)

    def _get_user_file(self, username: str) -> str:
        """Získá cestu k souboru s daty uživatele"""
        return os.path.join(self.data_dir, f"{username}.json")

    def load_data(self, username: str) -> dict:
        """Načte data uživatele"""
        file_path = self._get_user_file(username)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_data(self, username: str, data: dict) -> bool:
        """Uloží data uživatele"""
        try:
            file_path = self._get_user_file(username)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Chyba při ukládání dat: {e}")
            return False

    def add_entry(self, username: str, category: str, entry: dict) -> bool:
        """Přidá nový záznam"""
        # Kontrola prázdné kategorie
        if not category or not category.strip():
            raise ValueError("Kategorie nemůže být prázdná")
        
        try:
            data = self.load_data(username)
            
            # Přidání záznamu do kategorie
            if category not in data:
                data[category] = []
            
            # Kontrola duplicitního záznamu
            for existing_entry in data[category]:
                if (existing_entry.get('type') == entry.get('type') and
                    abs(float(existing_entry.get('amount', 0)) - float(entry.get('amount', 0))) < 0.01 and
                    existing_entry.get('timestamp') == entry.get('timestamp')):
                    return True  # Duplicitní záznam, vrátíme True bez přidání
            
            # Přidání nového záznamu
            data[category].append(entry)
            return self.save_data(username, data)
            
        except Exception as e:
            print(f"Chyba při přidávání záznamu: {e}")
            return False

    def load_expenses(self, username: str) -> list:
        """Načte výdaje uživatele"""
        data = self.load_data(username)
        expenses = []
        for category, entries in data.items():
            if isinstance(entries, list):
                for entry in entries:
                    if entry.get('type') == 'Výdaj':
                        expenses.append({
                            'category': category,
                            'amount': entry.get('amount', 0),
                            'timestamp': entry.get('timestamp', ''),
                            'note': entry.get('note', '')
                        })
        return expenses

    def create_backup(self, username: str) -> str:
        """Vytvoří zálohu dat uživatele"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = get_backup_file(username, timestamp)
        
        # Záloha výdajů
        expenses_file = get_user_expenses_file(username)
        if os.path.exists(expenses_file):
            shutil.copy2(expenses_file, f"{backup_file}_expenses.json")
        
        # Záloha investic
        investments_file = get_user_investments_file(username)
        if os.path.exists(investments_file):
            shutil.copy2(investments_file, f"{backup_file}_investments.json")
        
        return backup_file

    def restore_backup(self, username: str, timestamp: str) -> bool:
        """Obnoví data ze zálohy"""
        backup_expenses = get_backup_file(username, timestamp) + "_expenses.json"
        backup_investments = get_backup_file(username, timestamp) + "_investments.json"
        
        success = True
        if os.path.exists(backup_expenses):
            shutil.copy2(backup_expenses, get_user_expenses_file(username))
        else:
            success = False
        
        if os.path.exists(backup_investments):
            shutil.copy2(backup_investments, get_user_investments_file(username))
        else:
            success = False
        
        return success

    def load_investments(self, username: str) -> List[Dict]:
        """Načte investice uživatele"""
        file_path = get_user_investments_file(username)
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Chyba při načítání investic: {e}")
            # Pokus o obnovení ze zálohy
            self._restore_latest_backup(username, "investments")
        return []

    def save_investments(self, username: str, investments: List[Dict]) -> bool:
        """Uloží investice uživatele"""
        try:
            # Nejprve vytvoříme zálohu
            self.create_backup(username)
            
            # Pak uložíme nová data
            file_path = get_user_investments_file(username)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(investments, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Chyba při ukládání investic: {e}")
            return False

    def _restore_latest_backup(self, username: str, data_type: str) -> Optional[str]:
        """Pokusí se obnovit nejnovější zálohu daného typu dat"""
        pattern = f"{username}_*_{data_type}.json"
        backups = []
        for file in os.listdir(BACKUP_DIR):
            if file.startswith(username) and file.endswith(f"_{data_type}.json"):
                backups.append(file)
        
        if not backups:
            return None
        
        # Seřadíme zálohy podle času vytvoření (nejnovější první)
        latest_backup = sorted(backups, reverse=True)[0]
        timestamp = latest_backup.split('_')[1]
        
        return self.restore_backup(username, timestamp)

    def get_available_backups(self, username: str) -> List[str]:
        """Vrátí seznam dostupných záloh pro uživatele"""
        backups = []
        for file in os.listdir(BACKUP_DIR):
            if file.startswith(username) and file.endswith(".json"):
                timestamp = file.split('_')[1]
                if timestamp not in backups:
                    backups.append(timestamp)
        return sorted(backups, reverse=True) 
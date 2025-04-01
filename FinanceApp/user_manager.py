import json
import os
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from typing import Dict, Optional, Tuple
from config import USER_DATA_DIR

class UserManager:
    def __init__(self):
        """Inicializace správce uživatelů"""
        self.users_file = os.path.join(USER_DATA_DIR, "users.json")
        self.ensure_users_file()

    def ensure_users_file(self):
        """Zajistí existenci souboru s uživateli"""
        os.makedirs(USER_DATA_DIR, exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def load_users(self) -> Dict:
        """Načte data uživatelů"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def save_users(self, users: Dict):
        """Uloží data uživatelů"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """Registrace nového uživatele"""
        users = self.load_users()
        
        if username in users:
            return False, "Uživatel s tímto jménem již existuje"
        
        # Hashování hesla
        hashed_password = pbkdf2_sha256.hash(password)
        
        # Uložení nového uživatele
        users[username] = {
            "password": hashed_password,
            "created_at": str(datetime.now())
        }
        self.save_users(users)
        
        return True, "Registrace proběhla úspěšně"

    def verify_password(self, username: str, password: str) -> bool:
        """Ověření hesla uživatele"""
        users = self.load_users()
        
        if username not in users:
            return False
        
        stored_password = users[username]["password"]
        return pbkdf2_sha256.verify(password, stored_password)

    def get_user(self, username: str) -> Optional[Dict]:
        """Získání dat uživatele"""
        users = self.load_users()
        return users.get(username) 
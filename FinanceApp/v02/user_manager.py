import os
import json
from datetime import datetime, timedelta
import streamlit as st
import extra_streamlit_components as stx
from passlib.hash import pbkdf2_sha256
from typing import Dict, Optional, Tuple
from config import USER_DATA_DIR

# Inicializace správce uživatelů jako globální instance
user_manager = None
cookie_manager = None

def get_cookie_manager():
    """Získá instanci CookieManager"""
    global cookie_manager
    if cookie_manager is None:
        cookie_manager = stx.CookieManager(key="finance_app_cookies")
    return cookie_manager

def get_user_manager():
    """Získá instanci správce uživatelů"""
    global user_manager
    if user_manager is None:
        user_manager = UserManager()
    return user_manager

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

    def register_user(self, username: str, password: str, email: str = None) -> Tuple[bool, str]:
        """Registrace nového uživatele"""
        # Validace vstupů
        if not username or not password:
            return False, "Uživatelské jméno a heslo nesmí být prázdné"

        users = self.load_users()
        
        if username in users:
            return False, "Uživatel s tímto jménem již existuje"
        
        # Kontrola duplicitního emailu
        if email and self.is_email_registered(email):
            return False, "Email je již registrován"
        
        # Hashování hesla
        hashed_password = pbkdf2_sha256.hash(password)
        
        # Uložení nového uživatele
        users[username] = {
            "username": username,  # Přidáno pro kompatibilitu s testy
            "password": hashed_password,
            "email": email,
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
        try:
            return pbkdf2_sha256.verify(password, stored_password)
        except:
            return False

    def get_user(self, username: str) -> Optional[Dict]:
        """Získání dat uživatele"""
        users = self.load_users()
        return users.get(username)

    def update_password(self, username: str, new_password: str) -> bool:
        """Aktualizace hesla uživatele"""
        users = self.load_users()
        if username not in users:
            return False
        
        users[username]["password"] = pbkdf2_sha256.hash(new_password)
        self.save_users(users)
        return True

    def is_email_registered(self, email: str) -> bool:
        """Kontrola, zda je email již registrován"""
        users = self.load_users()
        return any(user.get("email") == email for user in users.values())

    def update_user_data(self, username: str, update_data: Dict) -> bool:
        """Aktualizuje data uživatele"""
        users = self.load_users()
        if username not in users:
            return False
        
        # Aktualizace dat
        users[username].update(update_data)
        
        # Pokud se aktualizuje heslo, zahashujeme ho
        if "password" in update_data:
            users[username]["password"] = pbkdf2_sha256.hash(update_data["password"])
        
        self.save_users(users)
        return True

# Funkce pro práci s cookies
def create_session_cookie(username: str, expiry_days: int = 30):
    """Vytvoří session cookie"""
    cookie_manager = get_cookie_manager()
    cookie_manager.set("username", username, expires_at=datetime.now() + timedelta(days=expiry_days))

def get_session_cookie() -> Optional[str]:
    """Získá username z cookie"""
    cookie_manager = get_cookie_manager()
    return cookie_manager.get("username")

def clear_session_cookie():
    """Vymaže session cookie"""
    cookie_manager = get_cookie_manager()
    cookie_manager.delete("username")

# Funkce pro kompatibilitu se starým kódem
def create_user(username: str, password: str, email: str = None) -> bool:
    """Vytvoří nového uživatele"""
    success, _ = get_user_manager().register_user(username, password, email)
    return success

def verify_user(username: str, password: str) -> Tuple[bool, Optional[Dict]]:
    """Ověří přihlašovací údaje uživatele"""
    manager = get_user_manager()
    if manager.verify_password(username, password):
        return True, manager.get_user(username)
    return False, None

def get_user_data(username: str) -> Optional[Dict]:
    """Získá data uživatele"""
    return get_user_manager().get_user(username)

def update_user_password(username: str, new_password: str) -> bool:
    """Aktualizuje heslo uživatele"""
    return get_user_manager().update_password(username, new_password)

def get_user_file_path(username: str) -> str:
    """Získá cestu k souboru s daty uživatele"""
    return os.path.join(USER_DATA_DIR, f"{username}.json")

def is_email_registered(email: str) -> bool:
    """Kontrola, zda je email již registrován"""
    return get_user_manager().is_email_registered(email)

def update_user_data(username: str, update_data: Dict) -> bool:
    """Aktualizuje data uživatele"""
    return get_user_manager().update_user_data(username, update_data) 
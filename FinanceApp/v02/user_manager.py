import os
import json
from datetime import datetime, timedelta
import streamlit as st
import extra_streamlit_components as stx
from passlib.hash import pbkdf2_sha256
from typing import Dict, Optional, Tuple
import re
import html
import bleach
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
        self.max_file_size = 1024 * 1024  # 1MB limit pro soubor s uživateli
        self.allowed_tags = []  # Žádné HTML tagy nejsou povoleny
        self.allowed_attributes = {}  # Žádné HTML atributy nejsou povoleny
        self.blacklist_words = ["script", "alert", "javascript", "onerror", "onload"]

    def ensure_users_file(self):
        """Zajistí existenci souboru s uživateli"""
        os.makedirs(USER_DATA_DIR, exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            # Nastavení oprávnění pro soubor (čtení a zápis pro vlastníka)
            os.chmod(self.users_file, 0o600)

    def check_disk_space(self):
        """Kontrola dostupného místa na disku"""
        try:
            if os.path.exists(self.users_file):
                file_size = os.path.getsize(self.users_file)
                if file_size > self.max_file_size:
                    return False
            return True
        except:
            return False

    def sanitize_input(self, text: str) -> str:
        """Sanitizace vstupních dat proti XSS"""
        if not isinstance(text, str):
            return text
        # Použití bleach pro odstranění HTML tagů
        text = bleach.clean(text, tags=self.allowed_tags, attributes=self.allowed_attributes, strip=True)
        # Odstranění nebezpečných slov
        for word in self.blacklist_words:
            text = re.sub(rf'\b{word}\b', '', text, flags=re.IGNORECASE)
        # Escape speciálních znaků
        text = html.escape(text)
        return text

    def validate_email(self, email: str) -> bool:
        """Validace emailové adresy"""
        if not email:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_username(self, username: str) -> bool:
        """Validace uživatelského jména"""
        if not username:
            return False
        # Povolené znaky: písmena, číslice, podtržítko
        pattern = r'^[a-zA-Z0-9_]+$'
        return bool(re.match(pattern, username))

    def validate_password(self, password: str) -> bool:
        """Validace hesla"""
        if not password:
            return False
        # Heslo musí obsahovat alespoň jedno písmeno
        has_letter = any(c.isalpha() for c in password)
        # Heslo musí obsahovat alespoň jednu číslici
        has_digit = any(c.isdigit() for c in password)
        # Minimální délka je 6 znaků
        min_length = len(password) >= 6
        return min_length

    def load_users(self) -> Dict:
        """Načte data uživatelů"""
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def save_users(self, users: Dict):
        """Uloží data uživatelů"""
        if not self.check_disk_space():
            raise ValueError("Nedostatek místa na disku")
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        # Nastavení oprávnění pro soubor (čtení a zápis pro vlastníka)
        os.chmod(self.users_file, 0o600)

    def register_user(self, username: str, password: str, email: str = None) -> Tuple[bool, str]:
        """Registrace nového uživatele"""
        # Sanitizace vstupů
        username = self.sanitize_input(username)
        if email:
            email = self.sanitize_input(email)

        # Validace vstupů
        if not username or not password:
            return False, "Uživatelské jméno a heslo nesmí být prázdné"

        if not self.validate_username(username):
            return False, "Neplatné uživatelské jméno"

        if not self.validate_password(password):
            return False, "Heslo musí mít alespoň 6 znaků"

        if email and not self.validate_email(email):
            return False, "Neplatný formát emailu"

        if not self.check_disk_space():
            return False, "Nedostatek místa na disku"

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
            "username": username,
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
        if not self.check_disk_space():
            return False

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
        if not self.check_disk_space():
            return False

        users = self.load_users()
        if username not in users:
            return False
        
        # Sanitizace vstupních dat
        sanitized_data = {k: self.sanitize_input(v) if isinstance(v, str) else v 
                         for k, v in update_data.items()}
        
        # Aktualizace dat
        users[username].update(sanitized_data)
        
        # Pokud se aktualizuje heslo, zahashujeme ho
        if "password" in sanitized_data:
            users[username]["password"] = pbkdf2_sha256.hash(sanitized_data["password"])
        
        self.save_users(users)
        return True

# Funkce pro práci s cookies
def create_session_cookie(username: str, expiry_days: int = 30):
    """Vytvoří session cookie"""
    cookie_manager = get_cookie_manager()
    expiry = datetime.now() + timedelta(days=expiry_days)
    cookie_manager.set("username", username, expires_at=expiry)
    cookie_manager.set("username_expiry", expiry.isoformat(), expires_at=expiry)

def get_session_cookie() -> Optional[str]:
    """Získá username z cookie"""
    cookie_manager = get_cookie_manager()
    username = cookie_manager.get("username")
    if username:
        # Kontrola expirace cookie
        expiry_str = cookie_manager.get("username_expiry")
        if expiry_str:
            try:
                expiry = datetime.fromisoformat(expiry_str)
                if expiry < datetime.now():
                    clear_session_cookie()
                    return None
            except (ValueError, TypeError):
                clear_session_cookie()
                return None
    return username

def clear_session_cookie():
    """Vymaže session cookie"""
    cookie_manager = get_cookie_manager()
    try:
        cookie_manager.delete("username")
    except KeyError:
        pass
    try:
        cookie_manager.delete("username_expiry")
    except KeyError:
        pass

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

def update_user_password(username: str, new_password: str) -> bool:
    """Aktualizuje heslo uživatele"""
    return get_user_manager().update_password(username, new_password)

def get_user_file_path(username: str) -> str:
    """Získá cestu k souboru s daty uživatele"""
    return os.path.join(USER_DATA_DIR, f"{username}.json")

def is_email_registered(email: str) -> bool:
    """Kontrola, zda je email již registrován"""
    return get_user_manager().is_email_registered(email) 
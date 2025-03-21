import os
import json
import bcrypt
from datetime import datetime

# Konstanta pro adresář s daty uživatelů
USER_DATA_DIR = "data/users"
os.makedirs(USER_DATA_DIR, exist_ok=True)

def get_user_file_path(username):
    """Vrátí cestu k souboru s daty uživatele"""
    return os.path.join(USER_DATA_DIR, f"{username}.json")

def create_user(username, password, email, name):
    """Vytvoří nového uživatele"""
    user_file = get_user_file_path(username)
    
    if os.path.exists(user_file):
        return False, "Uživatel již existuje"
    
    # Hash hesla
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # Vytvoření uživatelských dat
    user_data = {
        "username": username,
        "password": hashed.decode(),
        "email": email,
        "name": name,
        "created_at": datetime.now().isoformat()
    }
    
    # Uložení dat
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)
    
    return True, "Uživatel byl úspěšně vytvořen"

def verify_user(username, password):
    """Ověří přihlašovací údaje uživatele"""
    user_file = get_user_file_path(username)
    
    if not os.path.exists(user_file):
        return False, None
    
    with open(user_file, "r", encoding="utf-8") as f:
        user_data = json.load(f)
    
    if bcrypt.checkpw(password.encode(), user_data["password"].encode()):
        return True, user_data
    
    return False, None

def get_user_data(username):
    """Získá data uživatele"""
    user_file = get_user_file_path(username)
    
    if not os.path.exists(user_file):
        return None
    
    with open(user_file, "r", encoding="utf-8") as f:
        return json.load(f)

def update_user_password(username, old_password, new_password):
    """Aktualizuje heslo uživatele"""
    success, user_data = verify_user(username, old_password)
    
    if not success:
        return False, "Nesprávné heslo"
    
    # Hash nového hesla
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    
    # Aktualizace hesla
    user_data["password"] = hashed.decode()
    
    # Uložení aktualizovaných dat
    user_file = get_user_file_path(username)
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=2)
    
    return True, "Heslo bylo úspěšně změněno" 
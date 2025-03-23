import os
import json
import bcrypt
from datetime import datetime

# Konstanta pro adresář s daty uživatelů
USER_DATA_DIR = os.path.join("data", "users")

# Vytvoření všech potřebných adresářů
os.makedirs("data", exist_ok=True)
os.makedirs(USER_DATA_DIR, exist_ok=True)

def get_user_file_path(username):
    """Vrátí cestu k souboru s daty uživatele"""
    return os.path.join(USER_DATA_DIR, f"{username}.json")

def create_user(username: str, password: str, email: str, name: str) -> bool:
    """Vytvoří nového uživatele"""
    try:
        # Kontrola existence uživatele
        if os.path.exists(get_user_file_path(username)):
            return False
        
        # Vytvoření adresáře pro uživatelská data, pokud neexistuje
        os.makedirs(os.path.dirname(get_user_file_path(username)), exist_ok=True)
        
        # Vytvoření uživatelských dat
        user_data = {
            "username": username,
            "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
            "email": email,
            "name": name,
            "created_at": datetime.now().isoformat()
        }
        
        # Uložení dat do souboru
        with open(get_user_file_path(username), 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Chyba při vytváření uživatele: {e}")
        return False

def verify_user(username, password):
    """Ověří přihlašovací údaje uživatele"""
    user_file = get_user_file_path(username)
    print(f"Checking user file: {user_file}")
    
    if not os.path.exists(user_file):
        print(f"User file does not exist: {user_file}")
        return False, None
    
    try:
        with open(user_file, "r", encoding="utf-8") as f:
            user_data = json.load(f)
            print(f"Loaded user data for: {user_data.get('username')}")
        
        if bcrypt.checkpw(password.encode(), user_data["password"].encode()):
            print("Password verification successful")
            return True, user_data
        else:
            print("Password verification failed")
            return False, None
    except Exception as e:
        print(f"Error during user verification: {e}")
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
import os
import json
import bcrypt
from datetime import datetime

def get_user_data_dir():
    """Vrátí cestu k adresáři s daty uživatelů"""
    user_data_dir = os.getenv("USER_DATA_DIR", os.path.join("data", "users"))
    os.makedirs(user_data_dir, exist_ok=True)
    return user_data_dir

def get_user_file_path(username):
    """Vrátí cestu k souboru s daty uživatele"""
    return os.path.join(get_user_data_dir(), f"{username}.json")

def is_email_registered(email: str) -> bool:
    """
    Zkontroluje, zda je e-mail již registrován.
    
    Args:
        email: E-mailová adresa k ověření
        
    Returns:
        bool: True pokud je e-mail již registrován, jinak False
    """
    try:
        # Procházení všech uživatelských souborů
        for filename in os.listdir(get_user_data_dir()):
            if filename.endswith('.json'):
                with open(os.path.join(get_user_data_dir(), filename), 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                    if user_data.get('email') == email:
                        return True
        return False
    except Exception as e:
        print(f"Chyba při kontrole e-mailu: {e}")
        return False

def create_user(username: str, password: str, email: str) -> bool:
    """
    Vytvoří nového uživatele.
    
    Args:
        username: Uživatelské jméno
        password: Heslo
        email: E-mailová adresa
        
    Returns:
        bool: True pokud se uživatel podařilo vytvořit, jinak False
    """
    try:
        print(f"Creating user in directory: {get_user_data_dir()}")
        user_file = get_user_file_path(username)
        print(f"User file path: {user_file}")
        
        # Kontrola existence uživatele
        if os.path.exists(user_file):
            print(f"User file already exists: {user_file}")
            return False
        
        # Kontrola, zda e-mail již není registrován
        if is_email_registered(email):
            print(f"Email already registered: {email}")
            return False
        
        # Hash hesla pomocí bcrypt
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        
        # Vytvoření dat uživatele
        user_data = {
            "username": username,
            "password": hashed_password,
            "email": email,
            "created_at": datetime.now().isoformat()
        }
        print(f"User data prepared: {user_data}")
        
        # Uložení dat uživatele
        with open(user_file, "w", encoding="utf-8") as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
        print(f"User data saved to: {user_file}")
        
        return True
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        print(f"Current directory: {os.getcwd()}")
        print(f"Directory contents: {os.listdir('.')}")
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

def update_user_data(username, update_data):
    """Aktualizuje data uživatele.
    
    Args:
        username (str): Uživatelské jméno
        update_data (dict): Slovník s daty k aktualizaci
        
    Returns:
        bool: True pokud se aktualizace povedla, jinak False
    """
    try:
        user_file = get_user_file_path(username)
        if not os.path.exists(user_file):
            return False
            
        with open(user_file, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
            
        # Aktualizace dat
        user_data.update(update_data)
        
        # Uložení aktualizovaných dat
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
            
        return True
    except Exception as e:
        print(f"Chyba při aktualizaci dat uživatele: {str(e)}")
        return False 
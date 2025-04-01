import os
from pathlib import Path

# Získání cesty k domovskému adresáři uživatele
HOME_DIR = str(Path.home())

# Vytvoření adresáře pro data aplikace v domovském adresáři
APP_DATA_DIR = os.path.join(HOME_DIR, '.finance_app_data')
USER_DATA_DIR = os.path.join(APP_DATA_DIR, 'users')
BACKUP_DIR = os.path.join(APP_DATA_DIR, 'backups')

# Vytvoření potřebných adresářů, pokud neexistují
os.makedirs(APP_DATA_DIR, exist_ok=True)
os.makedirs(USER_DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# Cesty k souborům
def get_user_expenses_file(username: str) -> str:
    """Vrátí cestu k souboru s výdaji uživatele"""
    return os.path.join(USER_DATA_DIR, f'{username}_expenses.json')

def get_user_investments_file(username: str) -> str:
    """Vrátí cestu k souboru s investicemi uživatele"""
    return os.path.join(USER_DATA_DIR, f'{username}_investments.json')

def get_backup_file(username: str, timestamp: str) -> str:
    """Vrátí cestu k záložnímu souboru"""
    return os.path.join(BACKUP_DIR, f'{username}_{timestamp}.json') 
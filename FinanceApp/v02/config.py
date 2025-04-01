import os
import sys

# Detekce, zda běžíme v testovacím prostředí
IS_TESTING = 'pytest' in sys.modules

# Získání cesty k adresáři aplikace
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# Konfigurace cest k datům
if IS_TESTING:
    # Pro testy používáme dočasný adresář
    DATA_DIR = os.path.join(APP_DIR, "test_data")
    USER_DATA_DIR = os.path.join(DATA_DIR, "users")
else:
    # Pro produkci používáme normální adresář
    DATA_DIR = os.path.join(APP_DIR, "data")
    USER_DATA_DIR = os.path.join(DATA_DIR, "users")

DATA_FILE = os.path.join(DATA_DIR, "finance_data.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history_data.json")

# Vytvoření potřebných adresářů
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(USER_DATA_DIR, exist_ok=True)

DEFAULT_CATEGORIES = [
    "investments", "real_estate", "retirement_savings",
    "cryptocurrency", "mintos", "xtb_etf", "pension_savings_csob", "portu_majda",
    "deposit_flat", "portu_etf", "amundi_majda", "xtb_majda", "land_majda",
    "fiat_czk", "csob_medium", "insurance"
]
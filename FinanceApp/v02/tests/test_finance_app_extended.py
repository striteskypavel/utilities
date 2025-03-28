import unittest
import os
import json
import pandas as pd
from datetime import datetime, timedelta
import tempfile
import shutil
import bcrypt

# Vytvoření dočasného adresáře pro test
TEST_DIR = tempfile.mkdtemp()
USERS_DIR = os.path.join(TEST_DIR, "users")
os.makedirs(USERS_DIR, exist_ok=True)

# Nastavení proměnných prostředí pro test
os.environ["DATA_DIR"] = TEST_DIR
os.environ["USER_DATA_DIR"] = USERS_DIR

# Přidání cesty k modulům aplikace
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_manager import create_user, verify_user, get_user_data, update_user_data
from data_manager import load_data, save_data, add_entry, get_history

class TestFinanceAppExtended(unittest.TestCase):
    def setUp(self):
        """Nastavení před každým testem"""
        self.test_username = "test_user"
        self.test_password = "Test123!"
        self.test_email = "test@example.com"
        
        # Nastavení cest k testovacím datům
        self.test_dir = TEST_DIR
        self.users_dir = USERS_DIR
        self.data_file = os.path.join(self.test_dir, f"{self.test_username}_data.json")
        self.history_file = os.path.join(self.test_dir, f"{self.test_username}_history.json")
        self.user_file = os.path.join(self.users_dir, f"{self.test_username}.json")
        
        # Smazání existujících souborů
        for file in [self.data_file, self.history_file, self.user_file]:
            if os.path.exists(file):
                os.remove(file)

    @classmethod
    def tearDownClass(cls):
        """Úklid po všech testech"""
        shutil.rmtree(TEST_DIR)

    def test_user_data_update(self):
        """Test aktualizace dat uživatele"""
        # Vytvoření uživatele
        create_user(self.test_username, self.test_password, self.test_email)
        
        # Aktualizace emailu
        new_email = "new@example.com"
        success = update_user_data(self.test_username, {"email": new_email})
        self.assertTrue(success)
        
        # Ověření změny
        user_data = get_user_data(self.test_username)
        self.assertEqual(user_data["email"], new_email)

    def test_password_change(self):
        """Test změny hesla"""
        # Vytvoření uživatele
        create_user(self.test_username, self.test_password, self.test_email)
        
        # Změna hesla
        new_password = "NewTest123!"
        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        success = update_user_data(self.test_username, {"password": hashed})
        self.assertTrue(success)
        
        # Ověření nového hesla
        success, _ = verify_user(self.test_username, new_password)
        self.assertTrue(success)

    def test_data_validation(self):
        """Test validace dat"""
        # Vytvoření uživatele a prázdných dat
        create_user(self.test_username, self.test_password, self.test_email)
        save_data(self.test_username, {})
        
        # Test přidání validních dat
        success = add_entry(self.test_username, "Test", 1000)
        self.assertTrue(success)
        
        data = load_data(self.test_username)
        self.assertIn("Test", data)
        self.assertEqual(data["Test"][0]["amount"], 1000)

    def test_expense_tracking(self):
        """Test sledování výdajů"""
        # Vytvoření uživatele a prázdných dat
        create_user(self.test_username, self.test_password, self.test_email)
        save_data(self.test_username, {})
        
        # Přidání testovacích výdajů
        categories = ["Bydlení", "Jídlo", "Doprava"]
        amounts = [5000, 3000, 2000]
        
        for category, amount in zip(categories, amounts):
            add_entry(self.test_username, category, amount)
        
        # Načtení dat
        data = load_data(self.test_username)
        
        # Ověření kategorizace
        for category in categories:
            self.assertIn(category, data)
            self.assertEqual(len(data[category]), 1)
            self.assertEqual(data[category][0]["amount"], amounts[categories.index(category)])

    def test_investment_overview(self):
        """Test přehledu investic"""
        # Vytvoření uživatele
        create_user(self.test_username, self.test_password, self.test_email)
        
        # Přidání testovacích investic
        investments = {
            "TestAkcie": 100000,
            "TestETF": 50000,
            "TestKrypto": 30000
        }
        
        for category, amount in investments.items():
            add_entry(self.test_username, category, amount)
        
        # Načtení dat
        data = load_data(self.test_username)
        
        # Ověření struktury dat pro testovací kategorie
        for category in investments:
            self.assertIn(category, data)
            self.assertEqual(len(data[category]), 1)
            self.assertEqual(data[category][0]["amount"], investments[category])

    def test_data_persistence(self):
        """Test perzistence dat"""
        # Vytvoření uživatele
        create_user(self.test_username, self.test_password, self.test_email)
        
        # Přidání testovacích dat
        test_data = {
            "TestKat1": [{"amount": 1000, "timestamp": datetime.now().isoformat()}],
            "TestKat2": [{"amount": 2000, "timestamp": datetime.now().isoformat()}]
        }
        
        # Uložení dat
        save_data(self.test_username, test_data)
        
        # Načtení dat
        loaded_data = load_data(self.test_username)
        
        # Ověření shody pro testovací kategorie
        for category in test_data:
            self.assertIn(category, loaded_data)
            self.assertEqual(len(loaded_data[category]), len(test_data[category]))
            self.assertEqual(loaded_data[category][0]["amount"], test_data[category][0]["amount"])

    def test_date_filtering(self):
        """Test filtrování podle data"""
        # Vytvoření uživatele a prázdných dat
        create_user(self.test_username, self.test_password, self.test_email)
        save_data(self.test_username, {})
        
        # Přidání testovacích dat s různými daty
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        add_entry(self.test_username, "Test1", {
            "amount": 1000,
            "timestamp": today.isoformat(),
            "note": ""
        })
        add_entry(self.test_username, "Test2", {
            "amount": 2000,
            "timestamp": yesterday.isoformat(),
            "note": ""
        })
        
        # Načtení dat
        data = load_data(self.test_username)
        
        # Ověření správného uložení dat
        self.assertEqual(len(data["Test1"]), 1)
        self.assertEqual(len(data["Test2"]), 1)
        self.assertEqual(data["Test1"][0]["amount"], 1000)
        self.assertEqual(data["Test2"][0]["amount"], 2000)

if __name__ == '__main__':
    unittest.main() 
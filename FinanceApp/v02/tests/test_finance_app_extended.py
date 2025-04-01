import unittest
import os
import json
import pandas as pd
from datetime import datetime, timedelta
import tempfile
import shutil
import bcrypt
from user_manager import create_user, verify_user, get_user_data, update_user_data, update_user_password
from config import USER_DATA_DIR

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

from data_manager import load_data, save_data, add_entry, get_history

class TestFinanceAppExtended(unittest.TestCase):
    def setUp(self):
        """Příprava testovacího prostředí"""
        self.test_username = "test_user"
        self.test_password = "test_password"
        self.test_email = "test@example.com"
        
        # Vytvoření testovacího uživatele
        create_user(self.test_username, self.test_password, self.test_email)

    def tearDown(self):
        """Vyčištění testovacího prostředí"""
        # Smazání testovacího uživatele
        users_file = os.path.join(USER_DATA_DIR, "users.json")
        if os.path.exists(users_file):
            with open(users_file, 'r', encoding='utf-8') as f:
                users = json.load(f)
            if self.test_username in users:
                del users[self.test_username]
                with open(users_file, 'w', encoding='utf-8') as f:
                    json.dump(users, f, ensure_ascii=False, indent=2)

    def test_user_registration_validation(self):
        """Test validace registrace uživatele"""
        # Test 1: Prázdné jméno
        success = create_user("", self.test_password, self.test_email)
        self.assertFalse(success)
        
        # Test 2: Prázdné heslo
        success = create_user("test_user2", "", self.test_email)
        self.assertFalse(success)
        
        # Test 3: Duplicitní email
        success = create_user("test_user2", self.test_password, self.test_email)
        self.assertFalse(success)

    def test_password_change(self):
        """Test změny hesla"""
        # Vytvoření uživatele
        create_user(self.test_username, self.test_password, self.test_email)
        
        # Změna hesla
        new_password = "NewTest123!"
        success = update_user_password(self.test_username, new_password)
        self.assertTrue(success)
        
        # Ověření nového hesla
        success, _ = verify_user(self.test_username, new_password)
        self.assertTrue(success)
        
        # Ověření starého hesla (nemělo by fungovat)
        success, _ = verify_user(self.test_username, self.test_password)
        self.assertFalse(success)

    def test_user_data_update(self):
        """Test aktualizace dat uživatele"""
        # Aktualizace emailu
        new_email = "new@example.com"
        success = update_user_data(self.test_username, {"email": new_email})
        self.assertTrue(success)
        
        # Ověření změny
        user_data = get_user_data(self.test_username)
        self.assertEqual(user_data["email"], new_email)
        
        # Aktualizace neexistujícího uživatele
        success = update_user_data("nonexistent_user", {"email": new_email})
        self.assertFalse(success)

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
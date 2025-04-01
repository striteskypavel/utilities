import unittest
import os
import json
from datetime import datetime
import sys

# Přidání cesty k testovaným modulům
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_manager import load_data, save_data, add_entry
from user_manager import create_user, verify_user, get_user_data, update_user_data
from history_manager import log_change, load_history, clear_history
from config import USER_DATA_DIR

class TestFinanceApp(unittest.TestCase):
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

    def test_user_creation_and_verification(self):
        """Test vytvoření a ověření uživatele"""
        # Ověření přihlášení
        success, user_data = verify_user(self.test_username, self.test_password)
        self.assertTrue(success)
        self.assertIsNotNone(user_data)
        self.assertIn("email", user_data)
        self.assertEqual(user_data["email"], self.test_email)

    def test_user_data_storage(self):
        """Test ukládání dat uživatele"""
        # Získání dat uživatele
        user_data = get_user_data(self.test_username)
        self.assertIsNotNone(user_data)
        self.assertIn("email", user_data)
        self.assertEqual(user_data["email"], self.test_email)

    def test_user_update(self):
        """Test aktualizace dat uživatele"""
        # Aktualizace emailu
        new_email = "new@example.com"
        success = update_user_data(self.test_username, {"email": new_email})
        self.assertTrue(success)
        
        # Ověření změny
        user_data = get_user_data(self.test_username)
        self.assertEqual(user_data["email"], new_email)

    def test_data_management(self):
        """Test správy dat"""
        # Přidání záznamu
        entry_data = {
            "type": "Výdaj",
            "amount": 1000,
            "timestamp": datetime.now().isoformat()
        }
        add_entry(self.test_username, "Test Category", entry_data)
        
        # Načtení dat
        data = load_data(self.test_username)
        self.assertIn("Test Category", data)
        
        # Kontrola, zda je kategorie seznam nebo jednotlivý záznam
        category_data = data["Test Category"]
        if isinstance(category_data, list):
            self.assertEqual(category_data[0]["amount"], 1000)
        else:
            self.assertEqual(category_data["amount"], 1000)
    
    def test_history_management(self):
        """Test správy historie"""
        # Přidání záznamu do historie
        log_change("Test Category", 0, 1000)
        
        # Načtení historie
        history = load_history()
        self.assertGreater(len(history), 0)
        
        # Vymazání historie
        clear_history()
        history = load_history()
        self.assertEqual(len(history), 0)

if __name__ == '__main__':
    unittest.main() 
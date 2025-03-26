import unittest
import pandas as pd
from datetime import datetime
import sys
import os

# Přidání cesty k testovaným modulům
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_manager import load_data, save_data, add_entry
from user_manager import create_user, verify_user, get_user_data
from history_manager import log_change, load_history, clear_history

class TestFinanceApp(unittest.TestCase):
    def setUp(self):
        """Nastavení před každým testem"""
        self.test_username = "test_user"
        self.test_password = "Test123!"
        self.test_email = "test@example.com"
        
        # Vytvoření testovacího uživatele
        create_user(self.test_username, self.test_password, self.test_email)
    
    def tearDown(self):
        """Úklid po každém testu"""
        # Smazání testovacích souborů
        user_file = f"data/users/{self.test_username}.json"
        if os.path.exists(user_file):
            os.remove(user_file)
    
    def test_user_creation_and_verification(self):
        """Test vytvoření a ověření uživatele"""
        # Ověření přihlášení
        success, user_data = verify_user(self.test_username, self.test_password)
        self.assertTrue(success)
        self.assertEqual(user_data["username"], self.test_username)
        self.assertEqual(user_data["email"], self.test_email)
    
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
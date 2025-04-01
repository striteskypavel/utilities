import unittest
import sys
import os
from datetime import datetime
import json
import tempfile
import pandas as pd
from werkzeug.security import generate_password_hash

# Přidání cesty k aplikaci do PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'v02')))

from data_manager import DataManager

class TestFinanceAppExtended(unittest.TestCase):
    def setUp(self):
        """Nastavení před každým testem"""
        self.test_username = "test_user"
        self.test_password = "Test123!"
        self.test_email = "test@example.com"
        self.data_manager = DataManager()
        
        # Vytvoření testovacího uživatele
        self.data_manager.create_user(
            self.test_username,
            generate_password_hash(self.test_password),
            self.test_email
        )

    def tearDown(self):
        """Úklid po každém testu"""
        # Smazání testovacích dat
        user_file = self.data_manager.get_user_file_path(self.test_username)
        if os.path.exists(user_file):
            os.remove(user_file)
        
        investments_file = os.path.join('data', f'{self.test_username}_investments.json')
        if os.path.exists(investments_file):
            os.remove(investments_file)
        
        expenses_file = os.path.join('data', f'{self.test_username}_expenses.json')
        if os.path.exists(expenses_file):
            os.remove(expenses_file)

    def test_add_single_entry(self):
        """Test přidání jednoho záznamu"""
        # Vyčištění dat
        self.data_manager.save_data(self.test_username, {})
        
        # Přidání záznamu
        success = self.data_manager.add_entry(self.test_username, "Test", {"amount": 1000, "timestamp": datetime.now().isoformat()})
        self.assertTrue(success)
        
        # Ověření dat
        data = self.data_manager.load_data(self.test_username)
        self.assertIn("Test", data)
        self.assertEqual(data["Test"][0]["amount"], 1000)

    def test_add_multiple_entries(self):
        """Test přidání více záznamů"""
        # Vyčištění dat
        self.data_manager.save_data(self.test_username, {})
        
        # Přidání záznamů
        categories = ["Test1", "Test2", "Test3"]
        amounts = [1000, 2000, 3000]
        
        for category, amount in zip(categories, amounts):
            self.data_manager.add_entry(self.test_username, category, {"amount": amount, "timestamp": datetime.now().isoformat()})
        
        # Ověření dat
        data = self.data_manager.load_data(self.test_username)
        for category, amount in zip(categories, amounts):
            self.assertIn(category, data)
            self.assertEqual(data[category][0]["amount"], amount)

    def test_add_entries_same_category(self):
        """Test přidání více záznamů do stejné kategorie"""
        # Vyčištění dat
        self.data_manager.save_data(self.test_username, {})
        
        # Přidání záznamů
        category = "Test"
        amounts = [1000, 2000, 3000]
        
        for amount in amounts:
            self.data_manager.add_entry(self.test_username, category, {"amount": amount, "timestamp": datetime.now().isoformat()})
        
        # Ověření dat
        data = self.data_manager.load_data(self.test_username)
        self.assertIn(category, data)
        self.assertEqual(len(data[category]), len(amounts))
        for entry, amount in zip(data[category], amounts):
            self.assertEqual(entry["amount"], amount)

    def test_data_persistence(self):
        """Test perzistence dat"""
        # Vytvoření testovacích dat
        test_data = {
            "Test1": [{"amount": 1000, "timestamp": datetime.now().isoformat()}],
            "Test2": [{"amount": 2000, "timestamp": datetime.now().isoformat()}]
        }
        
        # Uložení dat
        self.data_manager.save_data(self.test_username, test_data)
        
        # Načtení dat a ověření
        loaded_data = self.data_manager.load_data(self.test_username)
        
        # Ověření struktury dat
        self.assertIn("Test1", loaded_data)
        self.assertIn("Test2", loaded_data)
        self.assertEqual(len(loaded_data["Test1"]), 1)
        self.assertEqual(len(loaded_data["Test2"]), 1)
        self.assertEqual(loaded_data["Test1"][0]["amount"], test_data["Test1"][0]["amount"])
        self.assertEqual(loaded_data["Test2"][0]["amount"], test_data["Test2"][0]["amount"])

    def test_complex_data_operations(self):
        """Test komplexních operací s daty"""
        # Vyčištění dat
        self.data_manager.save_data(self.test_username, {})
        
        # Přidání komplexních záznamů
        self.data_manager.add_entry(self.test_username, "Test1", {
            "amount": 1000,
            "timestamp": datetime.now().isoformat(),
            "type": "Výdaj",
            "note": "Test note 1"
        })
        
        self.data_manager.add_entry(self.test_username, "Test2", {
            "amount": 2000,
            "timestamp": datetime.now().isoformat(),
            "type": "Příjem",
            "note": "Test note 2"
        })
        
        # Ověření dat
        data = self.data_manager.load_data(self.test_username)
        self.assertIn("Test1", data)
        self.assertIn("Test2", data)
        self.assertEqual(data["Test1"][0]["type"], "Výdaj")
        self.assertEqual(data["Test2"][0]["type"], "Příjem")

if __name__ == '__main__':
    unittest.main() 
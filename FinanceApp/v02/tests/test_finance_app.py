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

class TestFinanceApp(unittest.TestCase):
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

    def test_csv_import_export(self):
        """Test importu a exportu CSV dat"""
        # Vytvoření testovacího CSV souboru
        csv_data = "Kategorie,Částka,Datum,Poznámka\nTest1,1000,2024-01-01,Test note 1\nTest2,2000,2024-01-02,Test note 2"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(csv_data)
            csv_file = f.name
        
        # Test importu CSV
        success = self.data_manager.import_data(self.test_username, csv_file, format="csv")
        self.assertTrue(success)
        
        # Ověření importovaných dat
        data = self.data_manager.load_data(self.test_username)
        self.assertIn("Test1", data)
        self.assertIn("Test2", data)
        
        # Vyčištění
        os.unlink(csv_file)

    def test_json_import_export(self):
        """Test importu a exportu JSON dat"""
        # Vytvoření testovacího JSON souboru
        json_data = {
            "Test1": [{"amount": 1000, "timestamp": "2024-01-01T00:00:00", "note": "Test note 1"}],
            "Test2": [{"amount": 2000, "timestamp": "2024-01-02T00:00:00", "note": "Test note 2"}]
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(json_data, f)
            json_file = f.name
        
        # Test importu JSON
        success = self.data_manager.import_data(self.test_username, json_file, format="json")
        self.assertTrue(success)
        
        # Ověření importovaných dat
        data = self.data_manager.load_data(self.test_username)
        self.assertIn("Test1", data)
        self.assertIn("Test2", data)
        
        # Vyčištění
        os.unlink(json_file)

    def test_data_operations(self):
        """Test operací s daty"""
        # Uložení původních dat
        original_data = self.data_manager.load_data(self.test_username)
        
        # Přidání testovacích záznamů
        self.data_manager.add_entry(self.test_username, "Test1", {"amount": 1000, "timestamp": datetime.now().isoformat()})
        self.data_manager.add_entry(self.test_username, "Test2", {"amount": 2000, "timestamp": datetime.now().isoformat()})
        
        # Export do CSV
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            csv_file = f.name
        success = self.data_manager.export_data(self.test_username, csv_file, format="csv")
        self.assertTrue(success)
        self.assertTrue(os.path.exists(csv_file))
        
        # Ověření CSV souboru
        df = pd.read_csv(csv_file)
        self.assertGreater(len(df), 0)
        
        # Vyčištění
        os.unlink(csv_file)
        
        # Export do JSON
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            json_file = f.name
        
        # Přidání testovacích záznamů
        self.data_manager.add_entry(self.test_username, "Test1", {"amount": 1000, "timestamp": datetime.now().isoformat()})
        self.data_manager.add_entry(self.test_username, "Test2", {"amount": 2000, "timestamp": datetime.now().isoformat()})
        
        success = self.data_manager.export_data(self.test_username, json_file, format="json")
        self.assertTrue(success)
        self.assertTrue(os.path.exists(json_file))
        
        # Ověření JSON souboru
        with open(json_file, 'r') as f:
            exported_data = json.load(f)
        self.assertGreater(len(exported_data), 0)
        
        # Vyčištění
        os.unlink(json_file)

    def test_history_operations(self):
        """Test operací s historií"""
        # Vyčištění dat
        self.data_manager.save_data(self.test_username, {})
        
        # Přidání testovacích záznamů
        self.data_manager.add_entry(self.test_username, "Test1", {"amount": 1000, "timestamp": datetime.now().isoformat()})
        self.data_manager.add_entry(self.test_username, "Test1", {"amount": 2000, "timestamp": datetime.now().isoformat()})
        
        # Načtení dat a ověření historie
        data = self.data_manager.load_data(self.test_username)
        self.assertIn("Test1", data)
        self.assertGreater(len(data["Test1"]), 0)
        self.assertEqual(len(data["Test1"]), 2)  # Ověření počtu záznamů

    def test_data_consistency(self):
        """Test konzistence dat"""
        # Uložení původních dat
        original_data = self.data_manager.load_data(self.test_username)
        
        # Přidání testovacího záznamu
        self.data_manager.add_entry(self.test_username, "Test1", {"amount": 1000, "timestamp": datetime.now().isoformat()})
        
        # Načtení aktualizovaných dat
        data = self.data_manager.load_data(self.test_username)
        self.assertIn("Test1", data)

if __name__ == '__main__':
    unittest.main() 
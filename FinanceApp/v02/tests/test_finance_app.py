import unittest
import os
import json
import pandas as pd
from datetime import datetime
import tempfile
import shutil

# Přidání cesty k modulům aplikace
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user_manager import create_user, verify_user, get_user_data, get_user_file_path
from data_manager import (
    load_data, save_data, add_entry, export_data, import_data,
    get_history, clear_history
)
from App import show_main_app

class TestFinanceApp(unittest.TestCase):
    def setUp(self):
        """Nastavení před každým testem"""
        self.test_username = "test_user"
        self.test_password = "Test123!"
        self.test_email = "test@example.com"
        
        # Vytvoření dočasného adresáře pro test
        self.test_dir = tempfile.mkdtemp()
        
        # Vytvoření adresáře pro uživatele
        self.users_dir = os.path.join(self.test_dir, "users")
        os.makedirs(self.users_dir, exist_ok=True)
        
        # Nastavení cest k testovacím datům
        self.data_file = os.path.join(self.test_dir, f"{self.test_username}_data.json")
        self.history_file = os.path.join(self.test_dir, f"{self.test_username}_history.json")
        self.user_file = os.path.join(self.users_dir, f"{self.test_username}.json")
        
        # Nastavení proměnných prostředí pro test
        os.environ["DATA_DIR"] = self.test_dir
        os.environ["USER_DATA_DIR"] = self.users_dir

    def tearDown(self):
        """Úklid po každém testu"""
        # Smazání dočasného adresáře
        shutil.rmtree(self.test_dir)

    def test_user_registration(self):
        """Test registrace nového uživatele"""
        # Registrace nového uživatele
        success = create_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.user_file))
        
        # Ověření dat uživatele
        user_data = get_user_data(self.test_username)
        self.assertEqual(user_data["username"], self.test_username)
        self.assertEqual(user_data["email"], self.test_email)
        self.assertTrue("created_at" in user_data)

    def test_user_login(self):
        """Test přihlášení nového uživatele"""
        # Nejprve vytvoříme uživatele
        create_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        
        # Ověření přihlášení
        success, user_data = verify_user(self.test_username, self.test_password)
        self.assertTrue(success)
        self.assertEqual(user_data["username"], self.test_username)
        self.assertEqual(user_data["email"], self.test_email)

    def test_page_navigation(self):
        """Test zobrazení všech stránek"""
        # Vytvoření a přihlášení uživatele
        create_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        
        success, user_data = verify_user(self.test_username, self.test_password)
        self.assertTrue(success)

    def test_csv_import(self):
        """Test importu dat z CSV"""
        # Vytvoření testovacího CSV souboru
        test_data = pd.DataFrame({
            'Kategorie': ['Test1', 'Test2'],
            'Částka': [1000, 2000],
            'Datum': [datetime.now().isoformat(), datetime.now().isoformat()],
            'Poznámka': ['Note1', 'Note2']
        })
        
        csv_file = os.path.join(self.test_dir, "test_import.csv")
        test_data.to_csv(csv_file, index=False)
        
        # Import dat
        success = import_data(self.test_username, csv_file, format="csv")
        self.assertTrue(success)
        
        # Ověření importovaných dat
        data = load_data(self.test_username)
        self.assertIn("Test1", data)
        self.assertIn("Test2", data)
        self.assertEqual(len(data["Test1"]), 1)
        self.assertEqual(len(data["Test2"]), 1)
        self.assertEqual(data["Test1"][0]["amount"], 1000)
        self.assertEqual(data["Test2"][0]["amount"], 2000)

    def test_json_import(self):
        """Test importu dat z JSON"""
        # Vytvoření testovacího JSON souboru
        test_data = {
            "Test1": [{
                "amount": 1000,
                "timestamp": datetime.now().isoformat(),
                "note": "Note1"
            }],
            "Test2": [{
                "amount": 2000,
                "timestamp": datetime.now().isoformat(),
                "note": "Note2"
            }]
        }
        
        json_file = os.path.join(self.test_dir, "test_import.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Import dat
        success = import_data(self.test_username, json_file, format="json")
        self.assertTrue(success)
        
        # Ověření importovaných dat
        data = load_data(self.test_username)
        self.assertIn("Test1", data)
        self.assertIn("Test2", data)
        self.assertEqual(len(data["Test1"]), 1)
        self.assertEqual(len(data["Test2"]), 1)
        self.assertEqual(data["Test1"][0]["amount"], 1000)
        self.assertEqual(data["Test2"][0]["amount"], 2000)

    def test_csv_export(self):
        """Test exportu dat do CSV"""
        # Přidání testovacích dat
        add_entry(self.test_username, "Test1", 1000)
        add_entry(self.test_username, "Test2", 2000)
        
        # Export dat
        csv_file = os.path.join(self.test_dir, "test_export.csv")
        success = export_data(self.test_username, csv_file, format="csv")
        self.assertTrue(success)
        self.assertTrue(os.path.exists(csv_file))
        
        # Ověření obsahu CSV souboru
        with open(csv_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)  # Hlavička + 2 záznamy
            self.assertTrue("Test1,1000" in lines[1] or "Test1,1000" in lines[2])
            self.assertTrue("Test2,2000" in lines[1] or "Test2,2000" in lines[2])
        
        # Úklid
        os.remove(csv_file)

    def test_json_export(self):
        """Test exportu dat do JSON"""
        # Přidání testovacích dat
        add_entry(self.test_username, "Test1", 1000)
        add_entry(self.test_username, "Test2", 2000)
        
        # Export dat
        json_file = os.path.join(self.test_dir, "test_export.json")
        success = export_data(self.test_username, json_file, format="json")
        self.assertTrue(success)
        
        # Ověření exportovaného souboru
        self.assertTrue(os.path.exists(json_file))
        with open(json_file, 'r', encoding='utf-8') as f:
            exported_data = json.load(f)
        self.assertIn("Test1", exported_data)
        self.assertIn("Test2", exported_data)

    def test_clear_history(self):
        """Test smazání historie"""
        # Přidání testovacích dat a historie
        add_entry(self.test_username, "Test1", 1000)
        add_entry(self.test_username, "Test1", 2000)
        
        # Smazání historie
        clear_history(self.test_username)
        
        # Ověření, že historie byla smazána
        history = get_history(self.test_username)
        self.assertEqual(len(history), 0)

    def test_add_new_entry(self):
        """Test přidání nové položky"""
        # Přidání nové položky
        add_entry(self.test_username, "Test1", 1000)
        
        # Ověření přidané položky
        data = load_data(self.test_username)
        self.assertIn("Test1", data)
        self.assertTrue(isinstance(data["Test1"], list))
        self.assertEqual(len(data["Test1"]), 1)
        self.assertEqual(data["Test1"][0]["amount"], 1000)

if __name__ == '__main__':
    unittest.main() 
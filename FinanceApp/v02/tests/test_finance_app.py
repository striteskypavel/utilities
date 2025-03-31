import unittest
import os
import json
import pandas as pd
from datetime import datetime
import tempfile
import shutil

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
        
        # Nastavení cest k testovacím datům
        self.test_dir = TEST_DIR
        self.users_dir = USERS_DIR
        self.data_file = os.path.join(self.test_dir, f"{self.test_username}_data.json")
        self.history_file = os.path.join(self.test_dir, f"{self.test_username}_history.json")
        self.user_file = os.path.join(self.users_dir, f"{self.test_username}.json")

    @classmethod
    def tearDownClass(cls):
        """Úklid po všech testech"""
        # Smazání dočasného adresáře
        shutil.rmtree(TEST_DIR)

    def test_user_registration(self):
        """Test registrace nového uživatele"""
        # Vytvoření unikátního uživatelského jména
        unique_username = f"test_user_{datetime.now().timestamp()}"
        unique_email = f"test_{datetime.now().timestamp()}@example.com"
        
        # Registrace nového uživatele
        success = create_user(
            unique_username,
            self.test_password,
            unique_email
        )
        
        self.assertTrue(success)
        
        # Získání cesty k souboru pomocí funkce z user_manager
        user_file = get_user_file_path(unique_username)
        self.assertTrue(os.path.exists(user_file))
        
        # Ověření dat uživatele
        user_data = get_user_data(unique_username)
        self.assertEqual(user_data["username"], unique_username)
        self.assertEqual(user_data["email"], unique_email)
        self.assertTrue("created_at" in user_data)
        
        # Úklid
        if os.path.exists(user_file):
            os.remove(user_file)

    def test_user_login(self):
        """Test přihlášení uživatele - různé scénáře"""
        # Test 1: Úspěšné přihlášení
        create_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        
        success, user_data = verify_user(self.test_username, self.test_password)
        self.assertTrue(success)
        self.assertEqual(user_data["username"], self.test_username)
        self.assertEqual(user_data["email"], self.test_email)
        
        # Test 2: Nesprávné heslo
        success, user_data = verify_user(self.test_username, "wrong_password")
        self.assertFalse(success)
        self.assertIsNone(user_data)
        
        # Test 3: Neexistující uživatel
        success, user_data = verify_user("nonexistent_user", self.test_password)
        self.assertFalse(success)
        self.assertIsNone(user_data)
        
        # Test 4: Prázdné přihlašovací údaje
        success, user_data = verify_user("", "")
        self.assertFalse(success)
        self.assertIsNone(user_data)
        
        # Test 5: Speciální znaky v hesle
        special_password = "Test123!@#$%^&*()"
        create_user(
            "special_user",
            special_password,
            "special@example.com"
        )
        success, user_data = verify_user("special_user", special_password)
        self.assertTrue(success)
        self.assertEqual(user_data["username"], "special_user")
        
        # Test 6: Citlivost na velikost písmen v hesle
        success, user_data = verify_user(self.test_username, self.test_password.upper())
        self.assertFalse(success)
        self.assertIsNone(user_data)

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
        # Načtení původních dat
        original_data = load_data(self.test_username)
        original_entries = sum(len(entries) if isinstance(entries, list) else 1 for entries in original_data.values())
        
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
            self.assertEqual(len(lines), original_entries + 3)  # Hlavička + původní záznamy + 2 nové záznamy
            self.assertTrue(any("Test1,1000" in line for line in lines))
            self.assertTrue(any("Test2,2000" in line for line in lines))
        
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
        # Načtení původních dat
        original_data = load_data(self.test_username)
        original_test1_count = len(original_data.get("Test1", []))
        
        # Přidání nové položky
        add_entry(self.test_username, "Test1", 1000)
        
        # Ověření přidané položky
        data = load_data(self.test_username)
        self.assertIn("Test1", data)
        self.assertTrue(isinstance(data["Test1"], list))
        self.assertEqual(len(data["Test1"]), original_test1_count + 1)
        self.assertEqual(data["Test1"][-1]["amount"], 1000)

if __name__ == '__main__':
    unittest.main() 
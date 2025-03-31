import unittest
import os
import json
import tempfile
import shutil
from datetime import datetime

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

from data_manager import DataManager

class TestExpenseInvestmentManager(unittest.TestCase):
    def setUp(self):
        """Nastavení před každým testem"""
        self.test_username = "test_user"
        self.data_manager = DataManager()
        
        # Nastavení cest k testovacím souborům
        self.investments_file = self.data_manager.get_user_investments_file(self.test_username)
        self.expenses_file = self.data_manager.get_user_expenses_file(self.test_username)
        
        # Smazání existujících souborů
        for file in [self.investments_file, self.expenses_file]:
            if os.path.exists(file):
                os.remove(file)

    @classmethod
    def tearDownClass(cls):
        """Úklid po všech testech"""
        shutil.rmtree(TEST_DIR)

    def test_load_investments_empty(self):
        """Test načtení prázdných investic"""
        investments = self.data_manager.load_investments(self.test_username)
        self.assertEqual(investments, [])

    def test_load_investments_with_data(self):
        """Test načtení existujících investic"""
        # Vytvoření testovacích dat
        test_investments = [
            {
                "type": "Akcie",
                "name": "Apple",
                "amount": 100000.0,
                "date": "2024-03-28"
            }
        ]
        
        # Uložení testovacích dat
        with open(self.investments_file, 'w', encoding='utf-8') as f:
            json.dump(test_investments, f)
        
        # Načtení dat
        investments = self.data_manager.load_investments(self.test_username)
        self.assertEqual(len(investments), 1)
        self.assertEqual(investments[0]["type"], "Akcie")
        self.assertEqual(investments[0]["name"], "Apple")
        self.assertEqual(investments[0]["amount"], 100000.0)

    def test_save_investments(self):
        """Test uložení investic"""
        test_investments = [
            {
                "type": "ETF",
                "name": "VWCE",
                "amount": 50000.0,
                "date": "2024-03-28"
            }
        ]
        
        # Uložení dat
        self.data_manager.save_investments(self.test_username, test_investments)
        
        # Ověření uložených dat
        with open(self.investments_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(len(loaded_data), 1)
        self.assertEqual(loaded_data[0]["type"], "ETF")
        self.assertEqual(loaded_data[0]["name"], "VWCE")
        self.assertEqual(loaded_data[0]["amount"], 50000.0)

    def test_load_expenses_empty(self):
        """Test načtení prázdných výdajů"""
        expenses = self.data_manager.load_expenses(self.test_username)
        self.assertEqual(expenses, [])

    def test_load_expenses_with_data(self):
        """Test načtení existujících výdajů"""
        # Vytvoření testovacích dat
        test_expenses = [
            {
                "amount": 1500.0,
                "category": "Potraviny",
                "type": "Výdaj",
                "date": "2024-03-28",
                "note": "Nákup v Albertu"
            }
        ]
        
        # Uložení testovacích dat
        with open(self.expenses_file, 'w', encoding='utf-8') as f:
            json.dump(test_expenses, f)
        
        # Načtení dat
        expenses = self.data_manager.load_expenses(self.test_username)
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["amount"], 1500.0)
        self.assertEqual(expenses[0]["category"], "Potraviny")
        self.assertEqual(expenses[0]["type"], "Výdaj")

    def test_save_expenses(self):
        """Test uložení výdajů"""
        test_expenses = [
            {
                "amount": 12000.0,
                "category": "Bydlení",
                "type": "Výdaj",
                "date": "2024-03-28",
                "note": "Nájem"
            }
        ]
        
        # Uložení dat
        self.data_manager.save_expenses(self.test_username, test_expenses)
        
        # Ověření uložených dat
        with open(self.expenses_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        self.assertEqual(len(loaded_data), 1)
        self.assertEqual(loaded_data[0]["amount"], 12000.0)
        self.assertEqual(loaded_data[0]["category"], "Bydlení")
        self.assertEqual(loaded_data[0]["type"], "Výdaj")

    def test_corrupted_investment_file(self):
        """Test načtení poškozeného souboru s investicemi"""
        # Vytvoření poškozeného JSON souboru
        with open(self.investments_file, 'w', encoding='utf-8') as f:
            f.write('{"invalid": "json"')  # Neuzavřená závorka
        
        # Pokus o načtení dat
        investments = self.data_manager.load_investments(self.test_username)
        self.assertEqual(investments, [])
        
        # Ověření vytvoření záložního souboru
        self.assertTrue(os.path.exists(self.investments_file + '.backup'))

    def test_corrupted_expense_file(self):
        """Test načtení poškozeného souboru s výdaji"""
        # Vytvoření poškozeného JSON souboru
        with open(self.expenses_file, 'w', encoding='utf-8') as f:
            f.write('{"invalid": "json"')  # Neuzavřená závorka
        
        # Pokus o načtení dat
        expenses = self.data_manager.load_expenses(self.test_username)
        self.assertEqual(expenses, [])
        
        # Ověření vytvoření záložního souboru
        self.assertTrue(os.path.exists(self.expenses_file + '.backup'))

if __name__ == '__main__':
    unittest.main() 
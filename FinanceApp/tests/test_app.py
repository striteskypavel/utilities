import unittest
import sys
import os
from datetime import datetime
import json
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

    def test_user_creation(self):
        """Test vytvoření uživatele"""
        # Test existence uživatele
        user = self.data_manager.get_user(self.test_username)
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], self.test_username)
        self.assertEqual(user['email'], self.test_email)

    def test_investment_operations(self):
        """Test operací s investicemi"""
        # Přidání testovací investice
        test_investment = {
            "amount": 10000,
            "type": "ETF a akcie",
            "name": "Test ETF",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "note": "Testovací investice"
        }
        
        # Test ukládání investic
        investments = [test_investment]
        self.data_manager.save_investments(self.test_username, investments)
        
        # Test načítání investic
        loaded_investments = self.data_manager.load_investments(self.test_username)
        self.assertEqual(len(loaded_investments), 1)
        self.assertEqual(loaded_investments[0]['amount'], test_investment['amount'])
        self.assertEqual(loaded_investments[0]['type'], test_investment['type'])

    def test_expense_operations(self):
        """Test operací s výdaji"""
        # Přidání testovacího výdaje
        test_expense = {
            "amount": 1000,
            "category": "Potraviny",
            "type": "Výdaj",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "note": "Testovací výdaj"
        }
        
        # Test ukládání výdajů
        expenses = [test_expense]
        self.data_manager.save_expenses(self.test_username, expenses)
        
        # Test načítání výdajů
        loaded_expenses = self.data_manager.load_expenses(self.test_username)
        self.assertEqual(len(loaded_expenses), 1)
        self.assertEqual(loaded_expenses[0]['amount'], test_expense['amount'])
        self.assertEqual(loaded_expenses[0]['category'], test_expense['category'])

    def test_user_authentication(self):
        """Test autentizace uživatele"""
        from App import verify_user
        
        # Test správných přihlašovacích údajů
        self.assertTrue(verify_user(self.test_username, self.test_password))
        
        # Test nesprávného hesla
        self.assertFalse(verify_user(self.test_username, "wrong_password"))
        
        # Test neexistujícího uživatele
        self.assertFalse(verify_user("nonexistent_user", "any_password"))

if __name__ == '__main__':
    unittest.main() 
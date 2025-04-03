import unittest
import sys
import os
from datetime import datetime
import json
from werkzeug.security import generate_password_hash
import shutil

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
            self.test_password,  # Předáváme heslo v plaintextu
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
        # Test správných přihlašovacích údajů
        self.assertTrue(self.data_manager.verify_user(self.test_username, self.test_password))
        
        # Test nesprávného hesla
        self.assertFalse(self.data_manager.verify_user(self.test_username, "wrong_password"))
        
        # Test neexistujícího uživatele
        self.assertFalse(self.data_manager.verify_user("nonexistent_user", "any_password"))

    def test_password_validation(self):
        """Test validace hesla"""
        # Test příliš krátkého hesla
        self.assertFalse(self.data_manager.validate_password("short"))
        
        # Test hesla bez čísla
        self.assertFalse(self.data_manager.validate_password("NoNumber!"))
        
        # Test hesla bez velkého písmena
        self.assertFalse(self.data_manager.validate_password("nouppercase123!"))
        
        # Test hesla bez speciálního znaku
        self.assertFalse(self.data_manager.validate_password("NoSpecial123"))
        
        # Test validního hesla
        self.assertTrue(self.data_manager.validate_password("ValidPass123!"))

    def test_email_validation(self):
        """Test validace emailu"""
        # Test nevalidních emailů
        self.assertFalse(self.data_manager.validate_email("notanemail"))
        self.assertFalse(self.data_manager.validate_email("still@not"))
        self.assertFalse(self.data_manager.validate_email("@invalid.com"))
        
        # Test validních emailů
        self.assertTrue(self.data_manager.validate_email("valid@email.com"))
        self.assertTrue(self.data_manager.validate_email("user.name+tag@domain.co.uk"))

    def test_username_validation(self):
        """Test validace uživatelského jména"""
        # Test příliš krátkého jména
        self.assertFalse(self.data_manager.validate_username("ab"))
        
        # Test jména s nepovolenými znaky
        self.assertFalse(self.data_manager.validate_username("user@name"))
        self.assertFalse(self.data_manager.validate_username("user name"))
        
        # Test již existujícího jména (s explicitní kontrolou existence)
        self.assertFalse(self.data_manager.validate_username(self.test_username, check_existence=True))
        
        # Test validních jmen
        self.assertTrue(self.data_manager.validate_username("new_user123"))
        self.assertTrue(self.data_manager.validate_username("validUser"))

    def test_email_uniqueness(self):
        """Test unikátnosti emailu"""
        # Vyčištění testovacích dat
        if os.path.exists(self.data_manager.data_dir):
            shutil.rmtree(self.data_manager.data_dir)
        if os.path.exists(self.data_manager.user_data_dir):
            shutil.rmtree(self.data_manager.user_data_dir)
        os.makedirs(self.data_manager.data_dir, exist_ok=True)
        os.makedirs(self.data_manager.user_data_dir, exist_ok=True)
        
        # První registrace by měla projít
        self.assertTrue(self.data_manager.create_user("user1", "ValidPass123!", "test1@example.com"))
        
        # Druhá registrace se stejným emailem by měla selhat
        self.assertFalse(self.data_manager.create_user("user2", "ValidPass123!", "test1@example.com"))
        
        # Registrace s jiným emailem by měla projít
        self.assertTrue(self.data_manager.create_user("user3", "ValidPass123!", "test2@example.com"))

    def test_registration_validation(self):
        """Test validace při registraci"""
        # Test registrace s nevalidním heslem
        self.assertFalse(self.data_manager.create_user("testuser1", "short", "valid@email.com"))
        
        # Test registrace s nevalidním emailem
        self.assertFalse(self.data_manager.create_user("testuser2", "ValidPass123!", "invalid"))
        
        # Test registrace s nevalidním uživatelským jménem
        self.assertFalse(self.data_manager.create_user("a", "ValidPass123!", "valid@email.com"))
        
        # Test validní registrace
        self.assertTrue(self.data_manager.create_user("validuser", "ValidPass123!", "new@email.com"))

    def test_concurrent_user_sessions(self):
        """Test souběžného přihlášení více uživatelů"""
        # Vyčištění testovacích dat
        if os.path.exists(self.data_manager.data_dir):
            shutil.rmtree(self.data_manager.data_dir)
        if os.path.exists(self.data_manager.user_data_dir):
            shutil.rmtree(self.data_manager.user_data_dir)
        os.makedirs(self.data_manager.data_dir, exist_ok=True)
        os.makedirs(self.data_manager.user_data_dir, exist_ok=True)
        
        # Vytvoření dvou testovacích uživatelů
        user1 = "test_user1"
        user2 = "test_user2"
        password = "Test123!"
        email1 = "test1@example.com"
        email2 = "test2@example.com"
        
        # Vytvoření uživatelů
        self.assertTrue(self.data_manager.create_user(user1, password, email1))
        self.assertTrue(self.data_manager.create_user(user2, password, email2))
        
        # Simulace souběžného přihlášení
        self.assertTrue(self.data_manager.verify_user(user1, password))
        self.assertTrue(self.data_manager.verify_user(user2, password))
        
        # Kontrola, že data zůstávají oddělená
        data1 = self.data_manager.load_data(user1)
        data2 = self.data_manager.load_data(user2)
        self.assertNotEqual(data1, data2)

if __name__ == '__main__':
    unittest.main() 
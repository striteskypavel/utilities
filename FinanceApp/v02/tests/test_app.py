import unittest
import sys
import os
from datetime import datetime
import json
from werkzeug.security import generate_password_hash
import shutil
import pytest
import streamlit as st
import tempfile

# Přidání cesty k aplikaci do PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_manager import DataManager

@pytest.fixture
def data_manager():
    """Create a DataManager instance with test data directory."""
    test_data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(test_data_dir, exist_ok=True)
    return DataManager(data_dir=test_data_dir)

class TestFinanceApp(unittest.TestCase):
    def setUp(self):
        """Nastavení před každým testem"""
        # Vytvoření dočasného adresáře pro testovací data
        self.test_dir = tempfile.mkdtemp()
        self.data_manager = DataManager(data_dir=self.test_dir)
        
        self.test_username = "test_user"
        self.test_password = "Test123!"
        self.test_email = "test@example.com"
        
        # Vytvoření testovacího uživatele
        self.data_manager.create_user(self.test_username, self.test_password, self.test_email)
    
    def tearDown(self):
        """Úklid po každém testu"""
        # Smazání dočasného adresáře
        shutil.rmtree(self.test_dir)
    
    def test_login_existing_user(self):
        """Test přihlášení existujícího uživatele."""
        # Test přihlášení se správnými údaji
        self.assertTrue(
            self.data_manager.verify_user(self.test_username, self.test_password),
            "Přihlášení se správnými údaji by mělo být úspěšné"
        )
        
        # Test přihlášení s nesprávným heslem
        self.assertFalse(
            self.data_manager.verify_user(self.test_username, "wrong_password"),
            "Přihlášení s nesprávným heslem by mělo selhat"
        )
        
        # Test přihlášení neexistujícího uživatele
        self.assertFalse(
            self.data_manager.verify_user("non_existent_user", self.test_password),
            "Přihlášení neexistujícího uživatele by mělo selhat"
        )
    
    def test_user_authentication(self):
        """Test autentizace uživatele."""
        # Test správného hesla
        self.assertTrue(
            self.data_manager.verify_user(self.test_username, self.test_password),
            "Ověření správného hesla by mělo být úspěšné"
        )
        
        # Test nesprávného hesla
        self.assertFalse(
            self.data_manager.verify_user(self.test_username, "wrong_password"),
            "Ověření nesprávného hesla by mělo selhat"
        )
        
        # Test neexistujícího uživatele
        self.assertFalse(
            self.data_manager.verify_user("non_existent_user", self.test_password),
            "Ověření neexistujícího uživatele by mělo selhat"
        )
    
    def test_user_creation(self):
        """Test vytvoření uživatele."""
        # Test vytvoření nového uživatele
        new_username = "new_test_user"
        new_password = "NewTest123!"
        new_email = "new_test@example.com"
        
        self.assertTrue(
            self.data_manager.create_user(new_username, new_password, new_email),
            "Vytvoření nového uživatele by mělo být úspěšné"
        )
        
        # Test vytvoření uživatele s existujícím jménem
        self.assertFalse(
            self.data_manager.create_user(self.test_username, "new_password", "new_email@example.com"),
            "Vytvoření uživatele s existujícím jménem by mělo selhat"
        )
        
        # Test vytvoření uživatele s existujícím emailem
        self.assertFalse(
            self.data_manager.create_user("another_user", "new_password", self.test_email),
            "Vytvoření uživatele s existujícím emailem by mělo selhat"
        )
    
    def test_password_validation(self):
        """Test validace hesla."""
        # Test platného hesla
        self.assertTrue(
            self.data_manager.validate_password("ValidPass123!"),
            "Platné heslo by mělo projít validací"
        )
        
        # Test příliš krátkého hesla
        self.assertFalse(
            self.data_manager.validate_password("Short1!"),
            "Příliš krátké heslo by nemělo projít validací"
        )
        
        # Test hesla bez čísla
        self.assertFalse(
            self.data_manager.validate_password("NoNumber!"),
            "Heslo bez čísla by nemělo projít validací"
        )
        
        # Test hesla bez velkého písmena
        self.assertFalse(
            self.data_manager.validate_password("nouppercase1!"),
            "Heslo bez velkého písmena by nemělo projít validací"
        )
        
        # Test hesla bez speciálního znaku
        self.assertFalse(
            self.data_manager.validate_password("NoSpecial1"),
            "Heslo bez speciálního znaku by nemělo projít validací"
        )
    
    def test_username_validation(self):
        """Test validace uživatelského jména."""
        # Test platného jména
        self.assertTrue(
            self.data_manager.validate_username("valid_username"),
            "Platné uživatelské jméno by mělo projít validací"
        )
        
        # Test příliš krátkého jména
        self.assertFalse(
            self.data_manager.validate_username("a"),
            "Příliš krátké jméno by nemělo projít validací"
        )
        
        # Test jména s neplatnými znaky
        self.assertFalse(
            self.data_manager.validate_username("invalid@name"),
            "Jméno s neplatnými znaky by nemělo projít validací"
        )
    
    def test_email_validation(self):
        """Test validace emailu."""
        # Test platného emailu
        self.assertTrue(
            self.data_manager.validate_email("valid@example.com"),
            "Platný email by měl projít validací"
        )
        
        # Test emailu bez @
        self.assertFalse(
            self.data_manager.validate_email("invalid.email.com"),
            "Email bez @ by neměl projít validací"
        )
        
        # Test emailu bez domény
        self.assertFalse(
            self.data_manager.validate_email("invalid@"),
            "Email bez domény by neměl projít validací"
        )
        
        # Test emailu bez uživatelské části
        self.assertFalse(
            self.data_manager.validate_email("@example.com"),
            "Email bez uživatelské části by neměl projít validací"
        )
    
    def test_email_uniqueness(self):
        """Test jedinečnosti emailu."""
        # Test vytvoření uživatele s unikátním emailem
        new_username = "unique_user"
        new_email = "unique@example.com"
        self.assertTrue(
            self.data_manager.create_user(new_username, "Test123!", new_email),
            "Vytvoření uživatele s unikátním emailem by mělo být úspěšné"
        )
        
        # Test vytvoření uživatele s existujícím emailem
        self.assertFalse(
            self.data_manager.create_user("another_user", "Test123!", new_email),
            "Vytvoření uživatele s existujícím emailem by mělo selhat"
        )
    
    def test_registration_validation(self):
        """Test validace registrace."""
        # Test platné registrace
        self.assertTrue(
            self.data_manager.create_user("new_user", "ValidPass123!", "new@example.com"),
            "Platná registrace by měla být úspěšná"
        )
        
        # Test registrace s neplatným jménem
        self.assertFalse(
            self.data_manager.create_user("a", "ValidPass123!", "new@example.com"),
            "Registrace s neplatným jménem by měla selhat"
        )
        
        # Test registrace s neplatným heslem
        self.assertFalse(
            self.data_manager.create_user("new_user", "weak", "new@example.com"),
            "Registrace s neplatným heslem by měla selhat"
        )
        
        # Test registrace s neplatným emailem
        self.assertFalse(
            self.data_manager.create_user("new_user", "ValidPass123!", "invalid.email"),
            "Registrace s neplatným emailem by měla selhat"
        )
    
    def test_expense_operations(self):
        """Test operací s výdaji."""
        # Přidání výdaje
        expense = {
            "amount": 100.0,
            "category": "Test",
            "date": datetime.now().isoformat(),
            "note": "Test expense"
        }
        self.assertTrue(
            self.data_manager.add_entry(self.test_username, "expense", expense),
            "Přidání výdaje by mělo být úspěšné"
        )
        
        # Načtení výdajů
        expenses = self.data_manager.load_expenses(self.test_username)
        self.assertEqual(len(expenses), 1, "Měl by existovat jeden výdaj")
        self.assertEqual(expenses[0]["amount"], 100.0, "Částka výdaje by měla být 100.0")
    
    def test_investment_operations(self):
        """Test operací s investicemi."""
        # Přidání investice
        investment = {
            "amount": 1000.0,
            "type": "Test",
            "date": datetime.now().isoformat(),
            "note": "Test investment"
        }
        self.assertTrue(
            self.data_manager.add_entry(self.test_username, "investment", investment),
            "Přidání investice by mělo být úspěšné"
        )
        
        # Načtení investic
        investments = self.data_manager.load_investments(self.test_username)
        self.assertEqual(len(investments), 1, "Měla by existovat jedna investice")
        self.assertEqual(investments[0]["amount"], 1000.0, "Částka investice by měla být 1000.0")
    
    def test_concurrent_user_sessions(self):
        """Test souběžných uživatelských session."""
        # Vytvoření druhého uživatele
        second_username = "second_user"
        second_password = "Test123!"
        second_email = "second@example.com"
        self.assertTrue(
            self.data_manager.create_user(second_username, second_password, second_email),
            "Vytvoření druhého uživatele by mělo být úspěšné"
        )
        
        # Test přihlášení prvního uživatele
        self.assertTrue(
            self.data_manager.verify_user(self.test_username, self.test_password),
            "Přihlášení prvního uživatele by mělo být úspěšné"
        )
        
        # Test přihlášení druhého uživatele
        self.assertTrue(
            self.data_manager.verify_user(second_username, second_password),
            "Přihlášení druhého uživatele by mělo být úspěšné"
        )
        
        # Test, že data uživatelů jsou oddělená
        expense1 = {
            "amount": 100.0,
            "category": "Test1",
            "date": datetime.now().isoformat(),
            "note": "Test expense 1"
        }
        expense2 = {
            "amount": 200.0,
            "category": "Test2",
            "date": datetime.now().isoformat(),
            "note": "Test expense 2"
        }
        
        self.data_manager.add_entry(self.test_username, "expense", expense1)
        self.data_manager.add_entry(second_username, "expense", expense2)
        
        expenses1 = self.data_manager.load_expenses(self.test_username)
        expenses2 = self.data_manager.load_expenses(second_username)
        
        self.assertEqual(len(expenses1), 1, "První uživatel by měl mít jeden výdaj")
        self.assertEqual(len(expenses2), 1, "Druhý uživatel by měl mít jeden výdaj")
        self.assertNotEqual(expenses1[0]["amount"], expenses2[0]["amount"], "Výdaje uživatelů by měly být různé")

    def test_session_persistence(self):
        """Test přetrvávání session po obnovení stránky."""
        # Vytvoření testovacího uživatele
        test_username = "test_session_user"
        test_password = "Test123!"
        test_email = "test_session@example.com"
        
        # Vytvoření uživatele
        self.assertTrue(
            self.data_manager.create_user(test_username, test_password, test_email),
            "Vytvoření testovacího uživatele by mělo být úspěšné"
        )
        
        # Simulace přihlášení
        self.assertTrue(
            self.data_manager.verify_user(test_username, test_password),
            "Přihlášení by mělo být úspěšné"
        )
        
        # Uložení session dat
        session_data = {
            "username": test_username,
            "is_authenticated": True,
            "last_activity": datetime.now().isoformat()
        }
        
        # Simulace obnovení stránky - načtení session dat
        loaded_session = self.data_manager.get_user_data(test_username)
        
        # Ověření, že session data jsou zachována
        self.assertIsNotNone(loaded_session, "Session data by měla existovat")
        self.assertEqual(loaded_session["username"], test_username, "Uživatelské jméno by mělo být zachováno")
        self.assertTrue(loaded_session.get("is_authenticated", False), "Stav přihlášení by měl být zachován")
        
        # Vyčištění testovacích dat
        self.data_manager.save_data(test_username, {})
        users = self.data_manager.load_users()
        if test_username in users:
            del users[test_username]
            self.data_manager.save_users(users)

    def test_password_change(self):
        """Test změny hesla."""
        # Test změny hesla na platné
        new_password = "NewTest123!"
        self.assertTrue(
            self.data_manager.update_user_password(self.test_username, new_password),
            "Změna hesla by měla být úspěšná"
        )
        
        # Ověření nového hesla
        self.assertTrue(
            self.data_manager.verify_user(self.test_username, new_password),
            "Přihlášení s novým heslem by mělo být úspěšné"
        )
        
        # Test změny hesla na neplatné
        self.assertFalse(
            self.data_manager.update_user_password(self.test_username, "weak"),
            "Změna hesla na neplatné by měla selhat"
        )
        
        # Test změny hesla neexistujícího uživatele
        self.assertFalse(
            self.data_manager.update_user_password("non_existent_user", "NewTest123!"),
            "Změna hesla neexistujícího uživatele by měla selhat"
        )
    
    def test_session_management(self):
        """Test správy session a odhlašování."""
        # Test přihlášení
        self.assertTrue(
            self.data_manager.verify_user(self.test_username, self.test_password),
            "Přihlášení by mělo být úspěšné"
        )
        
        # Simulace odhlašování - vyčištění session
        session_data = {
            "username": self.test_username,
            "is_authenticated": True,
            "last_activity": datetime.now().isoformat()
        }
        
        # Ověření, že session data jsou vyčištěna
        self.data_manager.save_data(self.test_username, {})
        loaded_data = self.data_manager.load_data(self.test_username)
        self.assertEqual(loaded_data, {}, "Session data by měla být vyčištěna po odhlášení")
        
        # Ověření, že uživatel je stále v databázi
        users = self.data_manager.load_users()
        self.assertIn(self.test_username, users, "Uživatel by měl zůstat v databázi po odhlášení")
        
        # Ověření, že se nelze přihlásit s vyčištěnými session daty
        self.assertFalse(
            self.data_manager.verify_user(self.test_username, "invalid_password"),
            "Přihlášení s vyčištěnými session daty by mělo selhat"
        )

def test_login_existing_user(data_manager):
    """Test login functionality with an existing user."""
    # Create test user
    username = "test_user"
    password = "Test123!"
    email = "test@example.com"
    
    # Ensure user doesn't exist first
    users = data_manager.load_users()
    if username in users:
        del users[username]
        data_manager.save_users(users)
    
    # Create new user
    assert data_manager.create_user(username, password, email), "Failed to create test user"
    
    # Test login with correct credentials
    assert data_manager.verify_user(username, password), "Login with correct credentials failed"
    
    # Test login with incorrect password
    assert not data_manager.verify_user(username, "wrong_password"), "Login with incorrect password should fail"
    
    # Test login with non-existent user
    assert not data_manager.verify_user("non_existent_user", password), "Login with non-existent user should fail"
    
    # Clean up
    users = data_manager.load_users()
    if username in users:
        del users[username]
        data_manager.save_users(users)

if __name__ == '__main__':
    unittest.main() 
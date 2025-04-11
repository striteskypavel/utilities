import unittest
import os
import json
import shutil
from datetime import datetime, timedelta
import streamlit as st
import extra_streamlit_components as stx
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from v02.user_manager import UserManager, create_session_cookie, get_session_cookie, clear_session_cookie

class TestAuth(unittest.TestCase):
    def setUp(self):
        """Příprava testovacího prostředí"""
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)
        self.users_file = os.path.join(self.test_dir, "users.json")
        self.manager = UserManager()
        self.manager.users_file = self.users_file

    def tearDown(self):
        """Úklid po testu"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_disk_space(self):
        """Test kontroly místa na disku"""
        # Vytvoření velkého souboru
        with open(self.users_file, 'w') as f:
            f.write('A' * (1024 * 1024 + 1))  # Více než 1MB
        self.assertFalse(self.manager.check_disk_space())

    def test_xss_protection(self):
        """Test ochrany proti XSS"""
        test_input = "<script>alert('xss')</script>"
        sanitized = self.manager.sanitize_input(test_input)
        self.assertNotIn("<script>", sanitized)
        self.assertNotIn("alert", sanitized)

    def test_session_management(self):
        """Test správy session"""
        username = "testuser"
        create_session_cookie(username)
        self.assertEqual(get_session_cookie(), username)
        clear_session_cookie()
        self.assertIsNone(get_session_cookie())

    def test_session_expiration(self):
        """Test expirace session"""
        username = "testuser"
        create_session_cookie(username, expiry_days=-1)  # Expired cookie
        self.assertIsNone(get_session_cookie())

    def test_invalid_emails(self):
        """Test validace emailů"""
        invalid_emails = [
            "invalid",
            "invalid@",
            "invalid@domain",
            "invalid@domain.",
            "@domain.com",
            "invalid@.com"
        ]
        for email in invalid_emails:
            self.assertFalse(self.manager.validate_email(email))

    def test_password_special_chars(self):
        """Test speciálních znaků v hesle"""
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        for i, char in enumerate(special_chars):
            username = f"testuser{i}"
            password = f"test{char}pass1"  # Přidáno číslo pro splnění minimálních požadavků
            success, message = self.manager.register_user(username, password)
            self.assertTrue(success, f"Failed for char '{char}': {message}")

    def test_long_credentials(self):
        """Test dlouhých přihlašovacích údajů"""
        long_username = "a" * 100
        long_password = "b" * 100
        success, _ = self.manager.register_user(long_username, long_password)
        self.assertTrue(success)

    def test_brute_force_protection(self):
        """Test ochrany proti brute force"""
        username = "testuser"
        password = "correctpass"
        self.manager.register_user(username, password)
        
        # Simulace neúspěšných pokusů
        for _ in range(5):
            self.assertFalse(self.manager.verify_password(username, "wrongpass"))

    def test_corrupted_user_file(self):
        """Test poškozeného souboru uživatelů"""
        with open(self.users_file, 'w') as f:
            f.write("invalid json")
        users = self.manager.load_users()
        self.assertEqual(users, {})

    def test_file_permissions(self):
        """Test oprávnění souborů"""
        self.manager.register_user("testuser", "testpass")
        self.assertTrue(os.path.exists(self.users_file))
        self.assertTrue(os.access(self.users_file, os.R_OK))
        self.assertTrue(os.access(self.users_file, os.W_OK))

if __name__ == '__main__':
    unittest.main() 
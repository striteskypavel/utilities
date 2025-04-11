import unittest
from datetime import datetime, timedelta
import pandas as pd
from expense_tracker import show_expense_tracker
from data_manager import DataManager
import streamlit as st

class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        """Nastavení před každým testem"""
        self.data_manager = DataManager()
        self.test_user = "test_user"
        self.test_data = {
            "Nájem": [
                {
                    "type": "Výdaj",
                    "amount": 15000.0,
                    "timestamp": "2025-04-01T10:00:00",
                    "note": "Test note 1"
                }
            ],
            "Mzda": [
                {
                    "type": "Příjem",
                    "amount": 50000.0,
                    "timestamp": "2025-04-01T09:00:00",
                    "note": "Test note 2"
                }
            ]
        }
        # Uložení testovacích dat
        self.data_manager.save_data(self.test_user, self.test_data)

    def test_edit_record(self):
        """Test editace záznamu"""
        # Načtení dat
        data = self.data_manager.load_data(self.test_user)
        
        # Vytvoření DataFrame pro editaci
        df_details = []
        for cat, entries in data.items():
            for entry in entries:
                df_details.append({
                    'Kategorie': cat,
                    'Typ': entry['type'],
                    'Částka': float(entry['amount']),
                    'Datum': datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M'),
                    'Poznámka': entry['note'],
                    'Upravit': True,  # Označení pro úpravu
                    'Smazat': False
                })
        
        edited_df = pd.DataFrame(df_details)
        
        # Úprava záznamu
        edited_df.loc[0, 'Částka'] = 16000.0
        edited_df.loc[0, 'Poznámka'] = "Updated note"
        
        # Simulace uložení změn
        existing_data = self.data_manager.load_data(self.test_user)
        changes_made = False
        
        for _, row in edited_df.iterrows():
            if row['Upravit']:
                category = row['Kategorie']
                if category not in existing_data:
                    existing_data[category] = []
                
                new_entry = {
                    'type': row['Typ'],
                    'amount': float(row['Částka']),
                    'timestamp': datetime.strptime(row['Datum'], '%Y-%m-%d %H:%M').isoformat(),
                    'note': row['Poznámka']
                }
                
                entries = existing_data[category]
                if isinstance(entries, list):
                    for i, entry in enumerate(entries):
                        if (entry['type'] == row['Typ'] and
                            datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M') == row['Datum']):
                            entries[i] = new_entry
                            changes_made = True
                            break
        
        # Uložení změn
        self.data_manager.save_data(self.test_user, existing_data)
        
        # Ověření změn
        updated_data = self.data_manager.load_data(self.test_user)
        self.assertEqual(updated_data['Nájem'][0]['amount'], 16000.0)
        self.assertEqual(updated_data['Nájem'][0]['note'], "Updated note")
        self.assertTrue(changes_made)

    def test_delete_record(self):
        """Test smazání záznamu"""
        # Načtení dat
        data = self.data_manager.load_data(self.test_user)
        
        # Vytvoření DataFrame pro smazání
        df_details = []
        for cat, entries in data.items():
            for entry in entries:
                df_details.append({
                    'Kategorie': cat,
                    'Typ': entry['type'],
                    'Částka': float(entry['amount']),
                    'Datum': datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M'),
                    'Poznámka': entry['note'],
                    'Upravit': False,
                    'Smazat': True if cat == 'Nájem' else False  # Označíme Nájem pro smazání
                })
        
        edited_df = pd.DataFrame(df_details)
        
        # Simulace smazání
        existing_data = self.data_manager.load_data(self.test_user)
        changes_made = False
        categories_to_delete = set()  # Seznam kategorií ke smazání
        
        for _, row in edited_df.iterrows():
            if row['Smazat']:
                category = row['Kategorie']
                if category in existing_data:
                    entries = existing_data[category]
                    if isinstance(entries, list):
                        existing_data[category] = [
                            entry for entry in entries
                            if not (
                                entry['type'] == row['Typ'] and
                                float(entry['amount']) == float(row['Částka']) and
                                datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M') == row['Datum']
                            )
                        ]
                        if not existing_data[category]:  # Pokud je seznam prázdný
                            categories_to_delete.add(category)
                        changes_made = True
        
        # Smazání prázdných kategorií
        for category in categories_to_delete:
            del existing_data[category]
        
        # Uložení změn
        self.data_manager.save_data(self.test_user, existing_data)
        
        # Ověření změn
        updated_data = self.data_manager.load_data(self.test_user)
        self.assertNotIn('Nájem', updated_data)  # Kategorie Nájem by měla být smazána
        self.assertIn('Mzda', updated_data)  # Kategorie Mzda by měla zůstat
        self.assertTrue(changes_made)

    def test_add_new_record(self):
        """Test přidání nového záznamu"""
        # Vytvoření nového záznamu
        new_entry = {
            "type": "Výdaj",
            "amount": 1000.0,
            "timestamp": datetime.now().isoformat(),
            "note": "New test entry"
        }
        
        # Přidání záznamu
        self.data_manager.add_entry(self.test_user, "Test", new_entry)
        
        # Ověření přidání
        updated_data = self.data_manager.load_data(self.test_user)
        self.assertIn("Test", updated_data)
        self.assertEqual(updated_data["Test"][0]["amount"], 1000.0)
        self.assertEqual(updated_data["Test"][0]["note"], "New test entry")

    def test_invalid_edit(self):
        """Test neplatné editace záznamu"""
        # Načtení dat
        data = self.data_manager.load_data(self.test_user)
        
        # Vytvoření DataFrame s neplatnými daty
        df_details = []
        for cat, entries in data.items():
            for entry in entries:
                df_details.append({
                    'Kategorie': cat,
                    'Typ': entry['type'],
                    'Částka': -100.0,  # Neplatná částka
                    'Datum': datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M'),
                    'Poznámka': entry['note'],
                    'Upravit': True,
                    'Smazat': False
                })
        
        edited_df = pd.DataFrame(df_details)
        
        # Simulace uložení změn
        existing_data = self.data_manager.load_data(self.test_user)
        original_data = self.data_manager.load_data(self.test_user)
        
        for _, row in edited_df.iterrows():
            if row['Upravit']:
                if row['Částka'] < 0:  # Kontrola neplatné částky
                    continue
                
                category = row['Kategorie']
                if category not in existing_data:
                    existing_data[category] = []
                
                new_entry = {
                    'type': row['Typ'],
                    'amount': float(row['Částka']),
                    'timestamp': datetime.strptime(row['Datum'], '%Y-%m-%d %H:%M').isoformat(),
                    'note': row['Poznámka']
                }
                
                entries = existing_data[category]
                if isinstance(entries, list):
                    for i, entry in enumerate(entries):
                        if (entry['type'] == row['Typ'] and
                            datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M') == row['Datum']):
                            entries[i] = new_entry
                            break
        
        # Ověření, že data zůstala nezměněna
        self.assertEqual(existing_data, original_data)

    def test_invalid_date_format(self):
        """Test neplatného formátu data"""
        # Načtení dat
        data = self.data_manager.load_data(self.test_user)
        
        # Vytvoření DataFrame s neplatným datem
        df_details = []
        for cat, entries in data.items():
            for entry in entries:
                df_details.append({
                    'Kategorie': cat,
                    'Typ': entry['type'],
                    'Částka': float(entry['amount']),
                    'Datum': "2025-13-32 25:61",  # Neplatné datum
                    'Poznámka': entry['note'],
                    'Upravit': True,
                    'Smazat': False
                })
        
        edited_df = pd.DataFrame(df_details)
        
        # Simulace uložení změn
        existing_data = self.data_manager.load_data(self.test_user)
        original_data = self.data_manager.load_data(self.test_user)
        changes_made = False
        
        for _, row in edited_df.iterrows():
            if row['Upravit']:
                try:
                    # Pokus o převod data
                    datetime.strptime(row['Datum'], '%Y-%m-%d %H:%M')
                    
                    category = row['Kategorie']
                    if category not in existing_data:
                        existing_data[category] = []
                    
                    new_entry = {
                        'type': row['Typ'],
                        'amount': float(row['Částka']),
                        'timestamp': datetime.strptime(row['Datum'], '%Y-%m-%d %H:%M').isoformat(),
                        'note': row['Poznámka']
                    }
                    
                    entries = existing_data[category]
                    if isinstance(entries, list):
                        for i, entry in enumerate(entries):
                            if (entry['type'] == row['Typ'] and
                                datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M') == row['Datum']):
                                entries[i] = new_entry
                                changes_made = True
                                break
                except ValueError:
                    continue
        
        # Ověření, že data zůstala nezměněna
        self.assertEqual(existing_data, original_data)
        self.assertFalse(changes_made)

    def test_duplicate_entry(self):
        """Test přidání duplicitního záznamu"""
        # Vytvoření duplicitního záznamu
        duplicate_entry = {
            "type": "Výdaj",
            "amount": 15000.0,
            "timestamp": "2025-04-01T10:00:00",
            "note": "Test note 1"
        }
        
        # Pokus o přidání duplicitního záznamu
        self.data_manager.add_entry(self.test_user, "Nájem", duplicate_entry)
        
        # Ověření, že nebyl přidán duplicitní záznam
        updated_data = self.data_manager.load_data(self.test_user)
        self.assertEqual(len(updated_data["Nájem"]), 1)
        self.assertEqual(updated_data["Nájem"][0]["amount"], 15000.0)

    def test_note_length(self):
        """Test délky poznámky"""
        # Vytvoření záznamu s dlouhou poznámkou
        long_note = "x" * 1000  # 1000 znaků
        entry_with_long_note = {
            "type": "Výdaj",
            "amount": 1000.0,
            "timestamp": datetime.now().isoformat(),
            "note": long_note
        }
        
        # Přidání záznamu s dlouhou poznámkou
        self.data_manager.add_entry(self.test_user, "Test", entry_with_long_note)
        
        # Ověření, že poznámka byla uložena
        updated_data = self.data_manager.load_data(self.test_user)
        self.assertEqual(len(updated_data["Test"][0]["note"]), 1000)

    def test_amount_precision(self):
        """Test přesnosti částky"""
        # Vytvoření záznamu s desetinnou částkou
        entry_with_decimal = {
            "type": "Výdaj",
            "amount": 1000.56,
            "timestamp": datetime.now().isoformat(),
            "note": "Test decimal amount"
        }
        
        # Přidání záznamu
        self.data_manager.add_entry(self.test_user, "Test", entry_with_decimal)
        
        # Ověření přesnosti částky
        updated_data = self.data_manager.load_data(self.test_user)
        self.assertEqual(updated_data["Test"][0]["amount"], 1000.56)

    def test_future_date(self):
        """Test data v budoucnosti"""
        # Vytvoření záznamu s budoucím datem
        future_date = (datetime.now() + timedelta(days=365)).isoformat()
        future_entry = {
            "type": "Výdaj",
            "amount": 1000.0,
            "timestamp": future_date,
            "note": "Future entry"
        }
        
        # Přidání záznamu s budoucím datem
        self.data_manager.add_entry(self.test_user, "Test", future_entry)
        
        # Ověření, že záznam byl uložen s budoucím datem
        updated_data = self.data_manager.load_data(self.test_user)
        saved_date = datetime.fromisoformat(updated_data["Test"][0]["timestamp"])
        self.assertTrue(saved_date > datetime.now())

    def test_empty_category(self):
        """Test prázdné kategorie"""
        # Pokus o přidání záznamu s prázdnou kategorií
        entry = {
            "type": "Výdaj",
            "amount": 1000.0,
            "timestamp": datetime.now().isoformat(),
            "note": "Test empty category"
        }
        
        # Ověření, že nelze přidat záznam s prázdnou kategorií
        with self.assertRaises(ValueError):
            self.data_manager.add_entry(self.test_user, "", entry)

    def tearDown(self):
        """Úklid po každém testu"""
        # Smazání testovacích dat
        self.data_manager.save_data(self.test_user, {})

if __name__ == '__main__':
    unittest.main() 
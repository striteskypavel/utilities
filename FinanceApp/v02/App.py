import streamlit as st
import pandas as pd
import json
from datetime import datetime
from data_manager import (
    load_data, save_data, add_entry,
    export_data, import_data, get_history
)
from visualizations import (
    show_pie_chart, show_history_chart, 
    show_category_comparison
)
from history_manager import log_change, load_history, clear_history, delete_history_entries
from config import DEFAULT_CATEGORIES
from retirement_planning import show_retirement_planning
from mortgage_calculator import show_mortgage_calculator
from user_manager import create_user, verify_user, get_user_data, update_user_password, get_user_file_path
import os
import time
from expense_tracker import show_expense_tracker

# Konfigurace stránky
st.set_page_config(
    page_title="Finanční aplikace",
    page_icon="💰",
    layout="wide"
)

def show_login_page():
    """Zobrazí přihlašovací stránku"""
    # Vytvoření tří sloupců pro centrování obsahu
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("Přihlášení")
        st.markdown("""
        ### Vítejte v Finance App
        
        Tato aplikace vám pomůže:
        - Sledovat vaše výdaje a příjmy
        - Analyzovat finanční trendy
        - Plánovat rozpočet
        - Spravovat vaše finance efektivně
        """)
        
        st.subheader("Přihlášení")
        with st.form("login_form"):
            username = st.text_input("Uživatelské jméno")
            password = st.text_input("Heslo", type="password")
            submit = st.form_submit_button("Přihlásit se", use_container_width=True)
            
            if submit:
                success, user_data = verify_user(username, password)
                if success and user_data:
                    st.success("Přihlášení bylo úspěšné!")
                    return user_data.get("name"), True, user_data
                else:
                    st.error("Nesprávné přihlašovací údaje")
                    return None, False, None
        
        st.markdown("---")
        st.subheader("Registrace nového uživatele")
        with st.form("register_form"):
            new_username = st.text_input("Nové uživatelské jméno")
            new_password = st.text_input("Nové heslo", type="password")
            confirm_password = st.text_input("Potvrzení hesla", type="password")
            email = st.text_input("E-mail")
            name = st.text_input("Jméno")
            register = st.form_submit_button("Registrovat", use_container_width=True)
            
            if register:
                # Validace všech polí
                if not new_username or not new_username.strip():
                    st.error("Zadejte uživatelské jméno")
                elif not new_password or not new_password.strip():
                    st.error("Zadejte heslo")
                elif not confirm_password or not confirm_password.strip():
                    st.error("Potvrďte heslo")
                elif not email or not email.strip():
                    st.error("Zadejte e-mail")
                elif not name or not name.strip():
                    st.error("Zadejte jméno")
                elif new_password != confirm_password:
                    st.error("Hesla se neshodují")
                else:
                    # Validace síly hesla
                    password_errors = []
                    if len(new_password) < 8:
                        password_errors.append("Heslo musí mít alespoň 8 znaků")
                    if not any(c.isupper() for c in new_password):
                        password_errors.append("Heslo musí obsahovat alespoň jedno velké písmeno")
                    if not any(c.islower() for c in new_password):
                        password_errors.append("Heslo musí obsahovat alespoň jedno malé písmeno")
                    if not any(c.isdigit() for c in new_password):
                        password_errors.append("Heslo musí obsahovat alespoň jednu číslici")
                    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in new_password):
                        password_errors.append("Heslo musí obsahovat alespoň jeden speciální znak")
                    
                    if password_errors:
                        st.error("Heslo nesplňuje požadavky na bezpečnost:")
                        for error in password_errors:
                            st.error(error)
                    else:
                        # Validace e-mailu
                        import re
                        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if not re.match(email_pattern, email):
                            st.error("Zadejte platnou e-mailovou adresu")
                        else:
                            # Kontrola existence uživatele
                            if os.path.exists(get_user_file_path(new_username)):
                                st.error("Uživatelské jméno již existuje. Zvolte jiné.")
                            elif create_user(new_username, new_password, email, name):
                                st.success("Registrace byla úspěšná! Můžete se přihlásit.")
                            else:
                                st.error("Nastala chyba při registraci. Zkuste to prosím znovu.")
    
    return None, False, None

def show_main_app(username, name):
    """Zobrazí hlavní aplikaci po přihlášení"""
    # Zobrazení jména přihlášeného uživatele a tlačítka pro odhlášení
    if st.sidebar.button("Odhlásit"):
        del st.session_state["user"]
        st.rerun()
    
    st.sidebar.title(f'Vítejte, {name}')
    
    # Načtení dat pro přihlášeného uživatele
    data = load_data(username)
    history = get_history(username)

    # Nastavení sidebaru
    st.sidebar.title("Nástroje")

    # Navigace
    menu = st.sidebar.selectbox(
        "Menu",
        ["Přehled", "Sledování výdajů", "Hypoteční kalkulačka", "Plánování důchodu", "Export/Import", "Správa uživatele"]
    )

    if menu == "Přehled":
        show_overview(username)
        
        # Hlavní obsah aplikace - pouze pro přehled
        st.title("Jednoduchý sledovač financí")

        # Přidání finančních záznamů
        st.subheader("Přidat finanční záznam")

        new_category = st.text_input("Název nové kategorie").strip()
        type_ = st.selectbox("Typ", ["Výdaj", "Příjem"])
        amount = st.number_input("Částka", min_value=0, step=1000, format="%d")
        
        if st.button("Přidat"):
            if not new_category:
                st.error("Zadejte název kategorie!")
            elif new_category in data:
                st.error(f"Kategorie '{new_category}' již existuje!")
            else:
                entry_data = {
                    "type": type_,
                    "amount": amount,
                    "timestamp": datetime.now().isoformat()
                }
                add_entry(username, new_category, entry_data)
                st.success(f"Vytvořena nová kategorie '{new_category}' a přidán záznam!")
                st.rerun()

        # Přehled financí
        st.subheader("Přehled financí")
        
        # Výpočet součtů pro každou kategorii a typ
        totals = {}
        for cat, entries in data.items():
            if isinstance(entries, list):
                for entry in entries:
                    type_ = entry.get("type", "Výdaj")
                    if cat not in totals:
                        totals[cat] = {"Výdaj": 0, "Příjem": 0}
                    totals[cat][type_] += float(entry.get("amount", 0))
            else:
                type_ = entries.get("type", "Výdaj")
                if cat not in totals:
                    totals[cat] = {"Výdaj": 0, "Příjem": 0}
                totals[cat][type_] += float(entries.get("amount", 0))
        
        # Vytvoření DataFrame pro zobrazení
        df = pd.DataFrame([
            {
                'Kategorie': cat,
                'Výdaje': data['Výdaj'],
                'Příjmy': data['Příjem'],
                'Bilance': data['Příjem'] - data['Výdaj']
            }
            for cat, data in totals.items()
        ])

        edited_df = st.data_editor(
            df,
            column_config={
                "Kategorie": st.column_config.TextColumn("Kategorie", disabled=True),
                "Výdaje": st.column_config.NumberColumn(
                    "Výdaje",
                    help="Upravte částku výdajů přímo v tabulce",
                    min_value=0,
                    format="%.0f Kč"
                ),
                "Příjmy": st.column_config.NumberColumn(
                    "Příjmy",
                    help="Upravte částku příjmů přímo v tabulce",
                    min_value=0,
                    format="%.0f Kč"
                ),
                "Bilance": st.column_config.NumberColumn(
                    "Bilance",
                    help="Bilance příjmů a výdajů",
                    disabled=True,
                    format="%.0f Kč"
                )
            },
            use_container_width=True,
            hide_index=True
        )

        if not df.equals(edited_df):
            for idx, row in edited_df.iterrows():
                category = row["Kategorie"]
                new_expenses = row["Výdaje"]
                new_income = row["Příjmy"]
                old_expenses = totals[category]["Výdaj"]
                old_income = totals[category]["Příjem"]
                
                if new_expenses != old_expenses or new_income != old_income:
                    if data[category]:
                        # Aktualizace výdajů
                        if new_expenses != old_expenses:
                            data[category][-1]["amount"] = new_expenses
                            data[category][-1]["type"] = "Výdaj"
                            save_data(username, data)
                            log_change(f"{category} (výdaje)", old_expenses, new_expenses)
                        
                        # Aktualizace příjmů
                        if new_income != old_income:
                            data[category][-1]["amount"] = new_income
                            data[category][-1]["type"] = "Příjem"
                            save_data(username, data)
                            log_change(f"{category} (příjmy)", old_income, new_income)
                        
                        st.success(f"Částky pro kategorii '{category}' byly aktualizovány!")
                        st.rerun()

        # Vizualizace dat
        st.header("Vizualizace dat")
        viz_tabs = st.tabs(["Rozložení financí", "Historie změn", "Porovnání kategorií"])

        with viz_tabs[0]:
            st.subheader("Rozložení financí")
            show_pie_chart(totals, height=600)

        with viz_tabs[1]:
            st.subheader("Historie změn")
            show_history_chart(history, height=600)

        with viz_tabs[2]:
            st.subheader("Porovnání kategorií")
            show_category_comparison(data, height=600)

    elif menu == "Sledování výdajů":
        show_expense_tracker(username)
    elif menu == "Hypoteční kalkulačka":
        show_mortgage_calculator()
    elif menu == "Plánování důchodu":
        show_retirement_planning()
    elif menu == "Export/Import":
        show_export_import(username)
    elif menu == "Správa uživatele":
        show_settings(username)

    # Modul pro správu historie
    with st.sidebar.expander("Správa historie", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Vymazat celou historii"):
                clear_history()
                st.success("Historie byla vymazána")
                st.rerun()
        
        with col2:
            if history:
                categories = sorted(set(entry["category"] for entry in history))
                selected_category = st.selectbox("Vyberte kategorii", [""] + categories)
                
                if selected_category and st.button(f"Smazat záznamy kategorie '{selected_category}'"):
                    deleted = delete_history_entries({"category": selected_category})
                    st.success(f"Smazáno {deleted} záznamů kategorie '{selected_category}'")
                    st.rerun()
        
        st.write("Smazat záznamy podle data")
        date_col1, date_col2 = st.columns(2)
        
        with date_col1:
            before_date = st.date_input("Smazat záznamy před datem", None)
            if before_date and st.button("Smazat staré záznamy"):
                before_date_str = datetime.combine(before_date, datetime.min.time()).isoformat()
                deleted = delete_history_entries({"before_date": before_date_str})
                st.success(f"Smazáno {deleted} záznamů před {before_date}")
                st.rerun()
        
        with date_col2:
            if history:
                entry_ids = list(range(len(history)))
                selected_id = st.selectbox("Vyberte ID záznamu ke smazání", [""] + entry_ids)
                
                if selected_id != "" and st.button("Smazat vybraný záznam"):
                    delete_history_entries({"id": selected_id})
                    st.success(f"Záznam s ID {selected_id} byl smazán")
                    st.rerun()

    # O aplikaci
    with st.sidebar.expander("O aplikaci", expanded=False):
        st.write("""
        **Jednoduchý sledovač financí** je aplikace pro sledování osobních financí.
        
        Funkce:
        - Přidávání finančních záznamů do kategorií
        - Vizualizace dat pomocí různých typů grafů
        - Sledování historie změn
        - Správa historie
        
        Vytvořeno pomocí Streamlit.
        """)

def show_export_import(username: str):
    """Zobrazí modul pro export a import dat"""
    st.title("Export a import dat")
    
    # Načtení dat
    data = load_data(username)
    
    # Vytvoření dvou sloupců pro export a import
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export dat")
        export_format = st.radio("Formát exportu", ["JSON", "CSV"], horizontal=True)
        
        # Vytvoření dočasného souboru pro export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format == "JSON":
            # Pro JSON export použijeme přímo data z paměti
            export_data_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
            st.download_button(
                label="Stáhnout JSON",
                data=export_data_bytes,
                file_name=f"finance_data_{timestamp}.json",
                mime="application/json"
            )
        else:  # CSV
            # Pro CSV export vytvoříme DataFrame
            rows = []
            for category, entries in data.items():
                if isinstance(entries, list):
                    for entry in entries:
                        rows.append({
                            "Kategorie": category,
                            "Částka": entry["amount"],
                            "Datum": entry["timestamp"],
                            "Poznámka": entry.get("note", "")
                        })
                else:
                    rows.append({
                        "Kategorie": category,
                        "Částka": entries["amount"],
                        "Datum": entries["timestamp"],
                        "Poznámka": entries.get("note", "")
                    })
            
            df = pd.DataFrame(rows)
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Stáhnout CSV",
                data=csv_data,
                file_name=f"finance_data_{timestamp}.csv",
                mime="text/csv"
            )
    
    with col2:
        st.subheader("Import dat")
        uploaded_file = st.file_uploader("Vyberte soubor pro import", type=["json", "csv"])
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            success_message = st.empty()
            
            if st.button("Importovat data"):
                temp_file = f"temp_import.{file_extension}"
                with open(temp_file, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                if import_data(username, temp_file, format=file_extension):
                    success_message.success("Data byla úspěšně importována!")
                    time.sleep(3)
                    success_message.empty()
                    st.rerun()
                else:
                    st.error("Chyba při importu dat. Zkontrolujte formát souboru.")
                
                if os.path.exists(temp_file):
                    os.remove(temp_file)

def show_settings(username: str):
    """Zobrazí nastavení uživatele"""
    st.title("Nastavení")
    
    # Načtení dat uživatele
    user_data = get_user_data(username)
    
    # Formulář pro změnu hesla
    st.subheader("Změna hesla")
    with st.form("password_change"):
        old_password = st.text_input("Staré heslo", type="password")
        new_password = st.text_input("Nové heslo", type="password")
        confirm_password = st.text_input("Potvrzení nového hesla", type="password")
        submit = st.form_submit_button("Změnit heslo", use_container_width=True)
        
        if submit:
            if not old_password or not new_password or not confirm_password:
                st.error("Vyplňte všechna pole")
            elif new_password != confirm_password:
                st.error("Nové heslo a potvrzení se neshodují")
            else:
                success, message = update_user_password(username, old_password, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    # Informace o účtu
    st.subheader("Informace o účtu")
    st.write(f"**Uživatelské jméno:** {user_data['username']}")
    st.write(f"**E-mail:** {user_data['email']}")
    st.write(f"**Jméno:** {user_data['name']}")
    st.write(f"**Účet vytvořen:** {datetime.fromisoformat(user_data['created_at']).strftime('%d.%m.%Y %H:%M')}")

def show_overview(username: str):
    """Zobrazí přehled financí"""
    st.title("Přehled financí")
    
    # Načtení dat
    data = load_data(username)
    
    if data:
        # Výpočet celkových součtů pro každou kategorii a typ
        totals = {}
        for cat, entries in data.items():
            if isinstance(entries, list):
                for entry in entries:
                    type_ = entry.get("type", "Výdaj")
                    if cat not in totals:
                        totals[cat] = {"Výdaj": 0, "Příjem": 0}
                    totals[cat][type_] += float(entry.get("amount", 0))
            else:
                type_ = entries.get("type", "Výdaj")
                if cat not in totals:
                    totals[cat] = {"Výdaj": 0, "Příjem": 0}
                totals[cat][type_] += float(entries.get("amount", 0))
        
        # Vytvoření DataFrame pro zobrazení
        df_totals = pd.DataFrame([
            {
                'Kategorie': cat,
                'Výdaje': data['Výdaj'],
                'Příjmy': data['Příjem'],
                'Bilance': data['Příjem'] - data['Výdaj']
            }
            for cat, data in totals.items()
        ])
        df_totals = df_totals.sort_values('Bilance', ascending=False)
        
        # Zobrazení tabulky
        st.dataframe(df_totals, use_container_width=True)
        
        # Výpočet celkových součtů
        total_expenses = sum(data['Výdaj'] for data in totals.values())
        total_income = sum(data['Příjem'] for data in totals.values())
        total_balance = total_income - total_expenses
        
        # Zobrazení celkových součtů
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Celkové výdaje", f"{total_expenses:,.0f} Kč")
        with col2:
            st.metric("Celkové příjmy", f"{total_income:,.0f} Kč")
        with col3:
            st.metric("Celková bilance", f"{total_balance:,.0f} Kč")
    else:
        st.info("Zatím nejsou žádné záznamy")

# Hlavní logika aplikace
if "user" not in st.session_state:
    name, authentication_status, user_data = show_login_page()
    if authentication_status and user_data:
        st.session_state["user"] = user_data
        st.session_state["authenticated"] = True
        st.rerun()
elif st.session_state.get("authenticated", False):
    user_data = st.session_state["user"]
    if user_data and "username" in user_data and "name" in user_data:
        show_main_app(user_data["username"], user_data["name"])
    else:
        st.session_state.clear()
        st.rerun()
else:
    st.session_state.clear()
    st.rerun()

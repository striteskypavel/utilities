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
from user_manager import create_user, verify_user, get_user_data, update_user_password
import os
import time

# Konfigurace stránky
st.set_page_config(
    page_title="Finanční aplikace",
    page_icon="💰",
    layout="wide"
)

def show_login_page():
    """Zobrazí přihlašovací stránku"""
    # Vytvoření jednoho sloupce pro centrování obsahu
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("Finanční aplikace")
        st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <p style='font-size: 16px; color: #666;'>
                Jednoduchá aplikace pro sledování osobních financí, 
                plánování rozpočtu a vizualizaci finančních dat.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Přihlašovací formulář
        st.markdown("""
        <div style='text-align: center; padding: 15px; background-color: #ffebee; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h2 style='color: #d32f2f; margin-bottom: 15px; font-size: 20px;'>Přihlášení</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Uživatelské jméno", key="login_username")
            password = st.text_input("Heslo", type="password", key="login_password")
            submit = st.form_submit_button("Přihlásit se", use_container_width=True, type="primary")
            
            if submit:
                success, user_data = verify_user(username, password)
                if success:
                    st.success("Přihlášení úspěšné!")
                    return user_data["name"], True, username
                else:
                    st.error("Nesprávné přihlašovací údaje")
        
        # Registrační formulář
        st.markdown("""
        <div style='text-align: center; padding: 15px; background-color: #ffebee; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h2 style='color: #d32f2f; margin-bottom: 15px; font-size: 20px;'>Registrace nového uživatele</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("register_form"):
            new_username = st.text_input("Uživatelské jméno", key="register_username")
            new_password = st.text_input("Heslo", type="password", key="register_password")
            confirm_password = st.text_input("Potvrzení hesla", type="password", key="confirm_password")
            email = st.text_input("E-mail", key="register_email")
            name = st.text_input("Jméno", key="register_name")
            register = st.form_submit_button("Registrovat", use_container_width=True, type="secondary")
            
            if register:
                if new_password != confirm_password:
                    st.error("Hesla se neshodují")
                else:
                    success, message = create_user(new_username, new_password, email, name)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
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
    page = st.sidebar.radio(
        "Přejít na",
        ["Přehled", "Hypoteční kalkulačka", "Plánování důchodu"]
    )

    if page == "Hypoteční kalkulačka":
        show_mortgage_calculator()
        return
    elif page == "Plánování důchodu":
        show_retirement_planning()
        return

    # Modul pro správu dat
    with st.sidebar.expander("Správa dat", expanded=False):
        st.subheader("Export a import dat")
        
        # Export dat
        st.write("Export dat")
        export_format = st.radio("Formát exportu", ["JSON", "CSV"], horizontal=True)
        
        # Vytvoření dočasného souboru pro export s absolutní cestou
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
                for entry in entries:
                    rows.append({
                        "Kategorie": category,
                        "Částka": entry["amount"],
                        "Datum": entry["date"],
                        "Poznámka": entry.get("note", "")
                    })
            
            df = pd.DataFrame(rows)
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Stáhnout CSV",
                data=csv_data,
                file_name=f"finance_data_{timestamp}.csv",
                mime="text/csv"
            )

        # Import dat
        st.write("Import dat")
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

    # Hlavní obsah aplikace
    st.title("Jednoduchý sledovač financí")

    # Přidání finančních záznamů
    st.subheader("Přidat finanční záznam")

    new_category = st.text_input("Název nové kategorie").strip()
    amount = st.number_input("Částka", min_value=0, step=1000, format="%d")
    
    if st.button("Přidat"):
        if not new_category:
            st.error("Zadejte název kategorie!")
        elif new_category in data:
            st.error(f"Kategorie '{new_category}' již existuje!")
        else:
            add_entry(username, new_category, amount)
            st.success(f"Vytvořena nová kategorie '{new_category}' a přidán záznam!")
            st.rerun()

    # Přehled financí
    st.subheader("Přehled financí")
    
    # Editovatelná tabulka
    totals = {cat: sum(item["amount"] for item in data.get(cat, [])) for cat in data.keys()}
    df = pd.DataFrame({
        "Kategorie": list(totals.keys()),
        "Částka": list(totals.values())
    })

    edited_df = st.data_editor(
        df,
        column_config={
            "Kategorie": st.column_config.TextColumn("Kategorie", disabled=True),
            "Částka": st.column_config.NumberColumn(
                "Částka",
                help="Upravte částku přímo v tabulce",
                min_value=0,
                format="%.0f Kč"
            )
        },
        use_container_width=True,
        hide_index=True
    )

    if not df["Částka"].equals(edited_df["Částka"]):
        for idx, row in edited_df.iterrows():
            category = row["Kategorie"]
            new_amount = row["Částka"]
            old_amount = totals[category]
            
            if new_amount != old_amount:
                if data[category]:
                    data[category][-1]["amount"] = new_amount
                    save_data(username, data)
                    log_change(category, old_amount, new_amount)
                    st.success(f"Částka pro kategorii '{category}' byla aktualizována!")
                    st.rerun()

    # Vizualizace dat
    st.header("Vizualizace dat")
    viz_tabs = st.tabs(["Rozložení financí", "Historie změn", "Porovnání kategorií"])

    with viz_tabs[0]:
        st.subheader("Rozložení financí")
        totals = {cat: sum(item["amount"] for item in items) for cat, items in data.items()}
        show_pie_chart(totals, height=600)

    with viz_tabs[1]:
        st.subheader("Historie změn")
        show_history_chart(history, height=600)

    with viz_tabs[2]:
        st.subheader("Porovnání kategorií")
        show_category_comparison(data, height=600)

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

# Hlavní logika aplikace
if "user" not in st.session_state:
    name, authentication_status, username = show_login_page()
    if authentication_status and username:
        st.session_state["user"] = get_user_data(username)
        st.rerun()
else:
    user_data = st.session_state["user"]
    show_main_app(user_data["username"], user_data["name"])

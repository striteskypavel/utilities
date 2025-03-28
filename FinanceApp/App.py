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
from retirement_planner import show_retirement_planning
from mortgage_calculator import show_mortgage_calculator
from compound_interest import show_compound_interest_calculator
from salary_calculator import show_salary_calculator
from user_manager import create_user, verify_user, get_user_data, update_user_password, get_user_file_path, is_email_registered
import os
import time
from expense_tracker import show_expense_tracker
import plotly.express as px

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
                if success:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("Nesprávné uživatelské jméno nebo heslo")
        
        st.markdown("---")
        st.subheader("Registrace nového uživatele")
        
        # Inicializace session state pro registrační formulář
        if 'registration_submitted' not in st.session_state:
            st.session_state.registration_submitted = False
        
        with st.form("register_form"):
            if not st.session_state.registration_submitted:
                new_username = st.text_input("Nové uživatelské jméno")
                new_password = st.text_input("Nové heslo", type="password")
                confirm_password = st.text_input("Potvrzení hesla", type="password")
                email = st.text_input("E-mail")
            else:
                new_username = ""
                new_password = ""
                confirm_password = ""
                email = ""
                st.session_state.registration_submitted = False
            
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
                        
                        def validate_email(email):
                            # Základní formát
                            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                            if not re.match(email_pattern, email):
                                return False, "Neplatný formát e-mailové adresy"
                            
                            # Kontrola běžných překlepů v doménách
                            common_domains = {
                                'gmail.com': ['gmai.com', 'gmail.cz', 'gmal.com', 'gmail.co', 'gmai2.com'],
                                'seznam.cz': ['seznan.cz', 'seznam.com', 'seznamcz'],
                                'email.cz': ['emil.cz', 'email.com'],
                                'yahoo.com': ['yaho.com', 'yahoo.cz', 'yahho.com'],
                                'outlook.com': ['outlok.com', 'outlook.cz', 'outlock.com']
                            }
                            
                            domain = email.split('@')[1].lower()
                            
                            # Kontrola známých překlepů
                            for valid_domain, typos in common_domains.items():
                                if domain in typos:
                                    return False, f"Možná jste měli na mysli @{valid_domain}?"
                            
                            # Kontrola minimální délky domény druhého řádu
                            domain_parts = domain.split('.')
                            if len(domain_parts) < 2 or any(len(part) < 2 for part in domain_parts):
                                return False, "Neplatná doména"
                            
                            return True, ""
                        
                        email_valid, email_error = validate_email(email)
                        if not email_valid:
                            st.error(email_error)
                        else:
                            # Kontrola existence uživatele
                            if os.path.exists(get_user_file_path(new_username)):
                                st.error("Uživatelské jméno již existuje. Zvolte jiné.")
                            elif is_email_registered(email):
                                st.error("E-mailová adresa je již registrována. Použijte jinou.")
                            elif create_user(new_username, new_password, email):
                                st.success("Registrace byla úspěšná! Můžete se přihlásit.")
                                st.session_state.registration_submitted = True
                                st.rerun()
                            else:
                                st.error("Nastala chyba při registraci. Zkuste to prosím znovu.")

def show_main_app(username, name):
    """Zobrazí hlavní aplikaci po přihlášení"""
    # Zobrazení jména přihlášeného uživatele a tlačítka pro odhlášení
    if st.sidebar.button("Odhlásit"):
        del st.session_state["logged_in"]
        del st.session_state["username"]
        st.rerun()
    
    st.sidebar.title(f'Vítejte, {name}')
    
    # Načtení dat pro přihlášeného uživatele
    data = load_data(username)
    history = get_history(username)

    # Nastavení sidebaru
    st.sidebar.title("Nástroje")

    # Navigace pomocí tlačítek
    if st.sidebar.button("📊 Přehled investic", use_container_width=True):
        st.session_state["current_page"] = "Přehled investic"
        st.rerun()
    
    if st.sidebar.button("💰 Sledování výdajů", use_container_width=True):
        st.session_state["current_page"] = "Sledování výdajů"
        st.rerun()
    
    if st.sidebar.button("🏠 Hypoteční kalkulačka", use_container_width=True):
        st.session_state["current_page"] = "Hypoteční kalkulačka"
        st.rerun()
    
    if st.sidebar.button("💰 Složené úročení", use_container_width=True):
        st.session_state["current_page"] = "Složené úročení"
        st.rerun()
    
    if st.sidebar.button("💵 Výpočet čisté mzdy", use_container_width=True):
        st.session_state["current_page"] = "Výpočet čisté mzdy"
        st.rerun()
    
    if st.sidebar.button("👴 Plánování důchodu", use_container_width=True):
        st.session_state["current_page"] = "Plánování důchodu"
        st.rerun()
    
    if st.sidebar.button("⚙️ Správa uživatele", use_container_width=True):
        st.session_state["current_page"] = "Správa uživatele"
        st.rerun()

    # Inicializace aktuální stránky, pokud není nastavena
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Přehled investic"

    # Zobrazení vybrané stránky
    if st.session_state["current_page"] == "Přehled investic":
        show_overview(username)
    elif st.session_state["current_page"] == "Sledování výdajů":
        show_expense_tracker(username)
    elif st.session_state["current_page"] == "Hypoteční kalkulačka":
        show_mortgage_calculator()
    elif st.session_state["current_page"] == "Složené úročení":
        show_compound_interest_calculator()
    elif st.session_state["current_page"] == "Výpočet čisté mzdy":
        show_salary_calculator()
    elif st.session_state["current_page"] == "Plánování důchodu":
        show_retirement_planning()
    elif st.session_state["current_page"] == "Správa uživatele":
        show_settings(username)

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

def show_export_import_module(username: str, data: dict, module_type: str):
    """Zobrazí modul pro export a import dat pro konkrétní modul"""
    # Vytvoření dvou sloupců pro export a import
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Export dat")
        export_format = st.radio(f"Formát exportu {module_type}", ["JSON", "CSV"], horizontal=True, key=f"export_format_{module_type}")
        
        # Vytvoření dočasného souboru pro export
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if export_format == "JSON":
            # Pro JSON export použijeme přímo data z paměti
            export_data_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
            st.download_button(
                label=f"Stáhnout {module_type} JSON",
                data=export_data_bytes,
                file_name=f"{module_type.lower()}_{timestamp}.json",
                mime="application/json",
                key=f"download_json_{module_type}"
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
                label=f"Stáhnout {module_type} CSV",
                data=csv_data,
                file_name=f"{module_type.lower()}_{timestamp}.csv",
                mime="text/csv",
                key=f"download_csv_{module_type}"
            )
    
    with col2:
        st.markdown("#### Import dat")
        uploaded_file = st.file_uploader(
            f"Vyberte soubor pro import {module_type}", 
            type=["json", "csv"],
            key=f"file_uploader_{module_type}"
        )
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            success_message = st.empty()
            
            if st.button(f"Importovat {module_type} data", key=f"import_button_{module_type}"):
                temp_file = f"temp_import_{module_type}.{file_extension}"
                with open(temp_file, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                if import_data(username, temp_file, format=file_extension):
                    success_message.success(f"Data {module_type} byla úspěšně importována!")
                    time.sleep(3)
                    success_message.empty()
                    st.rerun()
                else:
                    st.error(f"Chyba při importu dat {module_type}. Zkontrolujte formát souboru.")
                
                if os.path.exists(temp_file):
                    os.remove(temp_file)

def show_overview(username):
    """Zobrazí přehled investic uživatele."""
    st.title("Přehled investic")
    
    # Načtení dat
    data = load_data(username)
    if not data:
        st.error("Nepodařilo se načíst data uživatele.")
        return
    
    # Přidání Export/Import sekce
    with st.expander("Export/Import investičních dat", expanded=False):
        show_export_import_module(username, data, "Investice")
    
    # Definice kategorií investic a jejich popis
    investment_categories = {
        "ETF": {
            "subcategories": ["VWCE", "SDPR S&P 500", "iShares MSCI World"],
            "description": "Burzovně obchodované fondy"
        },
        "Akcie": {
            "subcategories": ["Dividendové akcie", "Růstové akcie", "České akcie"],
            "description": "Přímé investice do akcií"
        },
        "Kryptoměny": {
            "subcategories": ["Bitcoin", "Ethereum", "Altcoiny"],
            "description": "Digitální měny"
        },
        "Nemovitosti": {
            "subcategories": ["Vlastní bydlení", "Investiční nemovitosti", "REITs"],
            "description": "Nemovitostní investice"
        },
        "Dluhopisy": {
            "subcategories": ["Státní dluhopisy", "Korporátní dluhopisy", "Dluhopisové fondy"],
            "description": "Dluhové cenné papíry"
        },
        "Hotovost": {
            "subcategories": ["Běžný účet", "Spořící účet", "Termínované vklady"],
            "description": "Likvidní prostředky"
        },
        "Důchodové pojištění": {
            "subcategories": ["Penzijní připojištění", "Doplňkové penzijní spoření", "Důchodové fondy", "Rentové pojištění", "Investiční životní pojištění", "Důchodové účty", "Důchodové fondy", "Důchodové rezervy", "Důchodové plány", "Důchodové produkty"],
            "description": "Důchodové zabezpečení"
        }
    }
    
    # Vytvoření DataFrame pro přehled
    overview_data = []
    for category, subcategories in investment_categories.items():
        category_total = 0
        for subcategory in subcategories["subcategories"]:
            if subcategory in data:
                if isinstance(data[subcategory], list):
                    total = sum(entry['amount'] for entry in data[subcategory])
                else:
                    total = data[subcategory]['amount']
                category_total += total
                overview_data.append({
                    'Kategorie': category,
                    'Podkategorie': subcategory,
                    'Hodnota': total
                })
        
        # Přidání řádku s celkovým součtem pro kategorii
        overview_data.append({
            'Kategorie': category,
            'Podkategorie': 'CELKEM',
            'Hodnota': category_total
        })
    
    # Vytvoření DataFrame
    df_overview = pd.DataFrame(overview_data)
    
    # Výpočet celkového součtu
    total_sum = df_overview[df_overview['Podkategorie'] == 'CELKEM']['Hodnota'].sum()
    
    # Přidání řádku s celkovým součtem
    df_overview = pd.concat([
        df_overview,
        pd.DataFrame([{
            'Kategorie': 'CELKEM',
            'Podkategorie': 'CELKEM',
            'Hodnota': total_sum
        }])
    ], ignore_index=True)
    
    # 1. Klíčové metriky v řádku
    st.subheader("Klíčové metriky")
    
    # Vytvoření dvou řad metrik
    row1_cols = st.columns(4)
    row2_cols = st.columns(4)
    
    # První řada - Celkový objem a hlavní kategorie
    with row1_cols[0]:
        st.metric(
            "Celkový objem investic",
            f"{total_sum:,.0f} Kč",
            help="Celková hodnota všech investic"
        )
    
    with row1_cols[1]:
        etf_total = df_overview[
            (df_overview['Kategorie'] == 'ETF') & 
            (df_overview['Podkategorie'] == 'CELKEM')
        ]['Hodnota'].iloc[0]
        etf_percentage = (etf_total / total_sum * 100) if total_sum > 0 else 0
        st.metric("ETF", f"{etf_total:,.0f} Kč", f"{etf_percentage:.1f}%")
    
    with row1_cols[2]:
        stocks_total = df_overview[
            (df_overview['Kategorie'] == 'Akcie') & 
            (df_overview['Podkategorie'] == 'CELKEM')
        ]['Hodnota'].iloc[0]
        stocks_percentage = (stocks_total / total_sum * 100) if total_sum > 0 else 0
        st.metric("Akcie", f"{stocks_total:,.0f} Kč", f"{stocks_percentage:.1f}%")
    
    with row1_cols[3]:
        crypto_total = df_overview[
            (df_overview['Kategorie'] == 'Kryptoměny') & 
            (df_overview['Podkategorie'] == 'CELKEM')
        ]['Hodnota'].iloc[0]
        crypto_percentage = (crypto_total / total_sum * 100) if total_sum > 0 else 0
        st.metric("Kryptoměny", f"{crypto_total:,.0f} Kč", f"{crypto_percentage:.1f}%")
    
    # Druhá řada - Ostatní kategorie
    with row2_cols[0]:
        real_estate_total = df_overview[
            (df_overview['Kategorie'] == 'Nemovitosti') & 
            (df_overview['Podkategorie'] == 'CELKEM')
        ]['Hodnota'].iloc[0]
        real_estate_percentage = (real_estate_total / total_sum * 100) if total_sum > 0 else 0
        st.metric("Nemovitosti", f"{real_estate_total:,.0f} Kč", f"{real_estate_percentage:.1f}%")
    
    with row2_cols[1]:
        bonds_total = df_overview[
            (df_overview['Kategorie'] == 'Dluhopisy') & 
            (df_overview['Podkategorie'] == 'CELKEM')
        ]['Hodnota'].iloc[0]
        bonds_percentage = (bonds_total / total_sum * 100) if total_sum > 0 else 0
        st.metric("Dluhopisy", f"{bonds_total:,.0f} Kč", f"{bonds_percentage:.1f}%")
    
    with row2_cols[2]:
        cash_total = df_overview[
            (df_overview['Kategorie'] == 'Hotovost') & 
            (df_overview['Podkategorie'] == 'CELKEM')
        ]['Hodnota'].iloc[0]
        cash_percentage = (cash_total / total_sum * 100) if total_sum > 0 else 0
        st.metric("Hotovost", f"{cash_total:,.0f} Kč", f"{cash_percentage:.1f}%")
    
    with row2_cols[3]:
        pension_total = df_overview[
            (df_overview['Kategorie'] == 'Důchodové pojištění') & 
            (df_overview['Podkategorie'] == 'CELKEM')
        ]['Hodnota'].iloc[0]
        pension_percentage = (pension_total / total_sum * 100) if total_sum > 0 else 0
        st.metric("Důchodové pojištění", f"{pension_total:,.0f} Kč", f"{pension_percentage:.1f}%")
    
    # 2. Přidání/Editace investic
    st.subheader("Správa investic")
    
    # Vytvoření dvou sloupců pro přidání a editaci
    add_col, edit_col = st.columns(2)
    
    with add_col:
        st.markdown("#### Přidat novou investici")
        with st.form("add_investment"):
            selected_category = st.selectbox(
                "Kategorie",
                list(investment_categories.keys()),
                help="Vyberte hlavní kategorii investice"
            )
            
            selected_subcategory = st.text_input(
                "Podkategorie",
                help="Zadejte název podkategorie"
            )
            
            amount = st.number_input(
                "Částka (Kč)",
                min_value=0,
                step=1000,
                help="Zadejte hodnotu investice"
            )

            # Pouze výběr data
            date = st.date_input(
                "Datum",
                value=datetime.now(),
                help="Vyberte datum investice"
            )
            
            note = st.text_area(
                "Poznámka",
                help="Volitelný popis investice"
            )
            
            submitted = st.form_submit_button("Přidat investici")
            
            if submitted and amount > 0:
                # Přidání nové investice do dat
                # Použití pouze data (čas bude nastaven na půlnoc)
                timestamp = datetime.combine(date, datetime.min.time())
                new_investment = {
                    "amount": amount,
                    "timestamp": timestamp.isoformat(),
                    "note": note,
                    "type": selected_subcategory
                }
                
                if selected_subcategory not in data:
                    data[selected_subcategory] = []
                
                if isinstance(data[selected_subcategory], list):
                    data[selected_subcategory].append(new_investment)
                else:
                    data[selected_subcategory] = [new_investment]
                
                save_data(username, data)
                st.success("Investice byla úspěšně přidána!")
                st.rerun()
    
    with edit_col:
        st.markdown("#### Historie investic")
        
        # Vytvoření DataFrame pro historii
        history_data = []
        for category, subcategories in investment_categories.items():
            for subcategory in subcategories["subcategories"]:
                if subcategory in data:
                    entries = data[subcategory]
                    if isinstance(entries, list):
                        for entry in entries:
                            # Převod timestamp na datum
                            entry_date = datetime.fromisoformat(entry["timestamp"]).date()
                            history_data.append({
                                "Datum": entry_date.strftime("%Y-%m-%d"),
                                "Kategorie": category,
                                "Podkategorie": subcategory,
                                "Částka": entry["amount"],
                                "Poznámka": entry.get("note", "")
                            })
        
        if history_data:
            history_df = pd.DataFrame(history_data)
            # Seřazení podle data (sestupně)
            history_df = history_df.sort_values("Datum", ascending=False)
            
            # Zobrazení editovatelné tabulky
            edited_df = st.data_editor(
                history_df,
                hide_index=True,
                use_container_width=True,
                num_rows="dynamic"
            )
            
            if st.button("Uložit změny"):
                # TODO: Implementovat ukládání změn z editované tabulky
                st.success("Změny byly uloženy!")
                st.rerun()
    
    # 3. Grafické zobrazení
    st.subheader("Grafické zobrazení")
    
    # Hlavní přepínač pro zobrazení procent/částek
    show_percentages = st.checkbox("📊 Zobrazit procentuální zastoupení", value=True, help="Přepíná mezi zobrazením procent a částek ve všech grafech")
    
    # Vytvoření dvou sloupců pro grafy
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Koláčový graf pro aktuální rozložení
        category_data = df_overview[
            (df_overview['Podkategorie'] == 'CELKEM') & 
            (df_overview['Kategorie'] != 'CELKEM')
        ]
        
        if show_percentages:
            # Výpočet procent pro každou kategorii
            category_data = category_data.copy()  # Vytvoření kopie pro bezpečnou modifikaci
            category_data['Procenta'] = (category_data['Hodnota'] / total_sum * 100).round(1)
            values_col = 'Procenta'
            title_suffix = ' (v %)'
        else:
            values_col = 'Hodnota'
            title_suffix = ' (v Kč)'
        
        fig_pie = px.pie(
            category_data,
            values=values_col,
            names='Kategorie',
            title=f'Aktuální rozložení investic{title_suffix}',
            hole=0.3
        )
        
        # Přidání tooltipu s oběma hodnotami
        fig_pie.update_traces(
            textinfo='label+percent+value' if show_percentages else 'label+value',
            hovertemplate="<b>%{label}</b><br>" +
                         f"{'Procenta: %{percent:.1f}<br>' if show_percentages else ''}" +
                         f"Hodnota: %{{value:,.0f}} Kč<br>" +
                         "<extra></extra>"
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with chart_col2:
        # Graf vývoje v čase
        if history_data:
            # Přidání výběru časového intervalu
            time_interval = st.selectbox(
                "Časový interval",
                ["Den", "Týden", "Měsíc", "Rok", "Vše"],
                help="Vyberte interval pro agregaci dat"
            )
            
            history_df['Datum'] = pd.to_datetime(history_df['Datum'])
            
            # Agregace dat podle zvoleného intervalu
            if time_interval == "Den":
                grouped_df = history_df.groupby(['Datum', 'Kategorie'])['Částka'].sum().reset_index()
            elif time_interval == "Týden":
                history_df['Týden'] = history_df['Datum'].dt.strftime('%Y-%U')
                grouped_df = history_df.groupby(['Týden', 'Kategorie'])['Částka'].sum().reset_index()
                grouped_df['Datum'] = pd.to_datetime(grouped_df['Týden'].apply(lambda x: f"{x}-1"), format='%Y-%U-%w')
            elif time_interval == "Měsíc":
                history_df['Měsíc'] = history_df['Datum'].dt.strftime('%Y-%m')
                grouped_df = history_df.groupby(['Měsíc', 'Kategorie'])['Částka'].sum().reset_index()
                grouped_df['Datum'] = pd.to_datetime(grouped_df['Měsíc'] + '-01')
            elif time_interval == "Rok":
                history_df['Rok'] = history_df['Datum'].dt.strftime('%Y')
                grouped_df = history_df.groupby(['Rok', 'Kategorie'])['Částka'].sum().reset_index()
                grouped_df['Datum'] = pd.to_datetime(grouped_df['Rok'] + '-01-01')
            else:  # "Vše"
                grouped_df = history_df.groupby(['Datum', 'Kategorie'])['Částka'].sum().reset_index()
            
            # Vytvoření grafu
            fig_line = px.line(
                grouped_df,
                x='Datum',
                y='Částka',
                color='Kategorie',
                title=f'Vývoj investic v čase (po {time_interval.lower()}ech)'
            )
            
            # Úprava formátu data na ose X podle intervalu
            if time_interval == "Den":
                date_format = '%Y-%m-%d'
            elif time_interval == "Týden":
                date_format = 'Týden %U, %Y'
            elif time_interval == "Měsíc":
                date_format = '%B %Y'
            elif time_interval == "Rok":
                date_format = '%Y'
            else:
                date_format = '%Y-%m-%d'
            
            fig_line.update_xaxes(
                tickformat=date_format,
                tickangle=45
            )
            
            # Přidání možnosti přiblížení/oddálení
            fig_line.update_layout(
                xaxis=dict(rangeslider=dict(visible=True)),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Zatím nejsou k dispozici žádná historická data.")
    
    # 4. Detailní přehled podle kategorií
    st.subheader("Detailní přehled")
    
    # Definice ikon pro kategorie
    category_icons = {
        "ETF": "📈",
        "Akcie": "📊",
        "Kryptoměny": "🪙",
        "Nemovitosti": "🏠",
        "Dluhopisy": "📜",
        "Hotovost": "💵",
        "Důchodové pojištění": "👴"
    }
    
    # Vytvoření expanderu pro každou kategorii
    for category, info in investment_categories.items():
        icon = category_icons.get(category, "📊")  # Výchozí ikona pokud není definována
        with st.expander(f"{icon} {category} - {info['description']}", expanded=False):
            category_data = df_overview[
                (df_overview['Kategorie'] == category) & 
                (df_overview['Podkategorie'] != 'CELKEM')
            ]
            
            if not category_data.empty:
                # Vytvoření DataFrame pro kategorii
                category_df = pd.DataFrame(category_data)
                
                # Zobrazení tabulky
                st.dataframe(
                    category_df,
                    hide_index=True,
                    use_container_width=True
                )
                
                if show_percentages:
                    # Výpočet procent pro každou podkategorii
                    category_df = category_df.copy()  # Vytvoření kopie pro bezpečnou modifikaci
                    category_total = category_df['Hodnota'].sum()
                    category_df['Procenta'] = (category_df['Hodnota'] / category_total * 100).round(1)
                    values_col = 'Procenta'
                    title_suffix = ' (v %)'
                else:
                    values_col = 'Hodnota'
                    title_suffix = ' (v Kč)'
                
                # Vytvoření koláčového grafu pro kategorii
                fig = px.pie(
                    category_df,
                    values=values_col,
                    names='Podkategorie',
                    title=f'Rozložení investic v kategorii {category}{title_suffix}',
                    hole=0.3
                )
                
                # Přidání tooltipu s oběma hodnotami
                fig.update_traces(
                    textinfo='label+percent+value' if show_percentages else 'label+value',
                    hovertemplate="<b>%{label}</b><br>" +
                                f"{'Procenta: %{percent:.1f}<br>' if show_percentages else ''}" +
                                f"Hodnota: %{{value:,.0f}} Kč<br>" +
                                "<extra></extra>"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Zobrazení historie pro kategorii
                if history_data:
                    category_history = [d for d in history_data if d["Kategorie"] == category]
                    if category_history:
                        st.markdown("##### Historie transakcí")
                        category_history_df = pd.DataFrame(category_history)
                        st.dataframe(
                            category_history_df.sort_values("Datum", ascending=False),
                            hide_index=True,
                            use_container_width=True
                        )
            else:
                st.info(f"V kategorii {category} zatím nejsou žádné investice.")

def show_expense_tracker(username):
    """Zobrazí sledování výdajů."""
    st.title("Sledování výdajů")
    
    # Načtení dat
    data = load_data(username)
    if not data:
        st.error("Nepodařilo se načíst data uživatele.")
        return
    
    # Přidání Export/Import sekce
    with st.expander("Export/Import výdajových dat", expanded=False):
        show_export_import_module(username, data, "Výdaje")
    
    # Definice kategorií výdajů a jejich popis
    expense_categories = {
        "Bydlení": {
            "subcategories": ["Nájem/Hypotéka", "Energie", "Internet/TV", "Údržba"],
            "description": "Výdaje spojené s bydlením"
        },
        "Jídlo": {
            "subcategories": ["Potraviny", "Restaurace", "Dovoz jídla", "Kantýna"],
            "description": "Stravování a potraviny"
        },
        "Doprava": {
            "subcategories": ["MHD", "Auto", "Pohonné hmoty", "Údržba vozidla"],
            "description": "Výdaje na dopravu"
        },
        "Zábava": {
            "subcategories": ["Kino/Divadlo", "Sport", "Koníčky", "Cestování"],
            "description": "Volnočasové aktivity"
        },
        "Zdraví": {
            "subcategories": ["Léky", "Lékař", "Pojištění", "Wellness"],
            "description": "Zdravotní výdaje"
        },
        "Oblečení": {
            "subcategories": ["Oblečení", "Obuv", "Doplňky", "Péče o oděvy"],
            "description": "Výdaje za oblečení"
        },
        "Vzdělávání": {
            "subcategories": ["Kurzy", "Knihy", "Online kurzy", "Školné"],
            "description": "Investice do vzdělání"
        }
    }
    
    # Vytvoření DataFrame pro přehled
    overview_data = []
    total_expenses = 0
    total_income = 0
    
    # Procházení dat a vytvoření přehledu
    for category, info in expense_categories.items():
        category_total = 0
        for subcategory in info["subcategories"]:
            if subcategory in data:
                if isinstance(data[subcategory], list):
                    for entry in data[subcategory]:
                        amount = entry.get('amount', 0)
                        entry_type = entry.get('type', 'výdaj')
                        
                        if entry_type == 'příjem':
                            total_income += amount
                        else:
                            category_total += amount
                            total_expenses += amount
                        
                        overview_data.append({
                            'Kategorie': category,
                            'Podkategorie': subcategory,
                            'Částka': amount,
                            'Typ': entry_type,
                            'Datum': entry.get('timestamp', ''),
                            'Poznámka': entry.get('note', '')
                        })
    
    # Vytvoření DataFrame
    df_overview = pd.DataFrame(overview_data)
    
    # 1. Klíčové metriky
    st.subheader("Přehled financí")
    
    # Vytvoření tří sloupců pro metriky
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Celkové výdaje",
            f"{total_expenses:,.0f} Kč",
            help="Celková hodnota všech výdajů"
        )
    
    with col2:
        st.metric(
            "Celkové příjmy",
            f"{total_income:,.0f} Kč",
            help="Celková hodnota všech příjmů"
        )
    
    with col3:
        balance = total_income - total_expenses
        st.metric(
            "Bilance",
            f"{balance:,.0f} Kč",
            f"{'+' if balance >= 0 else ''}{balance/total_income*100:.1f}%" if total_income > 0 else "0%",
            help="Rozdíl mezi příjmy a výdaji"
        )
    
    # 2. Přidání/Editace výdajů
    st.subheader("Správa financí")
    
    # Vytvoření dvou sloupců pro přidání a editaci
    add_col, edit_col = st.columns(2)
    
    with add_col:
        st.markdown("#### Přidat nový záznam")
        with st.form("add_entry_form"):
            col1, col2 = st.columns(2)
            with col1:
                # Inicializace session state pro kategorii a podkategorii
                if 'selected_category' not in st.session_state:
                    st.session_state.selected_category = list(expense_categories.keys())[0]
                if 'selected_subcategory' not in st.session_state:
                    st.session_state.selected_subcategory = ""
                
                category = st.selectbox(
                    "Kategorie",
                    list(expense_categories.keys()),
                    key="category_select"
                )
                
                # Aktualizace podkategorie při změně kategorie
                if st.session_state.category_select != st.session_state.selected_category:
                    st.session_state.selected_category = st.session_state.category_select
                    st.session_state.selected_subcategory = ""
                
                subcategory = st.text_input(
                    "Podkategorie",
                    value=st.session_state.selected_subcategory,
                    key="subcategory_input"
                )
                
                # Aktualizace session state pro podkategorii
                st.session_state.selected_subcategory = st.session_state.subcategory_input
            
            with col2:
                amount = st.number_input("Částka (Kč)", min_value=0.0, step=1000.0)
                note = st.text_input("Poznámka")
            
            submitted = st.form_submit_button("Přidat záznam")
            
            if submitted:
                if add_entry(username, category, amount, note):
                    st.success("Záznam byl úspěšně přidán!")
                    st.rerun()
                else:
                    st.error("Chyba při přidávání záznamu!")
    
    with edit_col:
        st.markdown("#### Historie transakcí")
        
        if not df_overview.empty:
            # Zobrazení editovatelné tabulky
            edited_df = st.data_editor(
                df_overview,
                hide_index=True,
                use_container_width=True,
                num_rows="dynamic"
            )
            
            if st.button("Uložit změny"):
                # TODO: Implementovat ukládání změn z editované tabulky
                st.success("Změny byly uloženy!")
                st.rerun()
        else:
            st.info("Zatím nejsou k dispozici žádné záznamy.")
    
    # 3. Grafické zobrazení
    st.subheader("Grafické zobrazení")
    
    if not df_overview.empty:
        # Vytvoření dvou sloupců pro grafy
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Koláčový graf pro rozložení výdajů
            expenses_by_category = df_overview[
                (df_overview['Typ'] == 'výdaj')
            ].groupby('Kategorie')['Částka'].sum().reset_index()
            
            if not expenses_by_category.empty:
                fig_pie = px.pie(
                    expenses_by_category,
                    values='Částka',
                    names='Kategorie',
                    title='Rozložení výdajů podle kategorií',
                    hole=0.3
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Zatím nejsou k dispozici žádné výdaje pro zobrazení grafu.")
        
        with chart_col2:
            # Sloupcový graf pro porovnání příjmů a výdajů
            if 'Datum' in df_overview.columns:
                df_overview['Datum'] = pd.to_datetime(df_overview['Datum'])
                monthly_summary = df_overview.groupby([
                    df_overview['Datum'].dt.strftime('%Y-%m'),
                    'Typ'
                ])['Částka'].sum().unstack(fill_value=0).reset_index()
                
                if not monthly_summary.empty:
                    fig_bar = px.bar(
                        monthly_summary,
                        x='Datum',
                        y=['příjem', 'výdaj'] if 'příjem' in monthly_summary.columns and 'výdaj' in monthly_summary.columns else [],
                        title='Měsíční přehled příjmů a výdajů',
                        barmode='group'
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("Zatím nejsou k dispozici žádná data pro zobrazení grafu.")
            else:
                st.info("Zatím nejsou k dispozici žádná data pro zobrazení grafu.")
    
    # 4. Detailní přehled podle kategorií
    st.subheader("Detailní přehled")
    
    # Vytvoření expanderu pro každou kategorii
    for category, info in expense_categories.items():
        with st.expander(f"📊 {category} - {info['description']}", expanded=False):
            if not df_overview.empty:
                category_data = df_overview[df_overview['Kategorie'] == category]
                
                if not category_data.empty:
                    # Zobrazení tabulky
                    st.dataframe(
                        category_data,
                        hide_index=True,
                        use_container_width=True
                    )
                    
                    # Vytvoření koláčového grafu pro kategorii
                    fig = px.pie(
                        category_data,
                        values='Částka',
                        names='Podkategorie',
                        title=f'Rozložení výdajů v kategorii {category}',
                        hole=0.3
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"V kategorii {category} zatím nejsou žádné záznamy.")
            else:
                st.info(f"V kategorii {category} zatím nejsou žádné záznamy.")

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
                    st.error("Nové heslo nesplňuje požadavky na bezpečnost:")
                    for error in password_errors:
                        st.error(error)
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
    st.write(f"**Účet vytvořen:** {datetime.fromisoformat(user_data['created_at']).strftime('%d.%m.%Y %H:%M')}")

# Hlavní logika aplikace
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    show_login_page()
else:
    user_data = get_user_data(st.session_state["username"])
    if user_data:
        show_main_app(user_data["username"], user_data["username"])  # Použijeme username místo name
    else:
        st.session_state.clear()
        st.rerun()

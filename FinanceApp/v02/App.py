import streamlit as st
import pandas as pd
import json
from datetime import datetime
from data_manager import DataManager
from visualizations import (
    show_pie_chart, show_history_chart, 
    show_category_comparison
)
from history_manager import log_change, load_history, clear_history, delete_history_entries
from config import DEFAULT_CATEGORIES
from retirement_planning import show_retirement_planning
from mortgage_calculator import show_mortgage_calculator
from compound_interest import show_compound_interest_calculator
from salary_calculator import show_salary_calculator
from user_manager import (
    create_user, verify_user, get_user_data, update_user_password,
    get_user_file_path, is_email_registered, create_session_cookie,
    get_session_cookie, clear_session_cookie
)
import os
import time
from expense_tracker import show_expense_tracker
import plotly.express as px
import plotly.graph_objects as go
from werkzeug.security import check_password_hash, generate_password_hash

# Konfigurace stránky
st.set_page_config(
    page_title="Finance Tracker",
    page_icon="📊",
    layout="wide"
)

# Inicializace DataManager
data_manager = DataManager()

# Inicializace session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(time.time())

def login_page():
    st.title("Přihlášení")
    
    with st.form("login_form"):
        username = st.text_input("Uživatelské jméno")
        password = st.text_input("Heslo", type="password")
        submit = st.form_submit_button("Přihlásit se")
        
        if submit:
            if data_manager.verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Přihlášení úspěšné!")
                st.rerun()
            else:
                st.error("Nesprávné přihlašovací údaje!")

def register_page():
    st.title("Registrace")
    
    with st.form("register_form"):
        username = st.text_input("Uživatelské jméno")
        password = st.text_input("Heslo", type="password")
        email = st.text_input("Email")
        submit = st.form_submit_button("Registrovat se")
        
        if submit:
            if data_manager.create_user(username, password, email):
                st.success("Registrace úspěšná! Můžete se přihlásit.")
                st.rerun()
            else:
                st.error("Uživatelské jméno již existuje!")

def show_logout():
    """Zobrazí odhlašovací tlačítko."""
    if st.sidebar.button("Odhlásit se"):
        # Vyčištění session state
        st.session_state.pop("username", None)
        st.session_state.pop("logged_in", None)
        st.session_state.pop("session_id", None)
        st.rerun()

def show_main_app(username, name):
    """Zobrazí hlavní aplikaci po přihlášení"""
    # Zobrazení jména přihlášeného uživatele a tlačítka pro odhlášení
    if st.sidebar.button("Odhlásit"):
        del st.session_state["logged_in"]
        del st.session_state["username"]
        st.rerun()
    
    st.sidebar.title(f'Vítejte, {name}')
    
    # Načtení dat pro přihlášeného uživatele
    data = data_manager.load_data(username)
    history = data_manager.get_history(username)

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
        show_investment_overview(username)
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
                
                if data_manager.import_data(username, temp_file, format=file_extension):
                    success_message.success(f"Data {module_type} byla úspěšně importována!")
                    time.sleep(3)
                    success_message.empty()
                    st.rerun()
                else:
                    st.error(f"Chyba při importu dat {module_type}. Zkontrolujte formát souboru.")
                
                if os.path.exists(temp_file):
                    os.remove(temp_file)

def show_investment_overview(username):
    """Zobrazení přehledu investic"""
    st.title("Přehled investic")
    
    # Načtení existujících investic
    investments = data_manager.load_investments(username)
    
    # Formulář pro přidání nové investice
    st.subheader("1. Přidat novou investici")
    
    # Formulář pro přidání investice
    with st.form("add_investment_form"):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input(
                "Částka (Kč)", 
                min_value=0.0, 
                value=0.0, 
                step=1000.0,
                help="Zadejte částku v Kč. Použijte čísla bez mezer a speciálních znaků."
            )
            investment_type = st.selectbox(
                "Typ investice",
                options=[
                    "Kryptoměny",
                    "P2P půjčky",
                    "ETF a akcie",
                    "Doplňkové penzijní spoření",
                    "Investiční platformy",
                    "Spoření na cíl",
                    "Nemovitosti",
                    "Hotovost a běžné účty",
                    "Konzervativní investice",
                    "Ostatní"
                ],
                help="Vyberte kategorii vaší investice"
            )
        
        with col2:
            name = st.text_input(
                "Název",
                help="Zadejte název investice (např. 'Bitcoin', 'ETF World', 'Byt Praha')"
            )
            date = st.date_input(
                "Datum",
                help="Vyberte datum investice"
            )
            note = st.text_input(
                "Poznámka",
                help="Volitelná poznámka k investici"
            )
        
        submitted = st.form_submit_button("Přidat")
        if submitted:
            if amount > 0 and name:
                new_investment = {
                    "amount": amount,
                    "type": investment_type,
                    "name": name,
                    "date": date.strftime("%Y-%m-%d"),
                    "note": note
                }
                investments.append(new_investment)
                data_manager.save_investments(username, investments)
                st.success("Investice byla úspěšně přidána!")
                st.rerun()
            else:
                st.error("Vyplňte prosím částku a název.")
    
    if investments:
        # Převod na DataFrame a seřazení podle data
        df = pd.DataFrame(investments)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Získání posledních hodnot pro každý typ investice
        latest_values = df.groupby('type').last().reset_index()
        total_amount = latest_values['amount'].sum()
        
        # Přehled celkového jmění
        st.subheader("2. Přehled celkového jmění")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Celkový objem investic",
                f"{total_amount:,.0f} Kč",
                help="Celková hodnota všech investic"
            )
        
        # Zobrazení metrik pro každý typ investice
        for i, (investment_type, amount) in enumerate(zip(latest_values['type'], latest_values['amount']), start=1):
            if i < 4:  # Zobrazíme první 3 největší investice v metrikách
                with locals()[f"col{i+1}"]:
                    percentage = (amount / total_amount * 100) if total_amount > 0 else 0
                    st.metric(
                        investment_type,
                        f"{amount:,.0f} Kč",
                        f"{percentage:.1f}%"
                    )
        
        # Přepínač pro zobrazení hodnot v procentech nebo absolutních hodnotách
        show_percentages = st.checkbox("Zobrazit hodnoty v procentech", value=False)
        
        # Koláčový graf
        st.subheader("3. Rozložení investic")
        if not latest_values.empty:
            fig_pie = go.Figure()
            
            if show_percentages:
                # Výpočet procent pro každý typ
                percentages = (latest_values['amount'] / total_amount * 100).round(1)
                fig_pie.add_trace(go.Pie(
                    labels=latest_values['type'],
                    values=percentages,
                    textinfo='label+percent',
                    hovertemplate="<b>%{label}</b><br>%{value:.1f}%<extra></extra>"
                ))
                fig_pie.update_layout(title='Rozložení investic podle typu (v %)')
            else:
                fig_pie.add_trace(go.Pie(
                    labels=latest_values['type'],
                    values=latest_values['amount'],
                    textinfo='label+value',
                    hovertemplate="<b>%{label}</b><br>%{value:,.0f} Kč<extra></extra>"
                ))
                fig_pie.update_layout(title='Rozložení investic podle typu (v Kč)')
            
            fig_pie.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Časový vývoj
        st.subheader("4. Vývoj hodnoty investic v čase")
        fig = go.Figure()
        
        # Přidání čar pro každý typ investice
        for inv_type in df['type'].unique():
            type_df = df[df['type'] == inv_type]
            fig.add_trace(go.Scatter(
                x=type_df['date'],
                y=type_df['amount'],
                name=inv_type,
                mode='lines+markers'
            ))
        
        # Přidání agregované čáry pro celkovou hodnotu
        total_df = df.groupby('date')['amount'].sum().reset_index()
        fig.add_trace(go.Scatter(
            x=total_df['date'],
            y=total_df['amount'],
            name='Celkem',
            mode='lines+markers',
            line=dict(color='#FF6B6B', width=3)
        ))
        
        # Aktualizace layoutu
        fig.update_layout(
            title='Vývoj hodnoty investic v čase',
            xaxis_title='Datum',
            yaxis_title='Hodnota (Kč)',
            hovermode='x unified'
        )
        
        # Zobrazení grafu
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabulka všech záznamů s možností mazání
        st.subheader("5. Přehled všech záznamů")
        
        # Přidání sloupce pro mazání
        df['Smazat'] = False
        
        # Vytvoření kopie DataFrame pro editaci
        edited_df = st.data_editor(
            df,
            hide_index=True,
            column_config={
                'date': st.column_config.DateColumn(
                    'Datum',
                    format='DD.MM.YYYY'
                ),
                'amount': st.column_config.NumberColumn(
                    'Částka',
                    format='%.0f Kč'
                ),
                'Smazat': st.column_config.CheckboxColumn(
                    'Smazat',
                    help='Zaškrtněte pro smazání záznamu'
                )
            }
        )
        
        # Zpracování mazání
        if edited_df['Smazat'].any():
            if st.button("Smazat vybrané záznamy"):
                # Filtrování neoznačených záznamů
                df_to_keep = edited_df[~edited_df['Smazat']]
                # Převod datumů na string formát před uložením
                df_to_keep['date'] = df_to_keep['date'].dt.strftime('%Y-%m-%d')
                # Převod zpět na seznam slovníků
                investments_to_keep = df_to_keep.drop('Smazat', axis=1).to_dict('records')
                # Uložení aktualizovaných dat
                data_manager.save_investments(username, investments_to_keep)
                st.success("Vybrané záznamy byly úspěšně smazány!")
                st.rerun()
    else:
        st.info("Zatím nemáte žádné investice. Přidejte novou investici pomocí formuláře výše.")

def show_expense_tracker(username):
    """Zobrazení stránky pro sledování výdajů"""
    st.title("Sledování výdajů")
    
    # Načtení existujících výdajů
    expenses = data_manager.load_expenses(username)
    
    # Formulář pro přidání nového výdaje
    st.subheader("1. Přidat nový výdaj")
    
    # Formulář pro přidání výdaje
    with st.form("add_expense_form"):
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Částka (Kč)", min_value=0.0, value=0.0, step=100.0)
        
        with col2:
            category = st.text_input("Kategorie")
            transaction_type = st.selectbox("Typ transakce", ["Výdaj", "Příjem"])
            date = st.date_input("Datum")
            note = st.text_input("Poznámka")
        
        submitted = st.form_submit_button("Přidat")
        if submitted:
            if amount > 0 and category:
                new_expense = {
                    "amount": amount,
                    "category": category,
                    "type": transaction_type,
                    "date": date.strftime("%Y-%m-%d"),
                    "note": note
                }
                expenses.append(new_expense)
                data_manager.save_expenses(username, expenses)
                st.success("Výdaj byl úspěšně přidán!")
                st.rerun()
            else:
                st.error("Vyplňte prosím částku a kategorii.")
    
    # Přehled výdajů a příjmů
    st.subheader("2. Přehled výdajů a příjmů")
    
    # Výběr časového období
    time_period = st.selectbox(
        "Časové období",
        ["Celkem", "Rok", "Měsíc", "Týden", "Den"],
        index=0
    )
    
    # Filtrování dat podle vybraného období
    df = pd.DataFrame(expenses)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        now = pd.Timestamp.now()
        
        # Výběr konkrétního data podle období
        if time_period != "Celkem":
            if time_period == "Rok":
                selected_date = st.date_input(
                    "Vyberte rok",
                    value=now,
                    format="YYYY-MM-DD"
                )
                df = df[df['date'].dt.year == selected_date.year]
            elif time_period == "Měsíc":
                selected_date = st.date_input(
                    "Vyberte měsíc",
                    value=now,
                    format="YYYY-MM-DD"
                )
                df = df[
                    (df['date'].dt.year == selected_date.year) & 
                    (df['date'].dt.month == selected_date.month)
                ]
            elif time_period == "Týden":
                selected_date = st.date_input(
                    "Vyberte týden",
                    value=now,
                    format="YYYY-MM-DD"
                )
                week_start = pd.Timestamp(selected_date) - pd.Timedelta(days=selected_date.weekday())
                week_end = week_start + pd.Timedelta(days=6)
                df = df[(df['date'] >= week_start) & (df['date'] <= week_end)]
            elif time_period == "Den":
                selected_date = st.date_input(
                    "Vyberte den",
                    value=now,
                    format="YYYY-MM-DD"
                )
                df = df[df['date'].dt.date == selected_date]
        
        # Výpočet celkových částek
        total_expenses = df[df['type'] == 'Výdaj']['amount'].sum()
        total_income = df[df['type'] == 'Příjem']['amount'].sum()
        balance = total_income - total_expenses
        
        # Zobrazení metrik
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Celkové výdaje", f"{total_expenses:,.0f} Kč")
        with col2:
            st.metric("Celkové příjmy", f"{total_income:,.0f} Kč")
        with col3:
            st.metric("Bilance", f"{balance:,.0f} Kč", 
                     delta=f"{balance:,.0f} Kč" if balance != 0 else "0 Kč")
        
        # Histogramy výdajů a příjmů podle kategorií
        st.subheader("3. Rozložení podle kategorií")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Výdaje podle kategorií")
            expense_df = df[df['type'] == 'Výdaj']
            if not expense_df.empty:
                fig = px.histogram(
                    expense_df,
                    x='category',
                    y='amount',
                    title=f'Výdaje podle kategorií ({time_period})',
                    labels={'category': 'Kategorie', 'amount': 'Částka (Kč)'},
                    color='category'
                )
                fig.update_layout(
                    xaxis_title="Kategorie",
                    yaxis_title="Částka (Kč)",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Pro vybrané období nejsou k dispozici žádné výdaje.")
        
        with col2:
            st.write("Příjmy podle kategorií")
            income_df = df[df['type'] == 'Příjem']
            if not income_df.empty:
                fig = px.histogram(
                    income_df,
                    x='category',
                    y='amount',
                    title=f'Příjmy podle kategorií ({time_period})',
                    labels={'category': 'Kategorie', 'amount': 'Částka (Kč)'},
                    color='category'
                )
                fig.update_layout(
                    xaxis_title="Kategorie",
                    yaxis_title="Částka (Kč)",
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Pro vybrané období nejsou k dispozici žádné příjmy.")
        
        # Čárový graf příjmů a výdajů v čase
        st.subheader("4. Vývoj příjmů a výdajů v čase")
        if not df.empty:
            # Agregace dat podle data
            daily_data = df.groupby('date').apply(
                lambda x: pd.Series({
                    'income': x[x['type'] == 'Příjem']['amount'].sum(),
                    'expenses': x[x['type'] == 'Výdaj']['amount'].sum()
                })
            ).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_data['date'],
                y=daily_data['income'],
                name='Příjmy',
                line=dict(color='green')
            ))
            fig.add_trace(go.Scatter(
                x=daily_data['date'],
                y=daily_data['expenses'],
                name='Výdaje',
                line=dict(color='red')
            ))
            
            fig.update_layout(
                title=f'Vývoj příjmů a výdajů ({time_period})',
                xaxis_title='Datum',
                yaxis_title='Částka (Kč)',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabulka všech záznamů s možností mazání
        st.subheader("5. Přehled všech záznamů")
        if not df.empty:
            # Přidání sloupce pro mazání
            df['Smazat'] = False
            
            # Vytvoření kopie DataFrame pro editaci
            edited_df = st.data_editor(
                df,
                hide_index=True,
                column_config={
                    'date': st.column_config.DateColumn(
                        'Datum',
                        format='DD.MM.YYYY'
                    ),
                    'amount': st.column_config.NumberColumn(
                        'Částka',
                        format='%.0f Kč'
                    ),
                    'Smazat': st.column_config.CheckboxColumn(
                        'Smazat',
                        help='Zaškrtněte pro smazání záznamu'
                    )
                }
            )
            
            # Zpracování mazání
            if edited_df['Smazat'].any():
                if st.button("Smazat vybrané záznamy"):
                    # Filtrování neoznačených záznamů
                    df_to_keep = edited_df[~edited_df['Smazat']]
                    # Převod datumů na string formát před uložením
                    df_to_keep['date'] = df_to_keep['date'].dt.strftime('%Y-%m-%d')
                    # Převod zpět na seznam slovníků
                    expenses_to_keep = df_to_keep.drop('Smazat', axis=1).to_dict('records')
                    # Uložení aktualizovaných dat
                    data_manager.save_expenses(username, expenses_to_keep)
                    st.success("Vybrané záznamy byly úspěšně smazány!")
                    st.rerun()
        else:
            st.info("Pro vybrané období nejsou k dispozici žádné záznamy.")
    else:
        st.info("Zatím nemáte žádné záznamy. Přidejte nový výdaj pomocí formuláře výše.")

def show_settings(username: str):
    """Zobrazí nastavení uživatele"""
    st.title("Nastavení")
    
    # Načtení dat uživatele
    user_data = data_manager.get_user_data(username)
    if not user_data:
        st.error("Nepodařilo se načíst data uživatele")
        return
    
    # Zobrazení základních informací
    st.subheader("Informace o účtu")
    st.write(f"**Uživatelské jméno:** {username}")
    st.write(f"**E-mail:** {user_data['email']}")
    st.write(f"**Účet vytvořen:** {datetime.fromisoformat(user_data['created_at']).strftime('%d.%m.%Y %H:%M')}")
    
    # Změna hesla
    st.subheader("Změna hesla")
    with st.form("change_password"):
        current_password = st.text_input("Současné heslo", type="password")
        new_password = st.text_input("Nové heslo", type="password")
        confirm_password = st.text_input("Potvrzení nového hesla", type="password")
        
        if st.form_submit_button("Změnit heslo"):
            if not data_manager.verify_user(username, current_password):
                st.error("Nesprávné současné heslo")
            elif new_password != confirm_password:
                st.error("Nové heslo a jeho potvrzení se neshodují")
            elif len(new_password) < 8:
                st.error("Nové heslo musí mít alespoň 8 znaků")
            else:
                if data_manager.update_user_password(username, new_password):
                    st.success("Heslo bylo úspěšně změněno")
                else:
                    st.error("Nepodařilo se změnit heslo")

def main():
    """Hlavní funkce aplikace"""
    st.title("Finance App")
    
    if not st.session_state.logged_in:
        tab1, tab2 = st.tabs(["Přihlášení", "Registrace"])
        
        with tab1:
            login_page()
            
        with tab2:
            register_page()
    else:
        # Získání dat uživatele
        user_data = data_manager.get_user(st.session_state.username)
        if user_data:
            show_main_app(st.session_state.username, user_data.get('username', st.session_state.username))
        else:
            st.error("Nepodařilo se načíst data uživatele")
            if st.button("Odhlásit se"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.rerun()

if __name__ == "__main__":
    main()

import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from data_manager import DataManager

data_manager = DataManager()

def show_expense_tracker(username: str):
    """Zobrazí modul pro sledování výdajů a příjmů"""
    import streamlit as st
    
    st.title("Sledování výdajů a příjmů")
    
    # Načtení dat
    data = data_manager.load_data(username)
    expenses = data_manager.load_expenses(username)
    
    # Vytvoření dvou sloupců pro přehled
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Přidat nový záznam")
        with st.form("new_entry"):
            type_ = st.selectbox("Typ", ["Výdaj", "Příjem"])
            category = st.text_input("Kategorie")
            amount = st.number_input("Částka", min_value=0.0, step=100.0)
            note = st.text_area("Poznámka")
            submit = st.form_submit_button("Přidat")
            
            if submit:
                if category and amount:
                    # Přidání typu do dat
                    entry_data = {
                        "type": type_,
                        "amount": amount,
                        "timestamp": datetime.now().isoformat(),
                        "note": note
                    }
                    data_manager.add_entry(username, category, entry_data)
                    st.success("Záznam byl přidán!")
                    st.rerun()
                else:
                    st.error("Vyplňte povinná pole")
    
    with col2:
        st.subheader("Přehled kategorií")
        if data:
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
        else:
            st.info("Zatím nejsou žádné záznamy")
    
    # Přehled podle časových období
    st.subheader("Přehled podle časových období")
    if data:
        # Vytvoření DataFrame pro časové období
        df_time = []
        for cat, entries in data.items():
            if isinstance(entries, list):
                for entry in entries:
                    timestamp = datetime.fromisoformat(entry.get('timestamp', datetime.now().isoformat()))
                    df_time.append({
                        'Datum': timestamp,
                        'Rok': timestamp.year,
                        'Měsíc': timestamp.month,
                        'Kategorie': cat,
                        'Typ': entry.get('type', 'Výdaj'),
                        'Částka': float(entry.get("amount", 0))
                    })
            else:
                timestamp = datetime.fromisoformat(entries.get('timestamp', datetime.now().isoformat()))
                df_time.append({
                    'Datum': timestamp,
                    'Rok': timestamp.year,
                    'Měsíc': timestamp.month,
                    'Kategorie': cat,
                    'Typ': entries.get('type', 'Výdaj'),
                    'Částka': float(entries.get("amount", 0))
                })
        
        df_time = pd.DataFrame(df_time)
        
        # Výběr časového období
        period = st.selectbox("Vyberte časové období", ["Měsíční", "Roční"])
        
        if period == "Měsíční":
            # Agregace podle měsíců
            df_monthly = df_time.groupby(['Rok', 'Měsíc', 'Typ'])['Částka'].sum().reset_index()
            df_monthly['Období'] = df_monthly['Rok'].astype(str) + '-' + df_monthly['Měsíc'].astype(str).str.zfill(2)
            
            # Vytvoření sloupcového grafu pro měsíční přehled
            fig_monthly = px.bar(df_monthly, x='Období', y='Částka', color='Typ',
                               title='Měsíční přehled příjmů a výdajů',
                               barmode='group')
            st.plotly_chart(fig_monthly, use_container_width=True)
            
            # Tabulka s měsíčními součty
            st.subheader("Měsíční součty")
            df_monthly_pivot = df_monthly.pivot(index='Období', columns='Typ', values='Částka').fillna(0)
            
            # Zajistíme, že existují všechny potřebné sloupce
            if 'Příjem' not in df_monthly_pivot.columns:
                df_monthly_pivot['Příjem'] = 0
            if 'Výdaj' not in df_monthly_pivot.columns:
                df_monthly_pivot['Výdaj'] = 0
            
            df_monthly_pivot['Bilance'] = df_monthly_pivot['Příjem'] - df_monthly_pivot['Výdaj']
            st.dataframe(df_monthly_pivot, use_container_width=True)
        else:
            # Agregace podle roků
            df_yearly = df_time.groupby(['Rok', 'Typ'])['Částka'].sum().reset_index()
            
            # Vytvoření sloupcového grafu pro roční přehled
            fig_yearly = px.bar(df_yearly, x='Rok', y='Částka', color='Typ',
                              title='Roční přehled příjmů a výdajů',
                              barmode='group')
            st.plotly_chart(fig_yearly, use_container_width=True)
            
            # Tabulka s ročními součty
            st.subheader("Roční součty")
            df_yearly_pivot = df_yearly.pivot(index='Rok', columns='Typ', values='Částka').fillna(0)
            df_yearly_pivot['Bilance'] = df_yearly_pivot['Příjem'] - df_yearly_pivot['Výdaj']
            st.dataframe(df_yearly_pivot, use_container_width=True)
    else:
        st.info("Zatím nejsou žádné záznamy pro zobrazení přehledu")
    
    # Vytvoření dvou sloupců pro další grafy
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Rozložení podle typu")
        if data:
            # Výpočet celkových součtů pro každý typ
            type_totals = {"Výdaj": 0, "Příjem": 0}
            for cat, entries in data.items():
                if isinstance(entries, list):
                    for entry in entries:
                        type_ = entry.get("type", "Výdaj")
                        type_totals[type_] += float(entry.get("amount", 0))
                else:
                    type_ = entries.get("type", "Výdaj")
                    type_totals[type_] += float(entries.get("amount", 0))
            
            # Vytvoření DataFrame pro koláčový graf
            df_pie = pd.DataFrame([
                {'Typ': type_, 'Částka': amount}
                for type_, amount in type_totals.items()
            ])
            
            # Vytvoření koláčového grafu
            fig_pie = px.pie(df_pie, values='Částka', names='Typ', 
                           title='Rozložení příjmů a výdajů')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Zatím nejsou žádné záznamy pro zobrazení grafu")
    
    with col4:
        st.subheader("Trend v čase")
        if data:
            # Vytvoření DataFrame pro časový graf
            df_time = []
            for cat, entries in data.items():
                if isinstance(entries, list):
                    for entry in entries:
                        df_time.append({
                            'Datum': datetime.fromisoformat(entry.get('timestamp', datetime.now().isoformat())).strftime('%Y-%m-%d'),
                            'Kategorie': cat,
                            'Typ': entry.get('type', 'Výdaj'),
                            'Částka': float(entry.get("amount", 0))
                        })
                else:
                    df_time.append({
                        'Datum': datetime.fromisoformat(entries.get('timestamp', datetime.now().isoformat())).strftime('%Y-%m-%d'),
                        'Kategorie': cat,
                        'Typ': entries.get('type', 'Výdaj'),
                        'Částka': float(entries.get("amount", 0))
                    })
            
            df_time = pd.DataFrame(df_time)
            
            # Vytvoření časového grafu
            fig_time = px.line(df_time, x='Datum', y='Částka', color='Typ',
                             title='Trend příjmů a výdajů v čase')
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info("Zatím nejsou žádné záznamy pro zobrazení grafu")
    
    # Zobrazení detailních záznamů
    st.subheader("Detailní záznamy")
    if data:
        # Vytvoření DataFrame pro tabulku
        df_details = []
        for cat, entries in data.items():
            if isinstance(entries, list):
                for entry in entries:
                    df_details.append({
                        'Kategorie': cat,
                        'Typ': entry.get('type', 'Výdaj'),
                        'Částka': float(entry.get("amount", 0)),
                        'Datum': datetime.fromisoformat(entry.get('timestamp', datetime.now().isoformat())).strftime('%Y-%m-%d %H:%M'),
                        'Poznámka': entry.get('note', '')
                    })
            else:
                df_details.append({
                    'Kategorie': cat,
                    'Typ': entries.get('type', 'Výdaj'),
                    'Částka': float(entries.get("amount", 0)),
                    'Datum': datetime.fromisoformat(entries.get('timestamp', datetime.now().isoformat())).strftime('%Y-%m-%d %H:%M'),
                    'Poznámka': entries.get('note', '')
                })
        
        df_details = pd.DataFrame(df_details)
        df_details = df_details.sort_values('Datum', ascending=False)
        
        # Zobrazení tabulky
        st.dataframe(df_details, use_container_width=True)
    else:
        st.info("Zatím nejsou žádné záznamy") 
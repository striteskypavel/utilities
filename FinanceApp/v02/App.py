import streamlit as st
import pandas as pd
import json
from datetime import datetime
from data_manager import (
    load_data, save_data, add_entry, remove_entry,
    export_data, import_data, change_data_location
)
from visualizations import (
    show_pie_chart, show_history_chart, 
    show_category_comparison
)
from history_manager import log_change, load_history, clear_history, delete_history_entries
from config import DEFAULT_CATEGORIES
from retirement_planning import show_retirement_planning
from mortgage_calculator import show_mortgage_calculator
import os
import time

# Konfigurace stránky
st.set_page_config(
    page_title="Finanční aplikace",
    page_icon="💰",
    layout="wide"
)

# Výběr stránky
page = st.sidebar.radio(
    "Navigace",
    ["Hlavní stránka", "Plánování důchodu", "Hypoteční kalkulačka"]
)

if page == "Plánování důchodu":
    show_retirement_planning()
elif page == "Hypoteční kalkulačka":
    show_mortgage_calculator()
else:  # Hlavní stránka
    # Načtení dat
    data = load_data()
    history = load_history()

    # Nastavení sidebaru
    st.sidebar.title("Nástroje")

    # Modul pro správu dat
    with st.sidebar.expander("Správa dat", expanded=False):
        st.subheader("Export a import dat")
        
        # Export dat
        st.write("Export dat")
        export_format = st.radio("Formát exportu", ["JSON", "CSV"], horizontal=True)
        
        # Vytvoření dočasného souboru pro export s absolutní cestou
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_export = None  # Inicializace proměnné
        
        if export_format == "JSON":
            temp_export = os.path.abspath("temp_export.json")
            export_data(temp_export)
            
            # Načtení dat pro download
            with open(temp_export, "rb") as file:
                export_data_bytes = file.read()
            
            # Tlačítko pro download JSON
            st.download_button(
                label="Stáhnout JSON",
                data=export_data_bytes,
                file_name=f"finance_data_{timestamp}.json",
                mime="application/json"
            )
        else:  # CSV
            # Vytvoření DataFrame pro export
            export_df = pd.DataFrame()
            for category, items in data.items():
                for item in items:
                    export_df = pd.concat([export_df, pd.DataFrame({
                        "Kategorie": [category],
                        "Popis": [item["description"]],
                        "Částka": [item["amount"]]
                    })], ignore_index=True)
            
            # Seřazení podle kategorie
            export_df = export_df.sort_values("Kategorie")
            
            # Formátování částky
            export_df["Částka"] = export_df["Částka"].apply(lambda x: f"{x:,.0f} Kč".replace(",", " "))
            
            # Konverze do CSV s českým kódováním a oddělovačem středníkem
            csv_data = export_df.to_csv(
                index=False,
                sep=";",
                encoding="utf-8-sig"  # Přidá BOM pro správné zobrazení v Excelu
            ).encode("utf-8-sig")
            
            # Tlačítko pro download CSV
            st.download_button(
                label="Stáhnout CSV",
                data=csv_data,
                file_name=f"finance_data_{timestamp}.csv",
                mime="text/csv"
            )
        
        # Smazání dočasného souboru (pokud existuje a byl vytvořen)
        if temp_export and os.path.exists(temp_export):
            os.remove(temp_export)

        # Import dat
        st.write("Import dat")
        uploaded_file = st.file_uploader("Vyberte soubor pro import", type=["json", "csv"])
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            success_message = st.empty()  # Vytvoření prázdného kontejneru pro zprávu
            
            if st.button("Importovat data"):
                # Uložení nahraného souboru do dočasného souboru
                temp_file = f"temp_import.{file_extension}"
                with open(temp_file, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                if import_data(temp_file):
                    # Zobrazení úspěšné zprávy v prázdném kontejneru
                    success_message.success("Data byla úspěšně importována!")
                    # Počkání 3 sekundy
                    time.sleep(3)
                    # Vymazání zprávy
                    success_message.empty()
                    st.rerun()
                else:
                    st.error("Chyba při importu dat. Zkontrolujte formát souboru.")
                
                # Smazání dočasného souboru
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
            # Možnost smazat záznamy podle kategorie
            if history:
                categories = sorted(set(entry["category"] for entry in history))
                selected_category = st.selectbox("Vyberte kategorii", [""] + categories)
                
                if selected_category and st.button(f"Smazat záznamy kategorie '{selected_category}'"):
                    deleted = delete_history_entries({"category": selected_category})
                    st.success(f"Smazáno {deleted} záznamů kategorie '{selected_category}'")
                    st.rerun()
        
        # Možnost smazat záznamy podle data
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
            # Možnost smazat konkrétní záznam podle ID
            if history:
                entry_ids = list(range(len(history)))
                selected_id = st.selectbox("Vyberte ID záznamu ke smazání", [""] + entry_ids)
                
                if selected_id != "" and st.button("Smazat vybraný záznam"):
                    delete_history_entries({"id": selected_id})
                    st.success(f"Záznam s ID {selected_id} byl smazán")
                    st.rerun()

    # Hlavní obsah aplikace
    st.title("Jednoduchý sledovač financí")

    # **Vkládání finančních záznamů**
    st.subheader("Přidat finanční záznam")

    # Pole pro novou kategorii
    new_category = st.text_input("Název nové kategorie").strip()
    
    # Pole pro částku
    amount = st.number_input("Částka", min_value=0, step=1000, format="%d")
    
    submit = st.button("Přidat")

    if submit:
        if not new_category:
            st.error("Zadejte název kategorie!")
        elif new_category in data:
            st.error(f"Kategorie '{new_category}' již existuje! Použijte jinou kategorii nebo upravte existující.")
        else:
            add_entry(new_category, new_category, amount)  # Použijeme název kategorie jako popis
            st.success(f"Vytvořena nová kategorie '{new_category}' a přidán záznam!")
            st.rerun()

    # **Zobrazení přehledu financí**
    st.subheader("Přehled financí")

    # **Vizualizace dat**
    st.header("Vizualizace dat")

    # Vytvoření záložek pro různé typy vizualizací
    viz_tabs = st.tabs(["Rozložení financí", "Historie změn", "Porovnání kategorií"])

    with viz_tabs[0]:
        st.subheader("Rozložení financí")
        # Výpočet součtů pro každou kategorii
        totals = {cat: sum(item["amount"] for item in items) for cat, items in data.items()}
        # Nastavení větší výšky grafu
        show_pie_chart(totals, height=600)

    with viz_tabs[1]:
        st.subheader("Historie změn")
        show_history_chart(history, height=600)

    with viz_tabs[2]:
        st.subheader("Porovnání kategorií")
        show_category_comparison(data, height=600)

    # Přesunuto pod grafy - editovatelná tabulka
    totals = {cat: sum(item["amount"] for item in data.get(cat, [])) for cat in data.keys()}

    df = pd.DataFrame({
        "Kategorie": list(totals.keys()),
        "Částka": list(totals.values())  # Ukládáme číselné hodnoty bez formátování
    })

    # Vytvoření editovatelné tabulky
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

    # Kontrola změn a aktualizace dat
    if not df["Částka"].equals(edited_df["Částka"]):
        for idx, row in edited_df.iterrows():
            category = row["Kategorie"]
            new_amount = row["Částka"]
            old_amount = totals[category]
            
            if new_amount != old_amount:
                # Aktualizace posledního záznamu v kategorii
                if data[category]:
                    data[category][-1]["amount"] = new_amount
                    save_data(data)
                    log_change(category, old_amount, new_amount)
                    st.success(f"Částka pro kategorii '{category}' byla aktualizována!")
                    st.rerun()

    # Přidat informace o aplikaci
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

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from data_manager import load_data, save_data, add_entry, remove_entry
from visualizations import (
    show_pie_chart, show_history_chart, 
    show_category_comparison, show_time_distribution
)
from history_manager import log_change, load_history, clear_history, delete_history_entries
from config import DEFAULT_CATEGORIES

# Načtení dat
data = load_data()
history = load_history()

st.title("Jednoduchý sledovač financí")

# **Vkládání finančních záznamů**
st.subheader("Přidat finanční záznam")
category = st.selectbox("Kategorie", DEFAULT_CATEGORIES + list(data.keys()))
description = st.text_input("Popis")
amount = st.number_input("Částka", min_value=0.0, format="%.2f")
submit = st.button("Přidat")

if submit and description:
    old_value = sum(item["amount"] for item in data.get(category, []))
    add_entry(category, description, amount)
    new_value = sum(item["amount"] for item in data.get(category, []))
    log_change(category, old_value, new_value)
    st.success("Záznam přidán!")
    st.rerun()

# **Zobrazení přehledu financí**
st.subheader("Přehled financí")

totals = {cat: sum(item["amount"] for item in data.get(cat, [])) for cat in data.keys()}

df = pd.DataFrame({
    "Kategorie": list(totals.keys()),
    "Částka": [f"{value:,.0f} Kč" for value in totals.values()]
})

st.dataframe(df, use_container_width=True)

# **Vizualizace dat**
st.header("Vizualizace dat")

# Vytvoření záložek pro různé typy vizualizací
viz_tabs = st.tabs(["Rozložení financí", "Historie změn", "Porovnání kategorií", "Časová distribuce"])

with viz_tabs[0]:
    st.subheader("Rozložení financí")
    show_pie_chart(totals)

with viz_tabs[1]:
    st.subheader("Historie změn")
    show_history_chart(history)

with viz_tabs[2]:
    st.subheader("Porovnání kategorií")
    show_category_comparison(data)

with viz_tabs[3]:
    st.subheader("Časová distribuce")
    show_time_distribution(history)  # Předáváme history místo data

# **Historie změn - správa**
st.header("Správa historie")

# Rozšířené možnosti pro správu historie
with st.expander("Možnosti správy historie"):
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

# Přidat informace o aplikaci
with st.expander("O aplikaci"):
    st.write("""
    **Jednoduchý sledovač financí** je aplikace pro sledování osobních financí.
    
    Funkce:
    - Přidávání finančních záznamů do kategorií
    - Vizualizace dat pomocí různých typů grafů
    - Sledování historie změn
    - Správa historie
    
    Vytvořeno pomocí Streamlit.
    """)

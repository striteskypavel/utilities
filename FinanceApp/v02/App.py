import streamlit as st
import pandas as pd
import json
from datetime import datetime
from data_manager import load_data, save_data, add_entry, remove_entry
from visualizations import (
    show_pie_chart, show_history_chart, 
    show_category_comparison
)
from history_manager import log_change, load_history, clear_history, delete_history_entries
from config import DEFAULT_CATEGORIES

# Načtení dat
data = load_data()
history = load_history()

st.title("Jednoduchý sledovač financí")

# **Vkládání finančních záznamů**
st.subheader("Přidat finanční záznam")

# Přidání možnosti vytvořit novou kategorii nebo vybrat existující
action_type = st.radio(
    "Vyberte akci",
    ["Vytvořit novou kategorii", "Upravit existující kategorii"],
    horizontal=True
)

if action_type == "Vytvořit novou kategorii":
    new_category = st.text_input("Název nové kategorie").strip()
    
    # Vytvoření řádku pro částku a tlačítka
    col1, col2 = st.columns([3, 1])
    
    with col1:
        amount = st.number_input("Částka", min_value=0, step=1000, format="%d")
    
    with col2:
        if st.button("+"):
            # Zaokrouhlení nahoru na nejbližší tisíc a přidání dalšího tisíce
            amount = ((amount + 999) // 1000) * 1000 + 1000
    
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
else:
    if data:
        category = st.selectbox("Vyberte kategorii", sorted(data.keys()))
        st.info(f"Pro úpravu kategorie '{category}' použijte tabulku níže v sekci 'Přehled financí'.")
    else:
        st.info("Zatím nejsou k dispozici žádné kategorie. Vytvořte nejprve novou kategorii.")

# **Zobrazení přehledu financí**
st.subheader("Přehled financí")

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

# **Vizualizace dat**
st.header("Vizualizace dat")

# Vytvoření záložek pro různé typy vizualizací
viz_tabs = st.tabs(["Rozložení financí", "Historie změn", "Porovnání kategorií"])

with viz_tabs[0]:
    st.subheader("Rozložení financí")
    show_pie_chart(totals)

with viz_tabs[1]:
    st.subheader("Historie změn")
    show_history_chart(history)

with viz_tabs[2]:
    st.subheader("Porovnání kategorií")
    show_category_comparison(data)

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

import streamlit as st
import pandas as pd
import json
from data_manager import load_data, save_data, add_entry, remove_entry
from visualizations import show_pie_chart, show_history_chart
from history_manager import log_change, load_history, clear_history
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
    st.experimental_rerun()

# **Zobrazení přehledu financí**
st.subheader("Přehled financí")

totals = {cat: sum(item["amount"] for item in data.get(cat, [])) for cat in data.keys()}

df = pd.DataFrame({
    "Kategorie": list(totals.keys()),
    "Částka": [f"{value:,.0f} Kč" for value in totals.values()]
})

st.dataframe(df, use_container_width=True)

# **Koláčový graf alokace financí**
show_pie_chart(totals)

# **Historie změn**
st.subheader("Historie změn")
show_history_chart(history)
if st.button("Vymazat historii"):
    clear_history()
    st.experimental_rerun()

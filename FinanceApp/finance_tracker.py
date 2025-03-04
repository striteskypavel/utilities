import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np
from datetime import datetime

# Načtení nebo vytvoření dat
DATA_FILE = "finance_data.json"
HISTORY_FILE = "finance_history.json"


def remove_history_entry(category, timestamp):
    """Odstraní konkrétní historický záznam dle kategorie a časového razítka."""
    data = load_data()
    if "history" in data:
        data["history"] = [entry for entry in data["history"] if not (entry["category"] == category and entry["timestamp"] == timestamp)]
        save_data(data)


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {key: [] for key in [
            "investments", "real_estate", "retirement_savings",
            "cryptocurrency", "mintos", "xtb_etf", "pension_savings_csob", "portu_majda",
            "deposit_flat", "portu_etf", "amundi_majda", "xtb_majda", "land_majda",
            "fiat_czk", "csob_medium", "insurance"
        ]}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Načtení dat a historie
data = load_data()
history = load_history()

st.title("📊 Finanční sledovač s historií a editací")

# **Kategorie financí**
categories = [
    "investments", "real_estate", "retirement_savings",
    "cryptocurrency", "mintos", "xtb_etf", "pension_savings_csob", "portu_majda",
    "deposit_flat", "portu_etf", "amundi_majda", "xtb_majda", "land_majda",
    "fiat_czk", "csob_medium", "insurance"
]

category_names = {
    "investments": "Investice",
    "real_estate": "Nemovitosti",
    "retirement_savings": "Důchodové spoření",
    "cryptocurrency": "Kryptoměny",
    "mintos": "Mintos",
    "xtb_etf": "XTB ETF",
    "pension_savings_csob": "Penzijní spoření ČSOB",
    "portu_majda": "Portu Majda",
    "deposit_flat": "Záloha na byt",
    "portu_etf": "Portu ETF",
    "amundi_majda": "Amundi Majda",
    "xtb_majda": "XTB Majda",
    "land_majda": "Pole Majda",
    "fiat_czk": "Fiat CZK",
    "csob_medium": "ČSOB Medium",
    "insurance": "Pojištění"
}

# **Vytvoření součtů pro každou kategorii**
totals = {cat: sum(item.get("amount", 0) for item in data.get(cat, [])) for cat in categories}

# **Koláčový graf alokace financí**
st.subheader("📊 Rozložení financí")

# **Přepínač mezi % a Kč**
view_option = st.radio("Vyber zobrazení:", ["Hodnoty v Kč", "Procenta"], horizontal=True)

df_pie = pd.DataFrame({
    "Kategorie": [category_names[cat] for cat in totals.keys()],
    "Hodnota": list(totals.values())
})

if view_option == "Procenta":
    fig_pie = px.pie(df_pie, names="Kategorie", values="Hodnota", title="Rozložení financí (%)",
                     hole=0.3, height=600, width=800)
    fig_pie.update_traces(textinfo='percent+label')
else:
    fig_pie = px.pie(df_pie, names="Kategorie", values="Hodnota", title="Rozložení financí (Kč)",
                     hole=0.3, height=600, width=800)
    fig_pie.update_traces(textinfo='label+value')

st.plotly_chart(fig_pie, use_container_width=True)

# **Detailní tabulka s možností editace**
st.subheader("✏️ Editovatelná tabulka financí")

df = pd.DataFrame({
    "Kategorie": [category_names[cat] for cat in totals.keys()],
    "Částka": list(totals.values())
})

edited_df = st.data_editor(df, num_rows="dynamic")

# **Zpracování změn v editované tabulce**
if st.button("💾 Uložit změny"):
    for index, row in edited_df.iterrows():
        category_key = list(category_names.keys())[index]
        new_value = row["Částka"]

        # Pokud se hodnota změnila, aktualizuj a ulož do historie
        if new_value != totals[category_key]:
            update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Přidání změny do historie
            if category_key not in history:
                history[category_key] = []
            history[category_key].append({
                "old_value": totals[category_key],
                "new_value": new_value,
                "timestamp": update_time
            })

            # Aktualizace dat
            data[category_key] = [{"description": category_names[category_key], "amount": new_value}]
    
    save_data(data)
    save_history(history)
    st.success("✅ Data byla aktualizována!")

# **Zobrazení historie změn**
st.subheader("📜 Historie změn")

history_list = []
for cat, changes in history.items():
    for change in changes:
        history_list.append([category_names[cat], change["old_value"], change["new_value"], change["timestamp"]])

if history_list:
    history_df = pd.DataFrame(history_list, columns=["Kategorie", "Původní hodnota", "Nová hodnota", "Čas změny"])
    st.dataframe(history_df, use_container_width=True)
else:
    st.write("🔍 Zatím žádné změny nejsou zaznamenány.")

if "history" in data and data["history"]:
    history_df = pd.DataFrame(data["history_df"])
    
    # Zobrazení tabulky historie
    for index, row in history_df.iterrows():
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"**{row['category']}**: {row['amount']:,.0f} Kč")
        with col2:
            st.write(row["timestamp"])
        with col3:
            if st.button("🗑️", key=f"delete_{index}"):
                remove_history_entry(row["category"], row["timestamp"])
                st.rerun()  # Obnovení UI po odstranění záznamu
else:
    st.write("Žádné historické záznamy nejsou k dispozici.")

# **📈 Graf vývoje financí v čase**
st.subheader("📈 Vývoj financí v čase")

if history_list:
    history_df["Čas změny"] = pd.to_datetime(history_df["Čas změny"])
    history_df = history_df.sort_values(by="Čas změny")

    fig_line = px.line(history_df, x="Čas změny", y="Nová hodnota", color="Kategorie",
                       markers=True, title="Vývoj financí v čase", height=600, width=900)
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.write("📉 Zatím nejsou dostupná historická data pro zobrazení grafu.")






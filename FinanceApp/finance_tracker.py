import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

# Načtení nebo vytvoření dat
DATA_FILE = "finance_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "income": [],
            "expenses": [],
            "investments": [],
            "real_estate": [],
            "retirement_savings": []
        }

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Inicializace dat
data = load_data()

st.title("Jednoduchý sledovač financí")

# **Vkládání finančních záznamů**
with st.form("finance_form"):
    st.subheader("Přidat finanční záznam")
    category = st.selectbox("Kategorie", ["Příjem", "Výdaj", "Investice", "Nemovitosti", "Důchodové spoření"])
    description = st.text_input("Popis")
    amount = st.number_input("Částka", min_value=0.0, format="%.2f")
    submit = st.form_submit_button("Přidat")
    
    if submit and description:
        if category == "Příjem":
            data["income"].append({"description": description, "amount": amount})
        elif category == "Výdaj":
            data["expenses"].append({"description": description, "amount": amount})
        elif category == "Investice":
            data["investments"].append({"description": description, "amount": amount})
        elif category == "Nemovitosti":
            data["real_estate"].append({"description": description, "amount": amount})
        elif category == "Důchodové spoření":
            data["retirement_savings"].append({"description": description, "amount": amount})
        save_data(data)
        st.success("Záznam přidán!")

# **Zobrazení přehledu financí**
st.subheader("Přehled financí")

# Ověření, zda klíče existují v načtených datech, jinak inicializace prázdným seznamem
income_total = sum(item["amount"] for item in data.get("income", []))
expenses_total = sum(item["amount"] for item in data.get("expenses", []))
investment_total = sum(item["amount"] for item in data.get("investments", []))
real_estate_total = sum(item["amount"] for item in data.get("real_estate", []))
retirement_savings_total = sum(item["amount"] for item in data.get("retirement_savings", []))

savings = income_total - expenses_total
total_assets = savings + investment_total + real_estate_total + retirement_savings_total

# Zobrazení metrik
st.metric("Celkové příjmy", f"{income_total:,.2f} Kč")
st.metric("Celkové výdaje", f"{expenses_total:,.2f} Kč")
st.metric("Úspory", f"{savings:,.2f} Kč")
st.metric("Investice", f"{investment_total:,.2f} Kč")
st.metric("Nemovitosti", f"{real_estate_total:,.2f} Kč")
st.metric("Penzijní spoření", f"{retirement_savings_total:,.2f} Kč")
st.metric("Celkový majetek", f"{total_assets:,.2f} Kč")

# **Vizualizace financí**
st.subheader("Graf příjmů a výdajů")
fig, ax = plt.subplots()
ax.bar(["Příjmy", "Výdaje", "Investice", "Nemovitosti", "Důchodové spoření"], 
       [income_total, expenses_total, investment_total, real_estate_total, retirement_savings_total], 
       color=["green", "red", "blue", "orange", "purple"])
ax.set_ylabel("Částka (Kč)")
st.pyplot(fig)

st.subheader("Detailní tabulka")
all_data = pd.DataFrame(data["income"] + data["expenses"] + data["investments"] + data["real_estate"] + data["retirement_savings"]).fillna("-")
st.dataframe(all_data)

# **Predikce úspor do důchodu**
st.subheader("Simulace úspor do důchodu")

years = st.number_input("Počet let do důchodu", min_value=1, max_value=50, value=30)
income_growth = st.number_input("Roční růst příjmů (%)", min_value=0.0, max_value=20.0, value=2.0)
expenses_growth = st.number_input("Roční růst výdajů (%)", min_value=0.0, max_value=20.0, value=2.0)

# **Nastavení výnosů pro jednotlivé složky majetku**
st.subheader("Očekávané roční výnosy jednotlivých složek majetku:")
savings_rate = st.number_input("Úroková sazba pro úspory (%)", min_value=0.0, max_value=10.0, value=1.5)
investment_rate = st.number_input("Roční výnos z investic (%)", min_value=0.0, max_value=20.0, value=7.0)
real_estate_rate = st.number_input("Roční růst hodnoty nemovitostí (%)", min_value=0.0, max_value=10.0, value=4.0)
retirement_rate = st.number_input("Roční výnos důchodového spoření (%)", min_value=0.0, max_value=10.0, value=3.0)

# **Výpočet predikce**
savings_projection = [savings]
investment_projection = [investment_total]
real_estate_projection = [real_estate_total]
retirement_projection = [retirement_savings_total]

for i in range(years):
    income_total *= (1 + income_growth / 100)
    expenses_total *= (1 + expenses_growth / 100)
    
    savings = (savings + income_total - expenses_total) * (1 + savings_rate / 100)
    investment_total *= (1 + investment_rate / 100)
    real_estate_total *= (1 + real_estate_rate / 100)
    retirement_savings_total *= (1 + retirement_rate / 100)

    savings_projection.append(savings)
    investment_projection.append(investment_total)
    real_estate_projection.append(real_estate_total)
    retirement_projection.append(retirement_savings_total)

# **Graf predikce vývoje financí**
years_range = np.arange(0, years + 1)
fig, ax = plt.subplots()
ax.plot(years_range, savings_projection, label="Úspory", marker='o', linestyle='-')
ax.plot(years_range, investment_projection, label="Investice", marker='s', linestyle='--')
ax.plot(years_range, real_estate_projection, label="Nemovitosti", marker='^', linestyle='-.')
ax.plot(years_range, retirement_projection, label="Důchodové spoření", marker='x', linestyle=':')

ax.set_xlabel("Roky")
ax.set_ylabel("Částka (Kč)")
ax.set_title("Predikce úspor do důchodu")
ax.legend()
ax.ticklabel_format(style='plain')

st.pyplot(fig)

st.write(f"**Odhadovaný celkový majetek při odchodu do důchodu:** {savings_projection[-1] + investment_projection[-1] + real_estate_projection[-1] + retirement_projection[-1]:,.2f} Kč")
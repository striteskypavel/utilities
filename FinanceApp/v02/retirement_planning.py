import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def calculate_compound_interest(initial_investment, monthly_contribution, years, annual_rate):
    """Vypočítá růst investice se složeným úročením."""
    rate = annual_rate / 100 / 12  # Měsíční úroková míra
    months = years * 12
    
    # Inicializace polí pro graf
    timeline = []
    balance = []
    contributions = []
    interest = []
    
    current_balance = initial_investment
    total_contributions = initial_investment
    
    for month in range(months + 1):
        timeline.append(month / 12)  # Převod na roky pro osu X
        balance.append(current_balance)
        contributions.append(total_contributions)
        interest.append(current_balance - total_contributions)
        
        if month < months:  # Nepřičítáme po posledním měsíci
            # Přičtení měsíčního příspěvku
            current_balance += monthly_contribution
            total_contributions += monthly_contribution
            
            # Přičtení úroku
            current_balance *= (1 + rate)
    
    return timeline, balance, contributions, interest

def show_retirement_planning():
    st.title("Plánování důchodu")
    
    # Vstupní parametry
    col1, col2 = st.columns(2)
    
    with col1:
        initial_investment = st.number_input(
            "Počáteční investice (Kč)",
            min_value=0,
            value=100000,
            step=10000,
            format="%d"
        )
        
        monthly_contribution = st.number_input(
            "Měsíční příspěvek (Kč)",
            min_value=0,
            value=5000,
            step=1000,
            format="%d"
        )
    
    with col2:
        years = st.number_input(
            "Doba investice (roky)",
            min_value=1,
            max_value=50,
            value=30,
            step=1
        )
        
        annual_rate = st.number_input(
            "Očekávaný roční výnos (%)",
            min_value=0.0,
            max_value=20.0,
            value=7.0,
            step=0.5
        )
    
    # Výpočet hodnot
    timeline, balance, contributions, interest = calculate_compound_interest(
        initial_investment, monthly_contribution, years, annual_rate
    )
    
    # Zobrazení výsledků
    final_balance = balance[-1]
    total_contributions = contributions[-1]
    total_interest = interest[-1]
    
    st.header("Výsledky investování")
    
    result_cols = st.columns(3)
    with result_cols[0]:
        st.metric(
            "Konečná hodnota",
            f"{final_balance:,.0f} Kč"
        )
    with result_cols[1]:
        st.metric(
            "Celkové příspěvky",
            f"{total_contributions:,.0f} Kč"
        )
    with result_cols[2]:
        st.metric(
            "Výnos z úroků",
            f"{total_interest:,.0f} Kč"
        )
    
    # Graf
    fig = go.Figure()
    
    # Přidání ploch pro příspěvky a úroky
    fig.add_trace(go.Scatter(
        x=timeline,
        y=contributions,
        name="Vložené prostředky",
        fill='tozeroy',
        mode='none'
    ))
    
    fig.add_trace(go.Scatter(
        x=timeline,
        y=balance,
        name="Celková hodnota",
        fill='tonexty',
        mode='none'
    ))
    
    # Úprava vzhledu
    fig.update_layout(
        title="Růst investice v čase",
        xaxis_title="Roky",
        yaxis_title="Hodnota (Kč)",
        showlegend=True,
        hovermode='x unified'
    )
    
    # Formátování osy Y na miliony
    fig.update_layout(
        yaxis=dict(
            tickformat=",.0f",
            ticksuffix=" Kč"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Vysvětlení výpočtu
    with st.expander("Jak se to počítá?"):
        st.write("""
        Výpočet používá vzorec pro složené úročení s pravidelnými měsíčními příspěvky:
        
        1. Počáteční investice se úročí měsíčně (roční úrok / 12)
        2. Každý měsíc se přičte váš příspěvek
        3. Celá částka se dále úročí
        
        **Poznámky:**
        - Výpočet je zjednodušený a nezahrnuje inflaci
        - Nezahrnuje daně a poplatky
        - Předpokládá konstantní výnos
        - Slouží pouze pro orientační plánování
        """) 
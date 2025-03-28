import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

def calculate_compound_interest(principal, rate, time, compounding_frequency, monthly_contribution=0, inflation_rate=0):
    """
    Vypočítá složené úročení s možností měsíčních příspěvků a inflace.
    
    Args:
        principal (float): Počáteční částka
        rate (float): Roční úroková sazba (v procentech)
        time (int): Doba v letech
        compounding_frequency (int): Frekvence úročení (1=ročně, 12=měsíčně, 365=denně)
        monthly_contribution (float): Měsíční příspěvek (volitelné)
        inflation_rate (float): Roční míra inflace (v procentech)
    
    Returns:
        tuple: (celková částka, celkový příspěvek, celkový úrok, reálná hodnota)
    """
    # Převod procent na desetinné číslo
    r = rate / 100
    i = inflation_rate / 100
    
    # Výpočet efektivní roční sazby
    effective_rate = (1 + r/compounding_frequency) ** compounding_frequency - 1
    
    # Výpočet budoucí hodnoty počáteční částky
    future_value = principal * (1 + effective_rate) ** time
    
    # Výpočet budoucí hodnoty měsíčních příspěvků
    if monthly_contribution > 0:
        monthly_rate = effective_rate / 12
        future_value_contributions = monthly_contribution * ((1 + monthly_rate) ** (time * 12) - 1) / monthly_rate
        future_value += future_value_contributions
    
    # Výpočet celkového příspěvku
    total_contribution = principal + (monthly_contribution * 12 * time)
    
    # Výpočet celkového úroku
    total_interest = future_value - total_contribution
    
    # Výpočet reálné hodnoty (s ohledem na inflaci)
    real_value = future_value / ((1 + i) ** time)
    
    return future_value, total_contribution, total_interest, real_value

def create_compound_interest_chart(principal, rate, time, compounding_frequency, monthly_contribution=0, inflation_rate=0):
    """
    Vytvoří graf pro vizualizaci složeného úročení.
    """
    # Vytvoření časové osy
    dates = pd.date_range(start=datetime.now(), periods=time*12+1, freq='M')
    
    # Výpočet hodnot pro každý měsíc
    values = []
    contributions = []
    interests = []
    real_values = []
    
    for i in range(len(dates)):
        future_value, total_contribution, total_interest, real_value = calculate_compound_interest(
            principal, rate, i/12, compounding_frequency, monthly_contribution, inflation_rate
        )
        values.append(future_value)
        contributions.append(total_contribution)
        interests.append(total_interest)
        real_values.append(real_value)
    
    # Vytvoření grafu
    fig = go.Figure()
    
    # Přidání čar pro celkovou hodnotu, příspěvky, úrok a reálnou hodnotu
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        name='Celková hodnota',
        line=dict(color='blue')
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=contributions,
        name='Celkový příspěvek',
        line=dict(color='green')
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=interests,
        name='Celkový úrok',
        line=dict(color='red')
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=real_values,
        name='Reálná hodnota',
        line=dict(color='purple')
    ))
    
    # Úprava layoutu
    fig.update_layout(
        title='Vývoj složeného úročení v čase',
        xaxis_title='Datum',
        yaxis_title='Částka (Kč)',
        hovermode='x unified'
    )
    
    return fig

def show_compound_interest_calculator():
    """Zobrazí kalkulačku složeného úročení."""
    st.title("Kalkulačka složeného úročení")
    
    # Vytvoření dvou sloupců pro vstupní parametry
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Základní parametry")
        principal = st.number_input(
            "Počáteční částka (Kč)",
            min_value=0.0,
            step=1000.0,
            value=100000.0,
            help="Částka, kterou chcete investovat"
        )
        
        rate = st.number_input(
            "Roční úroková sazba (%)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            value=5.0,
            help="Roční úroková sazba v procentech"
        )
        
        time = st.number_input(
            "Doba v letech",
            min_value=1,
            max_value=50,
            step=1,
            value=20,
            help="Doba, po kterou chcete investovat"
        )
    
    with col2:
        st.subheader("Další parametry")
        compounding_frequency = st.selectbox(
            "Frekvence úročení",
            options=[
                ("Ročně", 1),
                ("Pololetně", 2),
                ("Čtvrtletně", 4),
                ("Měsíčně", 12),
                ("Denně", 365)
            ],
            format_func=lambda x: x[0],
            help="Jak často se úrok připisuje"
        )
        
        monthly_contribution = st.number_input(
            "Měsíční příspěvek (Kč)",
            min_value=0.0,
            step=1000.0,
            value=2000.0,
            help="Měsíční částka, kterou chcete přispívat"
        )
        
        inflation_rate = st.number_input(
            "Roční míra inflace (%)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            value=2.0,
            help="Očekávaná roční míra inflace v procentech"
        )
    
    # Výpočet výsledků
    future_value, total_contribution, total_interest, real_value = calculate_compound_interest(
        principal, rate, time, compounding_frequency[1], monthly_contribution, inflation_rate
    )
    
    # Zobrazení výsledků
    st.subheader("Výsledky")
    
    # Vytvoření čtyř sloupců pro metriky
    result_col1, result_col2, result_col3, result_col4 = st.columns(4)
    
    with result_col1:
        st.metric(
            "Celková hodnota",
            f"{future_value:,.0f} Kč",
            help="Celková částka po uplynutí doby"
        )
    
    with result_col2:
        st.metric(
            "Celkový příspěvek",
            f"{total_contribution:,.0f} Kč",
            help="Celková částka, kterou jste vložili"
        )
    
    with result_col3:
        st.metric(
            "Celkový úrok",
            f"{total_interest:,.0f} Kč",
            help="Celkový úrok, který jste získali"
        )
    
    with result_col4:
        st.metric(
            "Reálná hodnota",
            f"{real_value:,.0f} Kč",
            help="Celková částka po zohlednění inflace"
        )
    
    # Zobrazení grafu
    st.subheader("Vývoj v čase")
    fig = create_compound_interest_chart(
        principal, rate, time, compounding_frequency[1], monthly_contribution, inflation_rate
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailní rozpis
    st.subheader("Detailní rozpis")
    
    # Vytvoření tabulky s měsíčními hodnotami
    dates = pd.date_range(start=datetime.now(), periods=time*12+1, freq='M')
    monthly_data = []
    
    for i in range(len(dates)):
        future_value, total_contribution, total_interest, real_value = calculate_compound_interest(
            principal, rate, i/12, compounding_frequency[1], monthly_contribution, inflation_rate
        )
        monthly_data.append({
            'Datum': dates[i].strftime('%d.%m.%Y'),
            'Celková hodnota': f"{future_value:,.0f} Kč",
            'Celkový příspěvek': f"{total_contribution:,.0f} Kč",
            'Celkový úrok': f"{total_interest:,.0f} Kč",
            'Reálná hodnota': f"{real_value:,.0f} Kč"
        })
    
    df = pd.DataFrame(monthly_data)
    st.dataframe(df, hide_index=True, use_container_width=True) 
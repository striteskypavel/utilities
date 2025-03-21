import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import date, timedelta

def calculate_mortgage(loan_amount, interest_rate, years, extra_payment=0):
    """Vypočítá detaily hypotéky včetně splátek a úroků."""
    monthly_rate = interest_rate / 100 / 12
    num_payments = years * 12
    
    # Výpočet měsíční splátky (bez mimořádných splátek)
    if monthly_rate == 0:
        monthly_payment = loan_amount / num_payments
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    
    # Inicializace polí pro sledování průběhu
    remaining_balance = []
    interest_paid = []
    principal_paid = []
    total_paid = []
    dates = []
    monthly_payments = []
    
    balance = loan_amount
    total_interest = 0
    total_principal = 0
    
    start_date = date.today()
    
    for month in range(num_payments + 1):
        if month == 0:
            # Počáteční stav
            remaining_balance.append(balance)
            interest_paid.append(0)
            principal_paid.append(0)
            total_paid.append(0)
            monthly_payments.append(0)
        else:
            # Výpočet úroku a jistiny pro tento měsíc
            monthly_interest = balance * monthly_rate
            if balance > monthly_payment:
                this_payment = monthly_payment + extra_payment
                principal = this_payment - monthly_interest
            else:
                this_payment = balance + monthly_interest
                principal = balance
            
            # Aktualizace stavů
            balance = max(0, balance - principal)
            total_interest += monthly_interest
            total_principal += principal
            
            remaining_balance.append(balance)
            interest_paid.append(total_interest)
            principal_paid.append(total_principal)
            total_paid.append(total_principal + total_interest)
            monthly_payments.append(this_payment)
        
        dates.append(start_date + timedelta(days=30*month))
    
    return {
        'dates': dates,
        'remaining_balance': remaining_balance,
        'interest_paid': interest_paid,
        'principal_paid': principal_paid,
        'total_paid': total_paid,
        'monthly_payments': monthly_payments,
        'regular_payment': monthly_payment
    }

def show_mortgage_calculator():
    st.title("Hypoteční kalkulačka")
    
    # Vstupní parametry
    col1, col2 = st.columns(2)
    
    with col1:
        loan_amount = st.number_input(
            "Výše hypotéky (Kč)",
            min_value=100000,
            max_value=50000000,
            value=3000000,
            step=100000,
            format="%d"
        )
        
        interest_rate = st.number_input(
            "Úroková sazba (%)",
            min_value=0.1,
            max_value=20.0,
            value=5.9,
            step=0.1,
            format="%.1f"
        )
    
    with col2:
        years = st.number_input(
            "Doba splácení (roky)",
            min_value=1,
            max_value=40,
            value=30,
            step=1
        )
        
        extra_payment = st.number_input(
            "Mimořádná měsíční splátka (Kč)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=1000,
            format="%d"
        )
    
    # Výpočet hypotéky
    mortgage_data = calculate_mortgage(loan_amount, interest_rate, years, extra_payment)
    
    # Zobrazení měsíční splátky a souhrnů
    st.header("Výsledky hypotéky")
    
    result_cols = st.columns(4)
    with result_cols[0]:
        st.metric(
            "Měsíční splátka",
            f"{mortgage_data['regular_payment']:,.0f} Kč"
        )
    with result_cols[1]:
        st.metric(
            "Celkem zaplaceno",
            f"{mortgage_data['total_paid'][-1]:,.0f} Kč"
        )
    with result_cols[2]:
        st.metric(
            "Zaplaceno na úrocích",
            f"{mortgage_data['interest_paid'][-1]:,.0f} Kč"
        )
    with result_cols[3]:
        st.metric(
            "Efektivní úrok",
            f"{(mortgage_data['interest_paid'][-1] / loan_amount * 100):,.1f} %"
        )
    
    # Graf průběhu hypotéky
    fig = go.Figure()
    
    # Přidání křivek pro jistinu a úroky
    fig.add_trace(go.Scatter(
        x=mortgage_data['dates'],
        y=mortgage_data['principal_paid'],
        name="Splacená jistina",
        fill='tozeroy',
        mode='none'
    ))
    
    fig.add_trace(go.Scatter(
        x=mortgage_data['dates'],
        y=mortgage_data['total_paid'],
        name="Celkem zaplaceno",
        fill='tonexty',
        mode='none'
    ))
    
    # Přidání křivky zbývající jistiny
    fig.add_trace(go.Scatter(
        x=mortgage_data['dates'],
        y=mortgage_data['remaining_balance'],
        name="Zbývající jistina",
        line=dict(color='red', dash='dash')
    ))
    
    # Úprava vzhledu
    fig.update_layout(
        title="Průběh splácení hypotéky",
        xaxis_title="Datum",
        yaxis_title="Částka (Kč)",
        showlegend=True,
        hovermode='x unified'
    )
    
    # Formátování osy Y
    fig.update_layout(
        yaxis=dict(
            tickformat=",.0f",
            ticksuffix=" Kč"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabulka s detaily
    if st.checkbox("Zobrazit detailní tabulku splátek"):
        df = pd.DataFrame({
            'Datum': mortgage_data['dates'],
            'Měsíční splátka': mortgage_data['monthly_payments'],
            'Zbývající jistina': mortgage_data['remaining_balance'],
            'Zaplacené úroky': mortgage_data['interest_paid'],
            'Zaplacená jistina': mortgage_data['principal_paid'],
            'Celkem zaplaceno': mortgage_data['total_paid']
        })
        
        # Formátování sloupců
        for col in df.columns:
            if col != 'Datum':
                df[col] = df[col].apply(lambda x: f"{x:,.0f} Kč")
        
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )
    
    # Vysvětlení výpočtu
    with st.expander("Jak se to počítá?"):
        st.write("""
        Výpočet hypotéky používá standardní vzorec pro anuitní splácení:
        
        1. Měsíční splátka se počítá podle vzorce:
           - Splátka = Výše_úvěru * (i * (1 + i)^n) / ((1 + i)^n - 1)
           - kde i je měsíční úroková sazba (roční/12)
           - a n je počet měsíců splácení
        
        2. Každá splátka se dělí na:
           - Úrok = Zbývající_jistina * měsíční_úroková_sazba
           - Jistina = Splátka - Úrok
        
        **Poznámky:**
        - Výpočet je zjednodušený a nezahrnuje poplatky
        - Předpokládá fixní úrokovou sazbu po celou dobu
        - Mimořádné splátky jsou přičítány každý měsíc k běžné splátce
        - Slouží pouze pro orientační výpočet
        """) 
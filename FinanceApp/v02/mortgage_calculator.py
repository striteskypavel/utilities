import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import date, timedelta

def calculate_mortgage(loan_amount, interest_rate, years, extra_payment=0, inflation_rate=0, property_appreciation=0, insurance=0, ltv=80):
    """Vypočítá detaily hypotéky včetně splátek a úroků s ohledem na inflaci a zhodnocení nemovitosti."""
    monthly_rate = interest_rate / 100 / 12
    monthly_inflation = (1 + inflation_rate/100) ** (1/12) - 1
    monthly_appreciation = (1 + property_appreciation/100) ** (1/12) - 1
    num_payments = years * 12
    
    # Výpočet celkové hodnoty nemovitosti z LTV
    property_value = loan_amount / (ltv / 100)
    
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
    real_values = []  # Hodnoty v reálných cenách (očištěné o inflaci)
    property_values = []  # Hodnoty nemovitosti v čase
    insurance_paid = []  # Celkem zaplacené pojištění
    
    balance = loan_amount
    total_interest = 0
    total_principal = 0
    total_insurance = 0
    inflation_factor = 1
    appreciation_factor = 1
    
    start_date = date.today()
    
    for month in range(num_payments + 1):
        if month == 0:
            # Počáteční stav
            remaining_balance.append(balance)
            interest_paid.append(0)
            principal_paid.append(0)
            total_paid.append(0)
            monthly_payments.append(0)
            real_values.append(0)
            property_values.append(property_value)  # Počáteční hodnota nemovitosti
            insurance_paid.append(0)
        else:
            # Aktualizace faktorů
            inflation_factor *= (1 + monthly_inflation)
            appreciation_factor *= (1 + monthly_appreciation)
            
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
            total_insurance += insurance
            
            remaining_balance.append(balance)
            interest_paid.append(total_interest)
            principal_paid.append(total_principal)
            total_paid.append(total_principal + total_interest + total_insurance)
            monthly_payments.append(this_payment + insurance)
            
            # Výpočet reálné hodnoty (očištěné o inflaci)
            real_value = (total_principal + total_interest + total_insurance) / inflation_factor
            real_values.append(real_value)
            
            # Výpočet aktuální hodnoty nemovitosti
            current_property_value = property_value * appreciation_factor
            property_values.append(current_property_value)
            
            insurance_paid.append(total_insurance)
        
        dates.append(start_date + timedelta(days=30*month))
    
    return {
        'dates': dates,
        'remaining_balance': remaining_balance,
        'interest_paid': interest_paid,
        'principal_paid': principal_paid,
        'total_paid': total_paid,
        'monthly_payments': monthly_payments,
        'regular_payment': monthly_payment,
        'real_values': real_values,
        'property_values': property_values,
        'insurance_paid': insurance_paid,
        'property_value': property_value
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
            format="%d",
            help="Celková výše hypotéky, kterou chcete získat od banky"
        )
        
        interest_rate = st.number_input(
            "Úroková sazba (%)",
            min_value=0.1,
            max_value=20.0,
            value=5.9,
            step=0.1,
            format="%.1f",
            help="Roční úroková sazba hypotéky"
        )
    
    with col2:
        years = st.number_input(
            "Doba splácení (roky)",
            min_value=1,
            max_value=40,
            value=30,
            step=1,
            help="Doba, po kterou budete hypotéku splácet"
        )
        
        extra_payment = st.number_input(
            "Mimořádná měsíční splátka (Kč)",
            min_value=0,
            max_value=1000000,
            value=0,
            step=1000,
            format="%d",
            help="Dobrovolná měsíční mimořádná splátka navíc k běžné splátce"
        )
    
    # Přidání inflace, zhodnocení nemovitosti a pojištění
    col3, col4 = st.columns(2)
    
    with col3:
        inflation_rate = st.number_input(
            "Předpokládaná roční inflace (%)",
            min_value=0.0,
            max_value=20.0,
            value=2.0,
            step=0.1,
            format="%.1f",
            help="Očekávaná roční míra inflace, která ovlivní reálnou hodnotu peněz"
        )
    
    with col4:
        property_appreciation = st.number_input(
            "Očekávané roční zhodnocení nemovitosti (%)",
            min_value=-20.0,
            max_value=20.0,
            value=3.0,
            step=0.1,
            format="%.1f",
            help="Očekávané roční zhodnocení hodnoty nemovitosti"
        )
    
    # Přidání pojištění a LTV
    col5, col6 = st.columns(2)
    
    with col5:
        insurance = st.number_input(
            "Měsíční pojištění nemovitosti (Kč)",
            min_value=0,
            max_value=10000,
            value=500,
            step=100,
            format="%d",
            help="Měsíční náklady na pojištění nemovitosti"
        )
    
    with col6:
        ltv = st.number_input(
            "LTV - Loan to Value (%)",
            min_value=0,
            max_value=100,
            value=80,
            step=5,
            help="Poměr výše hypotéky k hodnotě nemovitosti. Vyšší LTV znamená vyšší riziko pro banku a může vést k vyšší úrokové sazbě"
        )
    
    # Výpočet hypotéky
    mortgage_data = calculate_mortgage(loan_amount, interest_rate, years, extra_payment, inflation_rate, property_appreciation, insurance, ltv)
    
    # Zobrazení měsíční splátky a souhrnů
    st.header("Výsledky hypotéky")
    
    result_cols = st.columns(4)
    with result_cols[0]:
        st.metric(
            "Měsíční splátka vč. pojištění",
            f"{mortgage_data['regular_payment'] + insurance:,.0f} Kč",
            help="Celková měsíční splátka včetně pojištění nemovitosti"
        )
    with result_cols[1]:
        st.metric(
            "Celkem zaplaceno",
            f"{mortgage_data['total_paid'][-1]:,.0f} Kč",
            help="Celková částka, kterou zaplatíte za celou dobu splácení včetně úroků a pojištění"
        )
    with result_cols[2]:
        st.metric(
            "Zaplaceno na úrocích",
            f"{mortgage_data['interest_paid'][-1]:,.0f} Kč",
            help="Celková částka zaplacená na úrocích za celou dobu splácení"
        )
    with result_cols[3]:
        real_interest_rate = (mortgage_data['interest_paid'][-1] / loan_amount * 100) - inflation_rate
        st.metric(
            "Reálný efektivní úrok",
            f"{real_interest_rate:,.1f} %",
            help="Efektivní úrok očištěný o inflaci"
        )
    
    # Zobrazení hodnoty nemovitosti a pojištění
    st.subheader("Hodnota nemovitosti a pojištění")
    property_cols = st.columns(2)
    
    with property_cols[0]:
        final_property_value = mortgage_data['property_values'][-1]
        property_appreciation_amount = final_property_value - mortgage_data['property_value']
        st.metric(
            "Konečná hodnota nemovitosti",
            f"{final_property_value:,.0f} Kč",
            f"{property_appreciation_amount:,.0f} Kč",
            help="Hodnota nemovitosti na konci splácení včetně zhodnocení"
        )
    
    with property_cols[1]:
        real_property_value = final_property_value / ((1 + inflation_rate/100) ** years)
        real_appreciation = real_property_value - mortgage_data['property_value']
        st.metric(
            "Reálná hodnota nemovitosti",
            f"{real_property_value:,.0f} Kč",
            f"{real_appreciation:,.0f} Kč",
            help="Hodnota nemovitosti očištěná o inflaci"
        )
    
    # Zobrazení celkových nákladů na pojištění
    st.subheader("Náklady na pojištění")
    insurance_cols = st.columns(2)
    
    with insurance_cols[0]:
        total_insurance = mortgage_data['insurance_paid'][-1]
        st.metric(
            "Celkem zaplaceno na pojištění",
            f"{total_insurance:,.0f} Kč",
            help="Celková částka zaplacená na pojištění nemovitosti za celou dobu splácení"
        )
    
    with insurance_cols[1]:
        real_insurance = total_insurance / ((1 + inflation_rate/100) ** years)
        st.metric(
            "Reálná hodnota pojištění",
            f"{real_insurance:,.0f} Kč",
            help="Celková částka zaplacená na pojištění očištěná o inflaci"
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
        y=[y + mortgage_data['insurance_paid'][i] for i, y in enumerate(mortgage_data['total_paid'])],
        name="Celkem zaplaceno vč. pojištění",
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
    
    # Přidání křivky reálné hodnoty
    fig.add_trace(go.Scatter(
        x=mortgage_data['dates'],
        y=mortgage_data['real_values'],
        name="Reálná hodnota (očištěná o inflaci)",
        line=dict(color='green', dash='dot')
    ))
    
    # Přidání křivky hodnoty nemovitosti
    fig.add_trace(go.Scatter(
        x=mortgage_data['dates'],
        y=mortgage_data['property_values'],
        name="Hodnota nemovitosti",
        line=dict(color='purple', dash='dot')
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
            'Měsíční splátka vč. pojištění': mortgage_data['monthly_payments'],
            'Zbývající jistina': mortgage_data['remaining_balance'],
            'Zaplacené úroky': mortgage_data['interest_paid'],
            'Zaplacená jistina': mortgage_data['principal_paid'],
            'Zaplacené pojištění': mortgage_data['insurance_paid'],
            'Celkem zaplaceno': mortgage_data['total_paid'],
            'Reálná hodnota': mortgage_data['real_values'],
            'Hodnota nemovitosti': mortgage_data['property_values']
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
        st.write(f"""
        Výpočet hypotéky používá standardní vzorec pro anuitní splácení s ohledem na inflaci, zhodnocení nemovitosti a pojištění:
        
        1. Měsíční splátka se počítá podle vzorce:
           - Splátka = Výše_úvěru * (i * (1 + i)^n) / ((1 + i)^n - 1)
           - kde i je měsíční úroková sazba (roční/12)
           - a n je počet měsíců splácení
        
        2. Každá splátka se dělí na:
           - Úrok = Zbývající_jistina * měsíční_úroková_sazba
           - Jistina = Splátka - Úrok
           - Pojištění = Měsíční pojištění
        
        3. Zohlednění inflace:
           - Měsíční inflace = (1 + roční_inflace)^(1/12) - 1
           - Reálná hodnota = Nominální hodnota / (1 + inflace)^(počet_měsíců/12)
           - Reálný efektivní úrok = Nominální efektivní úrok - roční_inflace
        
        4. Zohlednění zhodnocení nemovitosti:
           - Měsíční zhodnocení = (1 + roční_zhodnocení)^(1/12) - 1
           - Hodnota nemovitosti = Počáteční_hodnota * (1 + zhodnocení)^(počet_měsíců/12)
           - Reálná hodnota nemovitosti = Hodnota_nemovitosti / (1 + inflace)^(počet_let)
        
        **Poznámky:**
        - Výpočet je zjednodušený a nezahrnuje poplatky
        - Předpokládá fixní úrokovou sazbu po celou dobu
        - Předpokládá konstantní roční inflaci {inflation_rate}%
        - Předpokládá konstantní roční zhodnocení nemovitosti {property_appreciation}%
        - Předpokládá konstantní měsíční pojištění {insurance} Kč
        - LTV (Loan to Value) je nastaveno na {ltv}%
        - Mimořádné splátky jsou přičítány každý měsíc k běžné splátce
        - Slouží pouze pro orientační výpočet
        """) 
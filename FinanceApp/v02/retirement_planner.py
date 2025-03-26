import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def calculate_retirement_plan(
    current_age: int,
    retirement_age: int,
    life_expectancy: int,
    current_income: float,
    income_growth: float,
    current_savings: float,
    monthly_savings: float,
    investment_return: float,
    inflation_rate: float
) -> dict:
    """
    Vypočítá plán důchodu s ohledem na různé parametry.
    
    Args:
        current_age: Aktuální věk
        retirement_age: Věk odchodu do důchodu
        life_expectancy: Očekávaný věk dožití
        current_income: Aktuální měsíční příjem
        income_growth: Očekávaný roční růst příjmu (%)
        current_savings: Aktuální úspory
        monthly_savings: Měsíční úspory
        investment_return: Očekávaný roční výnos z investic (%)
        inflation_rate: Očekávaná roční inflace (%)
    
    Returns:
        dict: Slovník s výsledky výpočtu
    """
    # Převod procent na desetinná čísla
    income_growth = income_growth / 100
    investment_return = investment_return / 100
    inflation_rate = inflation_rate / 100
    
    # Výpočet počtu let do důchodu a v důchodu
    years_to_retirement = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age
    
    # Výpočet budoucí hodnoty úspor
    future_savings = current_savings * (1 + investment_return) ** years_to_retirement
    
    # Výpočet budoucí hodnoty měsíčních úspor
    monthly_investment_return = (1 + investment_return) ** (1/12) - 1
    future_monthly_savings = 0
    for year in range(years_to_retirement):
        future_monthly_savings += monthly_savings * 12 * (1 + investment_return) ** (years_to_retirement - year - 1)
    
    # Celkové úspory v době odchodu do důchodu
    total_savings_at_retirement = future_savings + future_monthly_savings
    
    # Výpočet budoucího příjmu v době odchodu do důchodu
    future_income = current_income * (1 + income_growth) ** years_to_retirement
    
    # Výpočet potřebného příjmu v důchodu (70% posledního příjmu)
    required_retirement_income = future_income * 0.7
    
    # Výpočet měsíčního příjmu z úspor v důchodu
    monthly_investment_income = total_savings_at_retirement * monthly_investment_return
    
    # Výpočet reálné hodnoty úspor v důchodu (očištěné o inflaci)
    real_savings = total_savings_at_retirement / ((1 + inflation_rate) ** years_to_retirement)
    
    # Výpočet reálného příjmu v důchodu (očištěného o inflaci)
    real_retirement_income = required_retirement_income / ((1 + inflation_rate) ** years_to_retirement)
    
    return {
        'years_to_retirement': years_to_retirement,
        'years_in_retirement': years_in_retirement,
        'total_savings_at_retirement': total_savings_at_retirement,
        'future_income': future_income,
        'required_retirement_income': required_retirement_income,
        'monthly_investment_income': monthly_investment_income,
        'real_savings': real_savings,
        'real_retirement_income': real_retirement_income,
        'monthly_savings_needed': required_retirement_income - monthly_investment_income
    }

def calculate_graph_data(
    current_age: int,
    retirement_age: int,
    life_expectancy: int,
    current_income: float,
    income_growth: float,
    current_savings: float,
    monthly_savings: float,
    investment_return: float,
    inflation_rate: float
) -> pd.DataFrame:
    """
    Vypočítá data pro graf vývoje úspor a příjmů v čase.
    """
    # Převod procent na desetinná čísla
    income_growth = income_growth / 100
    investment_return = investment_return / 100
    inflation_rate = inflation_rate / 100
    
    # Výpočet počtu let
    years_to_retirement = retirement_age - current_age
    years_in_retirement = life_expectancy - retirement_age
    total_years = years_to_retirement + years_in_retirement
    
    # Vytvoření seznamu let
    years = list(range(current_age, life_expectancy + 1))
    
    # Výpočet dat pro každý rok
    data = []
    current_savings_value = current_savings
    current_income_value = current_income
    
    for year in range(total_years + 1):
        age = current_age + year
        is_retired = age >= retirement_age
        
        # Výpočet úspor
        if year > 0:
            # Přidání měsíčních úspor
            current_savings_value += monthly_savings * 12
            # Výnos z investic
            current_savings_value *= (1 + investment_return)
        
        # Výpočet příjmu
        if not is_retired:
            current_income_value *= (1 + income_growth)
        
        # Výpočet reálných hodnot (očištěných o inflaci)
        real_savings = current_savings_value / ((1 + inflation_rate) ** year)
        real_income = current_income_value / ((1 + inflation_rate) ** year)
        
        data.append({
            'Věk': age,
            'Úspory': current_savings_value,
            'Příjem': current_income_value if not is_retired else 0,
            'Reálné úspory': real_savings,
            'Reálný příjem': real_income if not is_retired else 0,
            'Důchod': current_income_value * 0.7 if is_retired else 0,
            'Reálný důchod': (current_income_value * 0.7) / ((1 + inflation_rate) ** year) if is_retired else 0
        })
    
    return pd.DataFrame(data)

def show_retirement_planning():
    """Zobrazí formulář pro plánování důchodu"""
    st.title("Plánování důchodu")
    
    # Vysvětlení kalkulačky
    st.markdown("""
    Tato kalkulačka vám pomůže naplánovat finanční zabezpečení pro důchod. Zohledňuje:
    - Růst vašeho příjmu v průběhu kariéry
    - Inflaci a její vliv na kupní sílu
    - Výnosy z investic
    - Délku pobytu v důchodu
    
    Výsledky jsou orientační a slouží jako základ pro vaše finanční plánování.
    """)
    
    # Vstupní parametry
    col1, col2 = st.columns(2)
    
    with col1:
        current_age = st.number_input(
            "Aktuální věk",
            min_value=18,
            max_value=100,
            value=30,
            step=1,
            help="Zadejte svůj aktuální věk. Tato hodnota se používá pro výpočet počtu let do důchodu."
        )
        
        retirement_age = st.number_input(
            "Věk odchodu do důchodu",
            min_value=current_age,
            max_value=100,
            value=65,
            step=1,
            help="Věk, ve kterém plánujete odejít do důchodu. Může se lišit od oficiálního důchodového věku."
        )
        
        life_expectancy = st.number_input(
            "Očekávaný věk dožití",
            min_value=retirement_age,
            max_value=120,
            value=85,
            step=1,
            help="Očekávaný věk dožití pro výpočet délky pobytu v důchodu. Můžete použít průměrnou délku života nebo vlastní odhad."
        )
    
    with col2:
        current_income = st.number_input(
            "Aktuální měsíční příjem (Kč)",
            min_value=0,
            max_value=1000000,
            value=50000,
            step=1000,
            format="%d",
            help="Váš současný měsíční příjem. Tato hodnota se používá jako základ pro výpočet budoucího příjmu a potřebného důchodu."
        )
        
        income_growth = st.number_input(
            "Očekávaný roční růst příjmu (%)",
            min_value=0.0,
            max_value=20.0,
            value=2.0,
            step=0.1,
            format="%.1f",
            help="Očekávaný průměrný roční růst vašeho příjmu v procentech. Zohledňuje kariérní postup, inflaci a další faktory."
        )
        
        current_savings = st.number_input(
            "Aktuální úspory (Kč)",
            min_value=0,
            max_value=10000000,
            value=100000,
            step=10000,
            format="%d",
            help="Celková výše vašich současných úspor určených pro důchod. Zahrnuje penzijní fondy, investice a další úspory."
        )
    
    # Další parametry
    col3, col4 = st.columns(2)
    
    with col3:
        monthly_savings = st.number_input(
            "Měsíční úspory (Kč)",
            min_value=0,
            max_value=100000,
            value=5000,
            step=1000,
            format="%d",
            help="Měsíční částka, kterou pravidelně ukládáte pro důchod. Zahrnuje příspěvky do penzijního fondu a další pravidelné úspory."
        )
        
        investment_return = st.number_input(
            "Očekávaný roční výnos z investic (%)",
            min_value=0.0,
            max_value=20.0,
            value=5.0,
            step=0.1,
            format="%.1f",
            help="Očekávaný průměrný roční výnos z vašich investic v procentech. Zohledňuje typ investic a tržní podmínky."
        )
    
    with col4:
        inflation_rate = st.number_input(
            "Očekávaná roční inflace (%)",
            min_value=0.0,
            max_value=20.0,
            value=2.0,
            step=0.1,
            format="%.1f",
            help="Očekávaná průměrná roční míra inflace v procentech. Používá se pro výpočet reálné hodnoty budoucích úspor a příjmů."
        )
    
    # Výpočet plánu důchodu
    if st.button("Vypočítat plán důchodu"):
        results = calculate_retirement_plan(
            current_age=current_age,
            retirement_age=retirement_age,
            life_expectancy=life_expectancy,
            current_income=current_income,
            income_growth=income_growth,
            current_savings=current_savings,
            monthly_savings=monthly_savings,
            investment_return=investment_return,
            inflation_rate=inflation_rate
        )
        
        # Výpočet dat pro graf
        graph_data = calculate_graph_data(
            current_age=current_age,
            retirement_age=retirement_age,
            life_expectancy=life_expectancy,
            current_income=current_income,
            income_growth=income_growth,
            current_savings=current_savings,
            monthly_savings=monthly_savings,
            investment_return=investment_return,
            inflation_rate=inflation_rate
        )
        
        # Zobrazení výsledků
        st.subheader("Výsledky plánování důchodu")
        
        # Základní informace
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Let do důchodu",
                f"{results['years_to_retirement']}",
                help="Počet let, které vám zbývají do odchodu do důchodu. Vypočítáno jako rozdíl mezi důchodovým věkem a aktuálním věkem."
            )
        
        with col2:
            st.metric(
                "Let v důchodu",
                f"{results['years_in_retirement']}",
                help="Očekávaný počet let strávených v důchodu. Vypočítáno jako rozdíl mezi očekávaným věkem dožití a důchodovým věkem."
            )
        
        with col3:
            st.metric(
                "Budoucí měsíční příjem",
                f"{results['future_income']:,.0f} Kč",
                help="Váš měsíční příjem v době odchodu do důchodu. Vypočítán s ohledem na očekávaný růst příjmu."
            )
        
        # Úspory a příjmy v důchodu
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.metric(
                "Úspory v důchodu",
                f"{results['total_savings_at_retirement']:,.0f} Kč",
                help="Celková výše vašich úspor v době odchodu do důchodu. Zahrnuje současné úspory a budoucí úspory včetně výnosů z investic."
            )
        
        with col5:
            st.metric(
                "Potřebný měsíční příjem v důchodu",
                f"{results['required_retirement_income']:,.0f} Kč",
                help="Měsíční příjem, který budete potřebovat v důchodu. Vypočítán jako 70% vašeho posledního příjmu před důchodem."
            )
        
        with col6:
            st.metric(
                "Měsíční příjem z úspor",
                f"{results['monthly_investment_income']:,.0f} Kč",
                help="Měsíční příjem, který můžete očekávat z vašich úspor v důchodu. Vypočítán na základě očekávaného výnosu z investic."
            )
        
        # Reálné hodnoty
        st.subheader("Reálné hodnoty (očištěné o inflaci)")
        
        col7, col8, col9 = st.columns(3)
        
        with col7:
            st.metric(
                "Reálná hodnota úspor",
                f"{results['real_savings']:,.0f} Kč",
                help="Reálná hodnota vašich úspor v době odchodu do důchodu. Hodnota očištěná o inflaci ukazuje skutečnou kupní sílu vašich úspor."
            )
        
        with col8:
            st.metric(
                "Reálný příjem v důchodu",
                f"{results['real_retirement_income']:,.0f} Kč",
                help="Reálná hodnota potřebného příjmu v důchodu. Hodnota očištěná o inflaci ukazuje, kolik budete skutečně potřebovat pro zachování životní úrovně."
            )
        
        with col9:
            st.metric(
                "Doporučené měsíční úspory",
                f"{results['monthly_savings_needed']:,.0f} Kč",
                help="Doporučená měsíční částka k úspoře pro dosažení požadovaného příjmu v důchodu. Rozdíl mezi potřebným příjmem a očekávaným příjmem z úspor."
            )
        
        # Graf vývoje úspor a příjmů
        st.subheader("Vývoj úspor a příjmů v čase")
        
        # Vytvoření grafu pomocí Plotly
        fig = go.Figure()
        
        # Přidání stop pro nominální hodnoty
        fig.add_trace(go.Scatter(
            x=graph_data['Věk'],
            y=graph_data['Úspory'],
            name='Úspory',
            line=dict(color='blue')
        ))
        
        fig.add_trace(go.Scatter(
            x=graph_data['Věk'],
            y=graph_data['Příjem'],
            name='Příjem',
            line=dict(color='green')
        ))
        
        fig.add_trace(go.Scatter(
            x=graph_data['Věk'],
            y=graph_data['Důchod'],
            name='Důchod',
            line=dict(color='red')
        ))
        
        # Přidání stop pro reálné hodnoty
        fig.add_trace(go.Scatter(
            x=graph_data['Věk'],
            y=graph_data['Reálné úspory'],
            name='Reálné úspory',
            line=dict(color='lightblue', dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=graph_data['Věk'],
            y=graph_data['Reálný příjem'],
            name='Reálný příjem',
            line=dict(color='lightgreen', dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=graph_data['Věk'],
            y=graph_data['Reálný důchod'],
            name='Reálný důchod',
            line=dict(color='pink', dash='dash')
        ))
        
        # Úprava vzhledu grafu
        fig.update_layout(
            title='Vývoj úspor a příjmů v čase',
            xaxis_title='Věk',
            yaxis_title='Částka (Kč)',
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Zobrazení grafu
        st.plotly_chart(fig, use_container_width=True)
        
        # Vysvětlení výpočtu
        with st.expander("Jak se to počítá?"):
            st.write(f"""
            Výpočet plánu důchodu zohledňuje následující parametry:
            
            1. Časové parametry:
               - Aktuální věk: {current_age} let
               - Věk odchodu do důchodu: {retirement_age} let
               - Očekávaný věk dožití: {life_expectancy} let
               - Let do důchodu: {results['years_to_retirement']} let
               - Let v důchodu: {results['years_in_retirement']} let
            
            2. Finanční parametry:
               - Aktuální měsíční příjem: {current_income:,.0f} Kč
               - Očekávaný roční růst příjmu: {income_growth:.1f}%
               - Aktuální úspory: {current_savings:,.0f} Kč
               - Měsíční úspory: {monthly_savings:,.0f} Kč
               - Očekávaný roční výnos z investic: {investment_return:.1f}%
               - Očekávaná roční inflace: {inflation_rate:.1f}%
            
            3. Výpočty:
               - Budoucí hodnota úspor = Aktuální úspory * (1 + výnos)^let_do_důchodu
               - Budoucí hodnota měsíčních úspor = Suma(Úspory * (1 + výnos)^zbývající_roky)
               - Budoucí příjem = Aktuální příjem * (1 + růst)^let_do_důchodu
               - Potřebný příjem v důchodu = 70% budoucího příjmu
               - Reálné hodnoty = Nominální hodnoty / (1 + inflace)^let_do_důchodu
            
            **Poznámky:**
            - Výpočet je zjednodušený a nezahrnuje všechny faktory
            - Předpokládá konstantní růst příjmu {income_growth}% ročně
            - Předpokládá konstantní výnos z investic {investment_return}% ročně
            - Předpokládá konstantní inflaci {inflation_rate}% ročně
            - Slouží pouze pro orientační výpočet
            """) 
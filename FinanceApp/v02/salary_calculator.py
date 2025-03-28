import streamlit as st
import pandas as pd
import numpy as np

def calculate_salary(gross_salary, children_count=0, disability_level=0, ztp=False, working_pensioner=False, 
                    children_ztp=False, first_child=False, second_child=False, third_child=False, 
                    fourth_child=False, fifth_child=False, sixth_child=False, seventh_child=False, 
                    eighth_child=False, ninth_child=False, tenth_child=False,
                    spouse_caring_for_child=False, spouse_ztp_caring_for_child=False,
                    low_emission_car=False, car_price=0,
                    mortgage_interest=0, donations=0, pension_insurance=0, research_contribution=0):
    """
    Vypočítá čistou mzdu z hrubé mzdy s ohledem na všechny slevy a odpočty.
    
    Args:
        gross_salary (float): Hrubá mzda
        children_count (int): Počet nezaopatřených dětí
        disability_level (int): Stupeň invalidity (0-3)
        ztp (bool): Zda má zaměstnanec průkaz ZTP/P
        working_pensioner (bool): Zda je zaměstnanec pracující důchodce
        children_ztp (bool): Zda některé z dětí má průkaz ZTP/P
        first_child (bool): Zda je první dítě
        second_child (bool): Zda je druhé dítě
        third_child (bool): Zda je třetí dítě
        fourth_child (bool): Zda je čtvrté dítě
        fifth_child (bool): Zda je páté dítě
        sixth_child (bool): Zda je šesté dítě
        seventh_child (bool): Zda je sedmé dítě
        eighth_child (bool): Zda je osmé dítě
        ninth_child (bool): Zda je deváté dítě
        tenth_child (bool): Zda je desáté dítě
        spouse_caring_for_child (bool): Zda manžel/ka pečuje o dítě do 3 let
        spouse_ztp_caring_for_child (bool): Zda manžel/ka s ZTP/P pečuje o dítě do 3 let
        low_emission_car (bool): Zda má zaměstnanec nízkoemisní služební auto
        car_price (float): Cena služebního auta
        mortgage_interest (float): Úroky z úvěru na bydlení
        donations (float): Dary a dárcovství
        pension_insurance (float): Příspěvky na penzijní pojištění
        research_contribution (float): Příspěvky na výzkum
    
    Returns:
        dict: Slovník s výsledky výpočtu
    """
    # Základní parametry pro rok 2025
    SOCIAL_INSURANCE_RATE = 0.065  # 6.5% sociální pojištění
    HEALTH_INSURANCE_RATE = 0.045  # 4.5% zdravotní pojištění
    TAX_RATE = 0.15  # 15% daň z příjmů
    TAX_FREE_AMOUNT = 30960  # Roční nezdanitelná částka
    CHILD_TAX_CREDIT = 12600  # Roční daňové zvýhodnění na dítě
    
    # Výpočet pojistného
    social_insurance = gross_salary * SOCIAL_INSURANCE_RATE
    health_insurance = gross_salary * HEALTH_INSURANCE_RATE
    total_insurance = social_insurance + health_insurance
    
    # Výpočet daňového základu
    tax_base = gross_salary - total_insurance
    
    # Výpočet daňových slev
    tax_deductions = TAX_FREE_AMOUNT / 12  # Měsíční nezdanitelná částka
    
    # Daňové zvýhodnění na děti
    child_tax_credit = 0
    if first_child:
        child_tax_credit += CHILD_TAX_CREDIT / 12
    if second_child:
        child_tax_credit += CHILD_TAX_CREDIT / 12
    if third_child:
        child_tax_credit += CHILD_TAX_CREDIT / 12
    if fourth_child:
        child_tax_credit += CHILD_TAX_CREDIT / 12
    if fifth_child:
        child_tax_credit += CHILD_TAX_CREDIT / 12
    
    # Sleva na invaliditu
    disability_deduction = 0
    if disability_level == 1:
        disability_deduction = 210
    elif disability_level == 2:
        disability_deduction = 420
    elif disability_level == 3:
        disability_deduction = 1345
    
    # Sleva na ZTP/P
    ztp_deduction = 1345 if ztp else 0
    
    # Sleva na pracujícího důchodce
    pensioner_deduction = 210 if working_pensioner else 0
    
    # Výpočet daně
    tax = (tax_base - tax_deductions - child_tax_credit - disability_deduction - ztp_deduction - pensioner_deduction) * TAX_RATE
    
    # Výpočet čisté mzdy
    net_salary = gross_salary - total_insurance - tax
    
    # Výpočet celkových mzdových nákladů zaměstnavatele
    employer_social_insurance = gross_salary * 0.248  # 24.8% sociální pojištění zaměstnavatele
    employer_health_insurance = gross_salary * 0.09  # 9% zdravotní pojištění zaměstnavatele
    total_employer_costs = gross_salary + employer_social_insurance + employer_health_insurance
    
    return {
        "gross_salary": gross_salary,
        "social_insurance": social_insurance,
        "health_insurance": health_insurance,
        "total_insurance": total_insurance,
        "tax_base": tax_base,
        "tax": tax,
        "net_salary": net_salary,
        "employer_social_insurance": employer_social_insurance,
        "employer_health_insurance": employer_health_insurance,
        "total_employer_costs": total_employer_costs
    }

def show_salary_calculator():
    """Zobrazí kalkulačku čisté mzdy."""
    st.title("Kalkulačka čisté mzdy 2025")
    
    # Vytvoření dvou sloupců pro vstupní parametry
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Základní parametry")
        gross_salary = st.number_input(
            "Hrubá mzda (Kč)",
            min_value=0.0,
            step=1000.0,
            value=30000.0,
            help="Hrubá měsíční mzda"
        )
        
        children_count = st.number_input(
            "Počet nezaopatřených dětí",
            min_value=0,
            max_value=10,
            step=1,
            value=0,
            help="Počet nezaopatřených dětí"
        )
        
        if children_count > 0:
            st.subheader("Nastavení dětí")
            first_child = st.checkbox("První dítě", value=True)
            if children_count > 1:
                second_child = st.checkbox("Druhé dítě", value=True)
            if children_count > 2:
                third_child = st.checkbox("Třetí dítě", value=True)
            if children_count > 3:
                fourth_child = st.checkbox("Čtvrté dítě", value=True)
            if children_count > 4:
                fifth_child = st.checkbox("Páté dítě", value=True)
            if children_count > 5:
                sixth_child = st.checkbox("Šesté dítě", value=True)
            if children_count > 6:
                seventh_child = st.checkbox("Sedmé dítě", value=True)
            if children_count > 7:
                eighth_child = st.checkbox("Osmé dítě", value=True)
            if children_count > 8:
                ninth_child = st.checkbox("Deváté dítě", value=True)
            if children_count > 9:
                tenth_child = st.checkbox("Desáté dítě", value=True)
    
    with col2:
        st.subheader("Další parametry")
        disability_level = st.selectbox(
            "Invalidita",
            options=[("žádná", 0), ("1. stupeň", 1), ("2. stupeň", 2), ("3. stupeň", 3)],
            format_func=lambda x: x[0],
            help="Stupeň invalidity"
        )
        
        ztp = st.checkbox("Průkaz ZTP/P", help="Zda má zaměstnanec průkaz ZTP/P")
        working_pensioner = st.checkbox("Pracující důchodce", help="Zda je zaměstnanec pracující důchodce")
        children_ztp = st.checkbox("Některé z dětí ZTP/P", help="Zda některé z dětí má průkaz ZTP/P")
        
        spouse_caring_for_child = st.checkbox(
            "Manžel/ka pečující o dítě do 3 let",
            help="Manžel/ka pečující o dítě do 3 let nemá vlastní příjmy vyšší než 68 000 Kč"
        )
        
        spouse_ztp_caring_for_child = st.checkbox(
            "Manžel/ka s ZTP/P pečující o dítě do 3 let",
            help="Manžel/ka je držitel/ka ZTP/P pečující o dítě do 3 let nemá vlastní příjmy vyšší než 68 000 Kč"
        )
    
    # Výpočet výsledků
    results = calculate_salary(
        gross_salary=gross_salary,
        children_count=children_count,
        disability_level=disability_level[1],
        ztp=ztp,
        working_pensioner=working_pensioner,
        children_ztp=children_ztp,
        first_child=first_child if children_count > 0 else False,
        second_child=second_child if children_count > 1 else False,
        third_child=third_child if children_count > 2 else False,
        fourth_child=fourth_child if children_count > 3 else False,
        fifth_child=fifth_child if children_count > 4 else False,
        sixth_child=sixth_child if children_count > 5 else False,
        seventh_child=seventh_child if children_count > 6 else False,
        eighth_child=eighth_child if children_count > 7 else False,
        ninth_child=ninth_child if children_count > 8 else False,
        tenth_child=tenth_child if children_count > 9 else False,
        spouse_caring_for_child=spouse_caring_for_child,
        spouse_ztp_caring_for_child=spouse_ztp_caring_for_child
    )
    
    # Zobrazení výsledků
    st.subheader("Výsledky")
    
    # Vytvoření dvou sloupců pro výsledky
    result_col1, result_col2 = st.columns(2)
    
    with result_col1:
        st.metric(
            "Čistá mzda",
            f"{results['net_salary']:,.0f} Kč",
            help="Čistá měsíční mzda"
        )
        
        st.metric(
            "Roční čistá mzda",
            f"{results['net_salary'] * 12:,.0f} Kč",
            help="Roční čistá mzda"
        )
    
    with result_col2:
        st.metric(
            "Celkové mzdové náklady zaměstnavatele",
            f"{results['total_employer_costs']:,.0f} Kč",
            help="Celkové měsíční mzdové náklady zaměstnavatele"
        )
    
    # Detailní rozpis
    st.subheader("Detailní rozpis")
    
    # Vytvoření tabulky s rozpisem
    breakdown_data = {
        "Základ daně": f"{results['tax_base']:,.0f} Kč",
        "Pojistné zaměstnavatel": f"{results['employer_social_insurance'] + results['employer_health_insurance']:,.0f} Kč",
        "- z toho sociální pojištění": f"{results['employer_social_insurance']:,.0f} Kč",
        "- z toho zdravotní pojištění": f"{results['employer_health_insurance']:,.0f} Kč",
        "Hrubá mzda": f"{results['gross_salary']:,.0f} Kč",
        "Pojistné": f"{results['total_insurance']:,.0f} Kč",
        "- z toho sociální pojištění": f"{results['social_insurance']:,.0f} Kč",
        "- z toho zdravotní pojištění": f"{results['health_insurance']:,.0f} Kč",
        "Daň celkem": f"{results['tax']:,.0f} Kč",
        "Čistá mzda": f"{results['net_salary']:,.0f} Kč"
    }
    
    df = pd.DataFrame(list(breakdown_data.items()), columns=['Položka', 'Částka'])
    st.dataframe(df, hide_index=True, use_container_width=True) 
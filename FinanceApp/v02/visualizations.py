import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def show_pie_chart(data, height=400):
    """Zobrazí koláčový graf pro zobrazení rozložení financí."""
    # Vytvoření DataFrame pro graf
    df = pd.DataFrame(list(data.items()), columns=['Kategorie', 'Hodnota'])
    
    # Vytvoření koláčového grafu
    fig = px.pie(
        df,
        values='Hodnota',
        names='Kategorie',
        title='Rozložení financí podle kategorií',
        height=height
    )
    
    # Úprava vzhledu
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Zobrazení grafu
    st.plotly_chart(fig, use_container_width=True)

def show_history_chart(history, height=400):
    """Zobrazí graf historie změn."""
    if not history:
        return
    
    # Vytvoření DataFrame pro graf
    df = pd.DataFrame(history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Vytvoření grafu
    fig = go.Figure()
    
    # Přidání čar pro každou kategorii
    for category in df['category'].unique():
        cat_data = df[df['category'] == category]
        fig.add_trace(go.Scatter(
            x=cat_data['timestamp'],
            y=cat_data['new_value'],
            name=category,
            mode='lines+markers'
        ))
    
    # Úprava vzhledu
    fig.update_layout(
        title='Historie změn podle kategorií',
        xaxis_title='Datum',
        yaxis_title='Částka (Kč)',
        height=height,
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

def show_category_comparison(data, height=400):
    """Zobrazí sloupcový graf pro porovnání kategorií."""
    if not data:
        return
    
    # Vytvoření DataFrame pro graf
    totals = {cat: sum(item["amount"] for item in items) for cat, items in data.items()}
    df = pd.DataFrame({
        'Kategorie': list(totals.keys()),
        'Částka': list(totals.values())
    })
    
    # Seřazení podle částky vzestupně
    df = df.sort_values('Částka', ascending=True)
    
    # Vytvoření sloupcového grafu
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['Částka'],
        y=df['Kategorie'],
        orientation='h'
    ))
    
    # Úprava vzhledu
    fig.update_layout(
        title='Porovnání kategorií',
        xaxis_title='Částka (Kč)',
        yaxis_title='Kategorie',
        height=height,
        showlegend=False,
        hovermode='y unified'
    )
    
    # Formátování osy X
    fig.update_layout(
        xaxis=dict(
            tickformat=",.0f",
            ticksuffix=" Kč"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

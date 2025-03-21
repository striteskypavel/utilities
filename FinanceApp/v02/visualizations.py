import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def show_pie_chart(totals):
    df_pie = pd.DataFrame({
        "Kategorie": list(totals.keys()),
        "Hodnota": list(totals.values())
    })
    
    # Přidáme klíč "pie_chart_view_mode" k radio buttonu
    view_mode = st.radio(
        "Zobrazení grafu", 
        ["Hodnota v Kč", "% podíl"], 
        horizontal=True,
        key="pie_chart_view_mode"  # Unikátní klíč
    )
    
    # Vytvoříme kopii pro zachování původních hodnot
    df_display = df_pie.copy()
    
    if view_mode == "% podíl":
        df_display["Hodnota"] = df_display["Hodnota"] / df_display["Hodnota"].sum() * 100
        hover_template = "%{label}<br>%{value:.1f}%"
        value_format = ":.1f"
    else:
        hover_template = "%{label}<br>%{value:,.0f} Kč"
        value_format = ",.0f"
    
    fig_pie = px.pie(
        df_display,
        names="Kategorie",
        values="Hodnota",
        title="Rozložení financí",
        hole=0.4,
        width=700,
        height=500
    )
    
    # Aktualizace formátování a popisků
    if view_mode == "% podíl":
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent',  # Zobrazí pouze procenta
            hovertemplate=hover_template
        )
    else:
        fig_pie.update_traces(
            textposition='inside',
            textinfo='value',  # Zobrazí pouze hodnoty
            hovertemplate=hover_template,
            text=[f"{val:,.0f} Kč" for val in df_display["Hodnota"]],
        )
    
    st.plotly_chart(fig_pie)


def show_history_chart(history):
    if not history:
        st.info("Zatím nejsou k dispozici žádná historická data.")
        return
        
    df_history = pd.DataFrame(history)
    
    # Convert timestamp to datetime for better handling
    df_history['timestamp'] = pd.to_datetime(df_history['timestamp'])
    
    # Sort by timestamp
    df_history = df_history.sort_values('timestamp')
    
    # Add chart type selection
    chart_type = st.selectbox(
        "Typ grafu pro historii", 
        ["Čárový", "Sloupcový", "Plošný", "Bodový", "Histogram změn", "Tabulka"]
    )
    
    if chart_type == "Tabulka":
        # Format the timestamp for better readability
        df_display = df_history.copy()
        df_display['timestamp'] = df_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        df_display.columns = ['Kategorie', 'Původní hodnota', 'Nová hodnota', 'Časová značka']
        st.dataframe(df_display, use_container_width=True)
        return
    
    # For histogram, we need to calculate the change
    if chart_type == "Histogram změn":
        df_history['change'] = df_history['new_value'] - df_history['old_value']
        fig = px.histogram(
            df_history, 
            x='change', 
            color='category',
            title="Histogram změn hodnot",
            labels={'change': 'Změna hodnoty', 'count': 'Počet změn'},
            nbins=20
        )
        st.plotly_chart(fig)
        return
    
    # For other chart types
    y_axis = st.radio("Zobrazit hodnotu", ["new_value", "old_value"], 
                      format_func=lambda x: "Nová hodnota" if x == "new_value" else "Původní hodnota",
                      horizontal=True)
    
    if chart_type == "Čárový":
        fig = px.line(
            df_history, 
            x="timestamp", 
            y=y_axis, 
            color="category", 
            markers=True, 
            title="Vývoj hodnot v čase",
            labels={"timestamp": "Čas", y_axis: "Hodnota", "category": "Kategorie"}
        )
    
    elif chart_type == "Sloupcový":
        fig = px.bar(
            df_history, 
            x="timestamp", 
            y=y_axis, 
            color="category", 
            title="Vývoj hodnot v čase",
            labels={"timestamp": "Čas", y_axis: "Hodnota", "category": "Kategorie"}
        )
    
    elif chart_type == "Plošný":
        fig = px.area(
            df_history, 
            x="timestamp", 
            y=y_axis, 
            color="category", 
            title="Vývoj hodnot v čase",
            labels={"timestamp": "Čas", y_axis: "Hodnota", "category": "Kategorie"}
        )
    
    elif chart_type == "Bodový":
        fig = px.scatter(
            df_history, 
            x="timestamp", 
            y=y_axis, 
            color="category", 
            size=y_axis,  # Size points by value
            size_max=15,  # Maximum marker size
            hover_data=["old_value", "new_value"],
            title="Vývoj hodnot v čase",
            labels={"timestamp": "Čas", y_axis: "Hodnota", "category": "Kategorie"}
        )
    
    # Add date range selector
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="7D", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="Vše")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    st.plotly_chart(fig)

def show_category_comparison(data):
    """
    Show a comparison of categories using a bar chart.
    
    Args:
        data (dict): Dictionary with category data
    """
    if not data:
        st.info("Zatím nejsou k dispozici žádná data pro porovnání kategorií.")
        return
        
    # Calculate totals for each category
    totals = {cat: sum(item["amount"] for item in entries) for cat, entries in data.items()}
    
    df = pd.DataFrame({
        "Kategorie": list(totals.keys()),
        "Hodnota": list(totals.values())
    })
    
    # Sort by value
    sort_order = st.radio("Seřadit podle", ["Hodnoty (sestupně)", "Hodnoty (vzestupně)", "Abecedně"], horizontal=True)
    
    if sort_order == "Hodnoty (sestupně)":
        df = df.sort_values("Hodnota", ascending=False)
    elif sort_order == "Hodnoty (vzestupně)":
        df = df.sort_values("Hodnota", ascending=True)
    else:
        df = df.sort_values("Kategorie")
    
    fig = px.bar(
        df,
        x="Kategorie",
        y="Hodnota",
        title="Porovnání kategorií",
        text_auto='.2s',  # Add value labels on bars
        color="Kategorie"
    )
    
    # Improve layout
    fig.update_layout(
        xaxis_title="Kategorie",
        yaxis_title="Hodnota (Kč)",
        showlegend=False
    )
    
    st.plotly_chart(fig)

import streamlit as st
import plotly.express as px
import pandas as pd

def show_pie_chart(totals):
    df_pie = pd.DataFrame({
        "Kategorie": list(totals.keys()),
        "Hodnota": list(totals.values())
    })
    
    view_mode = st.radio("Zobrazení grafu", ["Hodnota v Kč", "% podíl"], horizontal=True)
    if view_mode == "% podíl":
        df_pie["Hodnota"] = df_pie["Hodnota"] / df_pie["Hodnota"].sum() * 100
    
    fig_pie = px.pie(df_pie, names="Kategorie", values="Hodnota", title="Rozložení financí", hole=0.4, width=700, height=500)
    st.plotly_chart(fig_pie)

def show_history_chart(history):
    df_history = pd.DataFrame(history)
    if not df_history.empty:
        fig = px.line(df_history, x="timestamp", y="new_value", color="category", markers=True, title="Vývoj hodnot v čase")
        st.plotly_chart(fig)

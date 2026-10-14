import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'Data' not in df.columns: return
    
    st.markdown("#### Evolução Temporal de Denúncias")
    
    df_tempo = df.groupby(df['Data'].dt.to_period("W")).size().reset_index(name='Casos')
    df_tempo['Data'] = df_tempo['Data'].dt.to_timestamp()
    
    fig_tempo = px.line(
        df_tempo, x='Data', y='Casos', markers=True, 
        title="Curva de Registos (Agrupamento Semanal)"
    )
    fig_tempo.update_traces(line_color='#CE1256', line_width=3, marker_size=6)
    
    st.plotly_chart(fig_tempo, use_container_width=True)
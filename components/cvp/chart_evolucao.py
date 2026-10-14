import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    st.markdown("#### Demanda Operacional e Evolução")
    col1, col2 = st.columns(2)
    
    with col1:
        if 'AIS' in df.columns:
            df_ais = df['AIS'].value_counts().reset_index()
            df_ais.columns = ['Área Integrada (AIS)', 'Ocorrências']
            
            fig_ais = px.bar(
                df_ais.head(10), x='Ocorrências', y='Área Integrada (AIS)', orientation='h',
                title="Top 10 Batalhões (AIS) Exigidos",
                color='Ocorrências', color_continuous_scale='Reds'
            )
            fig_ais.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_ais, use_container_width=True)

    with col2:
        if 'Data' in df.columns:
            df_tempo = df.groupby(df['Data'].dt.to_period("W")).size().reset_index(name='Casos')
            df_tempo['Data'] = df_tempo['Data'].dt.to_timestamp()
            
            fig_tempo = px.line(df_tempo, x='Data', y='Casos', markers=True, title="Evolução Semanal de Roubos")
            fig_tempo.update_traces(line_color='#CB181D', line_width=3, marker_size=6)
            st.plotly_chart(fig_tempo, use_container_width=True)
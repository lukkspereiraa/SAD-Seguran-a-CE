import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    col1, col2 = st.columns(2)
    
    # 1. Gráfico de Barras: Top 10 Municípios (Por volume de resgates)
    with col1:
        df_top_mun = df.groupby('Município').size().reset_index(name='Ocorrências')
        df_top_mun = df_top_mun.sort_values(by='Ocorrências', ascending=False).head(10)
        
        fig_mun = px.bar(
            df_top_mun,
            x='Ocorrências',
            y='Município',
            orientation='h',
            title="Top 10 Cidades (Volume Operacional)",
            color='Ocorrências',
            color_continuous_scale='Blues'
        )
        fig_mun.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_mun, use_container_width=True)

    # 2. Gráfico de Rosca: Top 5 AIS 
    with col2:
        df_ais = df.groupby('AIS').size().reset_index(name='Ocorrências')
        df_ais = df_ais.sort_values(by='Ocorrências', ascending=False).head(5)
        
        fig_ais = px.pie(
            df_ais, 
            values='Ocorrências', 
            names='AIS', 
            hole=0.4,
            title="Top 5 AIS (Concentração de Demanda)",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_ais.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_ais, use_container_width=True)

    st.divider()

    # 3. Evolução Temporal Mensal
    df_tempo = df.groupby(df['Data'].dt.to_period("M")).size().reset_index(name='Total de Ocorrências')
    df_tempo['Data'] = df_tempo['Data'].dt.to_timestamp()
    
    fig_tempo = px.line(
        df_tempo, 
        x='Data', 
        y='Total de Ocorrências', 
        markers=True,
        title="Evolução Mensal de Chamados (Tendência)"
    )
    fig_tempo.update_traces(line_color='#1f77b4', line_width=3, marker_size=8)
    st.plotly_chart(fig_tempo, use_container_width=True)
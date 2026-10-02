import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    col1, col2 = st.columns(2)
    
    # 1. Gráfico de Barras: Top 10 Municípios (Por volume de armas)
    with col1:
        df_top_mun = df.groupby('Município')['Quantidade'].sum().reset_index()
        df_top_mun = df_top_mun.sort_values(by='Quantidade', ascending=False).head(10)
        
        fig_mun = px.bar(
            df_top_mun,
            x='Quantidade',
            y='Município',
            orientation='h',
            title="Top 10 Municípios (Volume de Armas)",
            color='Quantidade',
            color_continuous_scale='Reds' # Vermelho para o perigo bélico
        )
        fig_mun.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_mun, use_container_width=True)

    # 2. Gráfico de Rosca: Top 5 AIS (Concentração de apreensões)
    with col2:
        df_ais = df.groupby('AIS')['Quantidade'].sum().reset_index()
        df_ais = df_ais.sort_values(by='Quantidade', ascending=False).head(5)
        
        fig_ais = px.pie(
            df_ais, 
            values='Quantidade', 
            names='AIS', 
            hole=0.4,
            title="Top 5 AIS (Concentração de Apreensões)",
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig_ais.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_ais, use_container_width=True)

    st.divider()

    # 3. Evolução Temporal Mensal
    df_tempo = df.groupby(df['Data'].dt.to_period("M"))['Quantidade'].sum().reset_index(name='Armas Apreendidas')
    df_tempo['Data'] = df_tempo['Data'].dt.to_timestamp()
    
    fig_tempo = px.line(
        df_tempo, 
        x='Data', 
        y='Armas Apreendidas', 
        markers=True,
        title="Evolução Mensal do Desarmamento (Total de Armas)"
    )
    fig_tempo.update_traces(line_color='#8B0000', line_width=3, marker_size=8)
    st.plotly_chart(fig_tempo, use_container_width=True)
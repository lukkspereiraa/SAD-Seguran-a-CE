import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty:
        return
        
    st.markdown("### :material/monitoring: Dinâmica de Apreensões")
    
    col1, col2 = st.columns(2)
    
    # 1. Gráfico de Rosca: Proporção de Volume (Kg) por Tipo de Droga
    with col1:
        df_kg_tipo = df.groupby('Tipo de Entorpecente')['Quantidade (Kg)'].sum().reset_index()
        fig_tipo = px.pie(
            df_kg_tipo, 
            values='Quantidade (Kg)', 
            names='Tipo de Entorpecente', 
            hole=0.4,
            title="Volume Apreendido (Kg) por Tipo",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_tipo.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_tipo, use_container_width=True)
        
    # 2. Gráfico de Barras: Top 10 Municípios com mais volume (Kg)
    with col2:
        df_top_mun = df.groupby('Município')['Quantidade (Kg)'].sum().reset_index()
        df_top_mun = df_top_mun.sort_values(by='Quantidade (Kg)', ascending=False).head(10)
        
        fig_mun = px.bar(
            df_top_mun,
            x='Quantidade (Kg)',
            y='Município',
            orientation='h',
            title="Top 10 Municípios (Volume em Kg)",
            color='Quantidade (Kg)',
            color_continuous_scale='Reds'
        )
        fig_mun.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_mun, use_container_width=True)

    st.divider()

    # 3. Gráfico de Linha: Evolução das ocorrências ao longo do tempo
    st.markdown("### :material/timeline: Histórico de Ocorrências (Tráfico)")
    df_tempo = df.groupby(df['Data'].dt.to_period("M")).size().reset_index(name='Ocorrências')
    df_tempo['Data'] = df_tempo['Data'].dt.to_timestamp()
    
    fig_tempo = px.line(
        df_tempo, 
        x='Data', 
        y='Ocorrências', 
        markers=True,
        title="Frequência de Ocorrências Policiais por Mês"
    )
    fig_tempo.update_traces(line_color='#2E8B57', line_width=3, marker_size=8)
    st.plotly_chart(fig_tempo, use_container_width=True)
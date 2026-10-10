import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    st.markdown("#### :material/trending_up: Evolução Mensal e Territorial")
    col1, col2 = st.columns(2)
    
    with col1:
        df_top_mun = df.groupby('Município').size().reset_index(name='Casos')
        df_top_mun = df_top_mun.sort_values(by='Casos', ascending=False).head(10)
        
        fig_mun = px.bar(
            df_top_mun,
            x='Casos',
            y='Município',
            orientation='h',
            title="Top 10 Cidades (Volume Absoluto)",
            color='Casos',
            color_continuous_scale='Sunset'
        )
        fig_mun.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_mun, use_container_width=True)

    with col2:
        df_tempo = df.groupby(df['Data'].dt.to_period("M")).size().reset_index(name='Casos')
        df_tempo['Data'] = df_tempo['Data'].dt.to_timestamp()
        
        fig_tempo = px.line(
            df_tempo, 
            x='Data', 
            y='Casos', 
            markers=True,
            title="Linha de Tendência Mensal"
        )
        fig_tempo.update_traces(line_color='#FF007F', line_width=3, marker_size=8)
        st.plotly_chart(fig_tempo, use_container_width=True)
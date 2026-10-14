import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 10 Batalhões (AIS) Demandados")
        if 'AIS' in df.columns:
            df_ais = df['AIS'].value_counts().reset_index()
            df_ais.columns = ['AIS', 'Ocorrências']
            df_ais_top = df_ais.head(10).copy()
            
            fig_ais = px.bar(
                df_ais_top, x='Ocorrências', y='AIS', orientation='h',
                color='Ocorrências', color_continuous_scale='Greens'
            )
            fig_ais.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_ais, use_container_width=True)

    with col2:
        st.markdown("#### Evolução Temporal")
        if 'Data' in df.columns:
            df_tempo = df.groupby(df['Data'].dt.date).size().reset_index(name='Casos')
            df_tempo['Data'] = pd.to_datetime(df_tempo['Data'])
            
            fig_tempo = px.line(df_tempo, x='Data', y='Casos', markers=True)
            fig_tempo.update_traces(line_color='#006D2C', line_width=3, marker_size=6)
            st.plotly_chart(fig_tempo, use_container_width=True)
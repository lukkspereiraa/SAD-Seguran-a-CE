import streamlit as st
import plotly.express as px
import pandas as pd

def classificar_turno(hora_str):
    try:
        h = int(str(hora_str).split(':')[0])
        if 0 <= h < 6: return '1. Madrugada (00h-06h)'
        elif 6 <= h < 12: return '2. Manhã (06h-12h)'
        elif 12 <= h < 18: return '3. Tarde (12h-18h)'
        else: return '4. Noite (18h-00h)'
    except: return 'Não Informado'

def render(df):
    if df.empty: return
    
    st.markdown("#### Perfil Criminal (Turnos e Dias)")
    col1, col2 = st.columns(2)
    
    df_perfil = df.copy()
    df_perfil['Turno'] = df_perfil['Hora'].apply(classificar_turno)
    
    with col1:
        # Gráfico de Donut por Turno
        df_turno = df_perfil['Turno'].value_counts().reset_index()
        df_turno.columns = ['Turno', 'Total']
        df_turno = df_turno.sort_values('Turno')
        
        fig_turno = px.pie(
            df_turno, values='Total', names='Turno', hole=0.4, 
            title="Distribuição de Assaltos por Turno", 
            color_discrete_sequence=['#67000D', '#A50F15', '#EF3B2C', '#FC9272']
        )
        fig_turno.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_turno, use_container_width=True)
        
    with col2:
        # Gráfico de Barras por Dia da Semana
        df_dia = df_perfil['Dia da Semana'].value_counts().reset_index()
        df_dia.columns = ['Dia da Semana', 'Total']
        
        # Ordenar pelos dias mais perigosos
        fig_dia = px.bar(
            df_dia, x='Total', y='Dia da Semana', orientation='h',
            title="Ranking de Risco por Dia",
            color='Total', color_continuous_scale='Reds'
        )
        fig_dia.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_dia, use_container_width=True)
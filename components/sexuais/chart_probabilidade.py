import streamlit as st
import plotly.express as px
import pandas as pd

def classificar_turno(hora_str):
    try:
        h = int(str(hora_str).split(':')[0])
        if 0 <= h < 6: return '1. Madrugada'
        elif 6 <= h < 12: return '2. Manhã'
        elif 12 <= h < 18: return '3. Tarde'
        else: return '4. Noite'
    except: return 'Desconhecido'

def render(df):
    if df.empty or 'Hora' not in df.columns: return
    
    st.markdown("#### Matriz de Probabilidade Condicional de Denúncia")
    
    df_prob = df.copy()
    df_prob['Turno'] = df_prob['Hora'].apply(classificar_turno)
    
    df_cross = pd.crosstab(df_prob['Dia da Semana'], df_prob['Turno'], normalize='index') * 100
    ordem_dias = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    df_cross = df_cross.reindex(ordem_dias)
    
    fig_prob = px.imshow(
        df_cross,
        labels=dict(x="Turno Operacional", y="Dia da Semana", color="Probabilidade (%)"),
        x=df_cross.columns, y=df_cross.index,
        color_continuous_scale='PuRd', aspect="auto"
    )
    fig_prob.update_traces(texttemplate='%{z:.1f}%', textfont_size=14)
    fig_prob.update_xaxes(side="top")
    
    st.plotly_chart(fig_prob, use_container_width=True)
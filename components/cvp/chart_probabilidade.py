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
    
    st.markdown("#### Matriz de Probabilidade Condicional (Risco Preditivo)")
    st.info("Inteligência Preditiva: Esta matriz não mostra o passado em números absolutos, mas calcula a probabilidade matemática futura. Lê-se: 'Dado que hoje é um determinado dia da semana, existe X% de probabilidade de o evento criminal ocorrer neste turno'.")
    
    df_prob = df.copy()
    df_prob['Turno'] = df_prob['Hora'].apply(classificar_turno)
    
    # Matemática: Calcula a tabela cruzada normalizada pelas linhas (probabilidade condicional)
    # Multiplicamos por 100 para transformar em percentagem (0% a 100%)
    df_cross = pd.crosstab(df_prob['Dia da Semana'], df_prob['Turno'], normalize='index') * 100
    
    # Ordenar os dias de forma lógica na semana
    ordem_dias = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    df_cross = df_cross.reindex(ordem_dias)
    
    # Gráfico de Calor Preditivo
    fig_prob = px.imshow(
        df_cross,
        labels=dict(x="Turno Operacional", y="Dia da Semana", color="Probabilidade (%)"),
        x=df_cross.columns,
        y=df_cross.index,
        color_continuous_scale='Reds',
        aspect="auto"
    )
    
    # Ajustes visuais para injetar o símbolo de "%" dentro dos blocos
    fig_prob.update_traces(texttemplate='%{z:.1f}%', textfont_size=14)
    fig_prob.update_xaxes(side="top")
    fig_prob.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    
    st.plotly_chart(fig_prob, use_container_width=True)
    
    # Algoritmo para extrair automaticamente a maior probabilidade da matriz
    max_prob = df_cross.max().max()
    dia_max = df_cross.max(axis=1).idxmax()
    turno_max = df_cross.idxmax(axis=1)[dia_max]
    
    st.error(f"**Janela de Vulnerabilidade Crítica:** A análise estatística aponta que a maior probabilidade de ocorrência incide à **{dia_max}** no turno da **{turno_max}**, representando **{max_prob:.1f}%** de certeza de que os crimes violentos desse dia ocorrerão nesta faixa horária específica.")
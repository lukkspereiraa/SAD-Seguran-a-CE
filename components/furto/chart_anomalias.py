import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render(df):
    if df.empty or 'Data' not in df.columns: return

    st.markdown("#### :material/warning: Deteção Algorítmica de Anomalias (Z-Score)")
    st.info("Monitorização de Quebra de Padrão: Este modelo estatístico identifica automaticamente dias em que o volume de furtos ultrapassou o limite máximo esperado (2 desvios padrão acima da média), disparando um alerta tático.")

    # Agrupamento diário
    df_diario = df.groupby(df['Data'].dt.date).size().reset_index(name='Casos')
    df_diario['Data'] = pd.to_datetime(df_diario['Data'])

    if len(df_diario) < 2:
        st.warning("Dados insuficientes para calcular desvio padrão.")
        return

    # Matemática Estatística (Z-Score)
    media = df_diario['Casos'].mean()
    desvio_padrao = df_diario['Casos'].std()
    
    # Define o teto de tolerância (95% de confiança)
    limite_tolerancia = media + (2 * desvio_padrao)
    
    # Classificador Booleano
    df_diario['Anomalia'] = df_diario['Casos'] > limite_tolerancia
    df_diario['Classificação'] = df_diario['Anomalia'].map({True: 'Alerta Crítico (Outlier)', False: 'Volume Normal'})

    fig = px.scatter(
        df_diario, x='Data', y='Casos', color='Classificação',
        color_discrete_map={'Alerta Crítico (Outlier)': '#CB181D', 'Volume Normal': '#6BAED6'},
        title="Mapeamento de Picos Anormais de Criminalidade"
    )

    # Adiciona as linhas de referência estatística
    fig.add_hline(y=media, line_dash="dash", line_color="gray", annotation_text="Média Histórica")
    fig.add_hline(y=limite_tolerancia, line_dash="dot", line_color="red", annotation_text="Teto Estatístico (Z-Score > 2)")

    # Realça os pontos anómalos com um tamanho maior
    fig.update_traces(marker=dict(size=7), selector=dict(name='Volume Normal'))
    fig.update_traces(marker=dict(size=12, symbol='x'), selector=dict(name='Alerta Crítico (Outlier)'))

    st.plotly_chart(fig, use_container_width=True)

    # Sistema de Alerta Baseado em Regras
    total_anomalias = df_diario['Anomalia'].sum()
    if total_anomalias > 0:
        st.error(f" **Auditoria Necessária:** O algoritmo detetou **{total_anomalias} dia(s)** com um volume de furtos estatisticamente anormal. É imperativo analisar o contexto operacional destas datas (grandes eventos, manifestações ou ausência de policiamento).")
    else:
        st.success(" O volume de furtos manteve-se dentro do padrão estatístico esperado no período selecionado.")
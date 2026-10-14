import streamlit as st
import pandas as pd
from services.data_handler import filtrar_dados_animais

import components.animais.chart_mapa as chart_mapa
import components.animais.chart_temporal as chart_temporal
import components.animais.chart_evolucao as chart_evolucao

def render(df_animais, datas, municipios, ais):
    st.subheader("Crimes Ambientais (Maus-Tratos e Resgate de Animais)")
    
    with st.popover("Metodologia Institucional"):
        st.markdown("""
        **Diretrizes do Módulo:**
        Este painel reflete a atuação do Batalhão de Polícia de Meio Ambiente (BPMA).
        
        **Foco Tático:**
        As ocorrências de resgate e denúncias de maus-tratos ocorrem tipicamente em horário diurno, dependendo da visibilidade pública para a denúncia. A inteligência espacial ajuda a posicionar bases móveis do BPMA perto de feiras, mercados e áreas de abandono crónico.
        """)
        
    if df_animais.empty:
        st.warning("Base de dados não encontrada.")
        return df_animais

    df_filtrado = filtrar_dados_animais(df_animais, datas, municipios, ais)
    if df_filtrado.empty:
        st.warning("Nenhum registo encontrado com os filtros selecionados.")
        return df_filtrado

    # --- FILTROS LOCAIS ---
    st.markdown("##### Filtros ")
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        if 'Dia da Semana' in df_filtrado.columns:
            dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            filtro_dias = st.multiselect("Isolar Dia:", dias_semana, default=[], key="dias_animais")
        else: filtro_dias = []
            
    with col_f2:
        filtro_horas = st.slider("Horário (0h-23h):", 0, 23, (0, 23), key="horas_animais")

    if filtro_dias: df_filtrado = df_filtrado[df_filtrado['Dia da Semana'].isin(filtro_dias)]
    if 'Hora' in df_filtrado.columns:
        df_filtrado['Hora_Int'] = pd.to_datetime(df_filtrado['Hora'], format='%H:%M:%S', errors='coerce').dt.hour
        df_filtrado = df_filtrado[(df_filtrado['Hora_Int'] >= filtro_horas[0]) & (df_filtrado['Hora_Int'] <= filtro_horas[1])]

    if df_filtrado.empty:
        st.warning("Sem dados para esta combinação de filtros.")
        return df_filtrado

    # --- KPIs ---
    st.divider()
    kpi1, kpi2, kpi3 = st.columns(3)
    total_casos = df_filtrado.shape[0]
    
    kpi1.metric(label="Volume de Ocorrências", value=f"{total_casos:,}".replace(',', '.'))
    if total_casos > 0:
        kpi2.metric(label="Município Crítico", value=df_filtrado['Município'].mode()[0])
        if 'Dia da Semana' in df_filtrado.columns:
            kpi3.metric(label="Dia de Maior Demanda", value=df_filtrado['Dia da Semana'].mode()[0])
            
    st.divider()
    
    # --- RENDERIZAÇÃO DAS ABAS ---
    aba1, aba2, aba3 = st.tabs([
        "Geografia Ambiental",
        "Engenharia de Tempo",
        "Demanda de Batalhões (AIS)"
    ])
    
    with aba1:
        chart_mapa.render(df_filtrado)
    with aba2:
        chart_temporal.render(df_filtrado)
    with aba3:
        chart_evolucao.render(df_filtrado)
    
    return df_filtrado
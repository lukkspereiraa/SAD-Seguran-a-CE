import streamlit as st
import pandas as pd
from services.data_handler import filtrar_dados_incendios

import components.incendios.chart_mapa as chart_mapa
import components.incendios.chart_temporal as chart_temporal

def render(df_incendio, datas, municipios, ais):
    st.subheader("Incêndios (Operações CBMCE)")
    
    with st.popover("Metodologia de Bombeiros"):
        st.markdown("""
        **Foco Tático:**
        A análise das manchas de calor guia as equipas do Corpo de Bombeiros. Picos diurnos em regiões do interior sugerem queimadas rurais e fogos florestais em áreas secas.
        """)
        
    if df_incendio.empty:
        st.warning("Base de dados não encontrada.")
        return df_incendio

    df_filtrado = filtrar_dados_incendios(df_incendio, datas, municipios, ais)
    if df_filtrado.empty:
        st.warning("Nenhum registo encontrado com os filtros selecionados.")
        return df_filtrado

    # Filtros Drill-Down
    st.markdown("##### Filtros")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        if 'Dia da Semana' in df_filtrado.columns:
            dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            filtro_dias = st.multiselect("Isolar Dia:", dias_semana, default=[], key="dias_fogo")
        else: filtro_dias = []
    with col_f2:
        filtro_horas = st.slider("Horário (0h-23h):", 0, 23, (0, 23), key="horas_fogo")

    if filtro_dias: df_filtrado = df_filtrado[df_filtrado['Dia da Semana'].isin(filtro_dias)]
    if 'Hora' in df_filtrado.columns:
        df_filtrado['Hora_Int'] = pd.to_datetime(df_filtrado['Hora'], format='%H:%M:%S', errors='coerce').dt.hour
        df_filtrado = df_filtrado[(df_filtrado['Hora_Int'] >= filtro_horas[0]) & (df_filtrado['Hora_Int'] <= filtro_horas[1])]

    st.divider()
    kpi1, kpi2, kpi3 = st.columns(3)
    total_casos = df_filtrado.shape[0]
    
    kpi1.metric(label="Total de Focos Controlados", value=f"{total_casos:,}".replace(',', '.'))
    if total_casos > 0:
        kpi2.metric(label="Município mais Atingido", value=df_filtrado['Município'].mode()[0])
        if 'Dia da Semana' in df_filtrado.columns:
            kpi3.metric(label="Dia de Maior Pressão Térmica", value=df_filtrado['Dia da Semana'].mode()[0])
            
    st.divider()
    
    aba1, aba2 = st.tabs(["Geografia do Fogo", "Engenharia de Tempo (Picos)"])
    with aba1:
        chart_mapa.render(df_filtrado)
    with aba2:
        chart_temporal.render(df_filtrado)
    
    return df_filtrado
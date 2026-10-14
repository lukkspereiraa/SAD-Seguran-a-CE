import streamlit as st
from services.data_handler import filtrar_dados_furto

import components.furto.chart_mapa as chart_mapa
import components.furto.chart_matriz as chart_matriz
import components.furto.chart_evolucao as chart_evolucao
import components.furto.chart_avancado as chart_avancado
import components.furto.chart_patrulha as chart_patrulha

def render(df_furto, datas, municipios, ais):
    st.subheader("Furtos (Crimes contra o Património)")
    
    with st.popover("Metodologia e Leitura Tática"):
        st.markdown("""
        **Diretrizes de Leitura:**
        Registo de subtração de património sem uso de violência ou grave ameaça.
        
        **Foco Tático:**
        Devido ao volume massivo de dados (alta subnotificação vs alta incidência), a análise deve ser estritamente focada na identificação de Zonas Quentes (Hotspots) e Horários Críticos para alocação de policiamento ostensivo a pé e patrulhamento de área.
        """)
        
    if df_furto.empty:
        st.warning("Base de dados não encontrada.")
        return df_furto

    df_filtrado = filtrar_dados_furto(df_furto, datas, municipios, ais)
    
    if df_filtrado.empty:
        st.warning("Nenhum registo encontrado com os filtros selecionados.")
        return df_filtrado

    st.divider()
    kpi1, kpi2, kpi3 = st.columns(3)
    
    total_casos = df_filtrado.shape[0]
    kpi1.metric(label="Volume Total de Furtos", value=f"{total_casos:,}".replace(',', '.'))
    
    if total_casos > 0:
        cidade_pior = df_filtrado['Município'].mode()[0]
        kpi2.metric(label="Ponto Crítico (Município)", value=cidade_pior)
        
        dia_pior = df_filtrado['Dia da Semana'].mode()[0]
        kpi3.metric(label="Dia de Maior Risco", value=dia_pior)
    
    st.divider()
    chart_mapa.render(df_filtrado)
    st.divider()
    
    st.markdown("### Dinâmica Operacional e Inteligência")
    
    aba1, aba2, aba3, aba4 = st.tabs([
        "Matriz de Risco (Tempo)",
        "Evolução e Demanda",
        "Séries e Algoritmos",
        "Inteligência de Patrulhamento"
    ])
    
    with aba1:
        chart_matriz.render(df_filtrado)
    with aba2:
        chart_evolucao.render(df_filtrado)
    with aba3:
        chart_avancado.render(df_filtrado)
    with aba4:
        chart_patrulha.render(df_filtrado)
    
    return df_filtrado
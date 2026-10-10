import streamlit as st
from services.data_handler import filtrar_dados_salvamento

# Importando os componentes isolados
import components.salvamento.chart_mapa as chart_mapa_salvamento
import components.salvamento.chart_visao_geral as chart_visao_geral
import components.salvamento.chart_matriz_risco as chart_matriz_risco
import components.salvamento.chart_treemap as chart_treemap
import components.salvamento.chart_fim_semana as chart_fim_semana
import components.salvamento.chart_engenharia_operacional as chart_engenharia # <-- NOVO COMPONENTE

def render(df_salvamento, datas, municipios, ais):
    st.subheader(":material/medical_services: Operações de Salvamento e Defesa Civil")
    
    with st.popover(":material/help: Metodologia e Leitura do Módulo"):
        st.markdown("""
        **Diretrizes de Leitura (Salvamento):**
        Este módulo reflete a carga operacional do Corpo de Bombeiros e Defesa Civil.
        
        **Métricas Principais:**
        * Como a base é unitária, cada linha no banco de dados contabiliza **exatamente 1 (uma) ocorrência de resgate/salvamento**.
        * **Volume Absoluto:** Mostra as cidades com maior demanda bruta por viaturas e efetivo.
        * **Densidade (Taxa):** Mostra as cidades que, proporcionalmente ao seu tamanho, exigem um esforço atípico de resgate.
        """)
        
    if df_salvamento.empty:
        st.warning(":material/warning: Base de dados de Salvamento não encontrada ou vazia.")
        return df_salvamento
        
    # Processamento e Filtro
    df_filtrado = filtrar_dados_salvamento(df_salvamento, datas, municipios, ais)
    
    if df_filtrado.empty:
        st.warning(":material/search_off: Nenhum registro encontrado com estes filtros.")
        return df_filtrado

    # KPIs Focados em Salvamento
    kpi1, kpi2 = st.columns(2)
    total_ocorrencias = df_filtrado.shape[0]
    
    kpi1.metric(label=":material/support_agent: Total de Chamados Atendidos", value=f"{total_ocorrencias:,}".replace(',', '.'))
    
    # Média diária de atendimentos no período selecionado
    dias_no_periodo = (df_filtrado['Data'].max() - df_filtrado['Data'].min()).days
    dias_no_periodo = dias_no_periodo if dias_no_periodo > 0 else 1
    media_diaria = total_ocorrencias / dias_no_periodo
    
    kpi2.metric(label=":material/speed: Média de Ocorrências por Dia", value=f"{media_diaria:,.1f}".replace('.', ','))
    
    st.divider()
    
    # 1. Renderiza o Mapa Tático
    chart_mapa_salvamento.render(df_filtrado)
    
    st.divider()
    
    # 2. Renderiza as Abas e chama os gráficos isolados
    st.markdown("### :material/monitoring: Dinâmica de Demanda Operacional")
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        ":material/dashboard: Visão Geral", 
        ":material/calendar_clock: Matriz de Calor",
        ":material/account_tree: Árvore Hierárquica",
        ":material/event: Fator Fim de Semana",
        ":material/engineering: Engenharia Operacional" # <-- NOVA ABA AQUI
    ])
    
    with aba1:
        chart_visao_geral.render(df_filtrado)
        
    with aba2:
        chart_matriz_risco.render(df_filtrado)
        
    with aba3:
        chart_treemap.render(df_filtrado)
        
    with aba4:
        chart_fim_semana.render(df_filtrado)
        
    with aba5:
        chart_engenharia.render(df_filtrado) 
    return df_filtrado
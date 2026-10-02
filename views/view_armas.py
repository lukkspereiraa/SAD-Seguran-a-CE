import streamlit as st
from services.data_handler import filtrar_dados_armas

# Importando os componentes isolados
import components.armas.chart_mapa as chart_mapa_armas
import components.armas.chart_visao_geral as chart_visao_geral
import components.armas.chart_matriz_risco as chart_matriz_risco

def render(df_armas, datas, municipios, ais):
    st.subheader(":material/crisis_alert: Desarmamento e Apreensão de Armas de Fogo")
    
    with st.popover(":material/help: Metodologia e Leitura do Módulo"):
        st.markdown("""
        **Diretrizes de Leitura (Armas de Fogo):**
        Este módulo foca na descapitalização bélica do crime organizado.
        
        **Métricas Principais:**
        * **Total de Ocorrências:** Frequência de ações policiais que resultaram em apreensão.
        * **Volume Total (Armas Apreendidas):** A soma real do poder de fogo retirado das ruas (Quantidade).
        """)
        
    if df_armas.empty:
        st.warning(":material/warning: Base de dados de Armas não encontrada ou vazia.")
        return df_armas
        
    # Processamento e Filtro
    df_armas_filtrado = filtrar_dados_armas(df_armas, datas, municipios, ais)
    
    if df_armas_filtrado.empty:
        st.warning(":material/search_off: Nenhum registro encontrado com estes filtros.")
        return df_armas_filtrado

    # KPIs Focados em Desarmamento
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label=":material/receipt_long: Total de Ocorrências Policiais", value=f"{df_armas_filtrado.shape[0]:,}".replace(',', '.'))
    
    total_armas = int(df_armas_filtrado['Quantidade'].sum())
    kpi2.metric(label=":material/hardware: Total de Armas Apreendidas", value=f"{total_armas:,}".replace(',', '.'))
    
    st.divider()
    
    # 1. Renderiza o Mapa Tático
    chart_mapa_armas.render(df_armas_filtrado)
    
    st.divider()
    
    # 2. Renderiza as Abas e chama os gráficos isolados
    st.markdown("### :material/monitoring: Dinâmica de Desarmamento Territorial")
    
    aba1, aba2 = st.tabs([
        ":material/dashboard: Visão Geral", 
        ":material/calendar_clock: Matriz de Risco Temporal"
    ])
    
    with aba1:
        chart_visao_geral.render(df_armas_filtrado)
        
    with aba2:
        chart_matriz_risco.render(df_armas_filtrado)
    
    return df_armas_filtrado
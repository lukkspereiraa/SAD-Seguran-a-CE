import streamlit as st
from services.data_handler import filtrar_dados_maria_penha

# Importando os componentes isolados
import components.maria_penha.chart_mapa as chart_mapa_mp
import components.maria_penha.chart_perfil_vitima as chart_perfil
import components.maria_penha.chart_matriz_risco as chart_matriz
import components.maria_penha.chart_evolucao as chart_evolucao
import components.maria_penha.chart_inteligencia as chart_inteligencia
import components.maria_penha.chart_auditoria_dados as chart_auditoria # <-- NOVO COMPONENTE

def render(df_mp, datas, municipios, ais):
    st.subheader(":material/family_restroom: Violência Doméstica (Lei Maria da Penha)")
    
    with st.popover(":material/help: Metodologia e Leitura do Módulo"):
        st.markdown("""
        **Diretrizes de Leitura:**
        Este módulo analisa a incidência de crimes contra a mulher no contexto doméstico e familiar.
        
        **Foco Tático:**
        * **Perfil de Vulnerabilidade:** Permite cruzar Raça, Idade e Escolaridade para entender qual grupo feminino está mais exposto.
        * **Temporalidade:** Identifica os dias críticos (geralmente finais de semana) para direcionar as viaturas da Patrulha Maria da Penha.
        """)
        
    if df_mp.empty:
        st.warning(":material/warning: Base de dados não encontrada ou vazia.")
        return df_mp

    # Filtros Sociodemográficos Específicos
    st.markdown("#### :material/tune: Filtros de Perfil da Vítima")
    col1, col2, col3 = st.columns(3)
    with col1:
        faixas = st.multiselect("Faixa Etária:", sorted(df_mp['Faixa Etária'].dropna().astype(str).unique()))
    with col2:
        racas = st.multiselect("Raça/Cor:", sorted(df_mp['Raça da Vítima'].dropna().unique()))
    with col3:
        escolaridades = st.multiselect("Escolaridade:", sorted(df_mp['Escolaridade da Vítima'].dropna().unique()))
        
    # Processamento e Filtro
    df_filtrado = filtrar_dados_maria_penha(df_mp, datas, municipios, ais, faixas, racas, escolaridades)
    
    if df_filtrado.empty:
        st.warning(":material/search_off: Nenhum registro encontrado com estes filtros.")
        return df_filtrado

    # KPIs Principais
    st.divider()
    kpi1, kpi2 = st.columns(2)
    
    total_casos = df_filtrado.shape[0]
    kpi1.metric(label=":material/report: Total de Ocorrências Registradas", value=f"{total_casos:,}".replace(',', '.'))
    
    dias_no_periodo = (df_filtrado['Data'].max() - df_filtrado['Data'].min()).days
    dias_no_periodo = dias_no_periodo if dias_no_periodo > 0 else 1
    media_diaria = total_casos / dias_no_periodo
    kpi2.metric(label=":material/calendar_today: Média de Casos por Dia", value=f"{media_diaria:,.1f}".replace('.', ','))
    
    st.divider()
    
    # 1. Renderiza o Mapa Tático
    chart_mapa_mp.render(df_filtrado)
    
    st.divider()
    
    # 2. Renderiza as Abas e chama os gráficos isolados
    st.markdown("### :material/monitoring: Dinâmica da Violência Doméstica")
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        ":material/group: Perfil da Vítima", 
        ":material/calendar_clock: Matriz de Risco",
        ":material/trending_up: Evolução e Território",
        ":material/psychology: Inteligência Socioterritorial",
        ":material/policy: Auditoria de Dados (Governança)" # <-- NOVA ABA AQUI
    ])
    
    with aba1:
        chart_perfil.render(df_filtrado)
        
    with aba2:
        chart_matriz.render(df_filtrado)
        
    with aba3:
        chart_evolucao.render(df_filtrado)
        
    with aba4:
        chart_inteligencia.render(df_filtrado)
        
    with aba5:
        chart_auditoria.render(df_filtrado) # <-- RENDERIZAÇÃO
    
    return df_filtrado
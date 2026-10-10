import streamlit as st
from services.data_handler import filtrar_dados_lgbt

# Importação dos componentes isolados
import components.lgbtfobia.chart_perfil as chart_perfil
import components.lgbtfobia.chart_locais_risco as chart_locais
import components.lgbtfobia.chart_mapa as chart_mapa
import components.lgbtfobia.chart_auditoria as chart_auditoria
import components.lgbtfobia.chart_matriz_risco as chart_matriz # <-- NOVO
import components.lgbtfobia.chart_evolucao as chart_evolucao # <-- NOVO

def render(df_lgbt, datas, municipios, ais):
    st.subheader(":material/diversity_3: Crimes de Intolerância e Ódio (LGBTfobia)")
    
    with st.popover(":material/help: Metodologia e Leitura do Módulo"):
        st.markdown("""
        **Diretrizes de Leitura:**
        Módulo focado na análise de crimes motivados por preconceito de orientação sexual ou identidade de género.
        
        **Foco Tático:**
        * **Subnotificação:** O volume absoluto baixo em relação à população sugere que muitas vítimas não reportam o crime. O foco recai sobre o *padrão* de quem reporta.
        * **Mapeamento de Locais:** Identificar se o risco é maior na via pública, estabelecimentos comerciais ou no ambiente doméstico.
        """)
        
    if df_lgbt.empty:
        st.warning(":material/warning: Base de dados não encontrada ou vazia.")
        return df_lgbt

    # Filtros Específicos para LGBTfobia
    st.markdown("#### :material/tune: Filtros de Perfil e Natureza")
    col1, col2, col3 = st.columns(3)
    with col1:
        naturezas = st.multiselect("Tipificação Penal:", sorted(df_lgbt['Natureza'].dropna().unique()))
    with col2:
        identidades = st.multiselect("Identidade de Género:", sorted(df_lgbt['Identidade de Gênero'].dropna().unique()))
    with col3:
        orientacoes = st.multiselect("Orientação Sexual:", sorted(df_lgbt['Orientação Sexual'].dropna().unique()))
        
    # Processamento e Filtro
    df_filtrado = filtrar_dados_lgbt(df_lgbt, datas, municipios, ais, naturezas, identidades, orientacoes)
    
    if df_filtrado.empty:
        st.warning(":material/search_off: Nenhum registo encontrado com estes filtros.")
        return df_filtrado

    # KPIs Principais
    st.divider()
    kpi1, kpi2 = st.columns(2)
    
    total_casos = df_filtrado.shape[0]
    kpi1.metric(label=":material/report: Ocorrências Registadas", value=f"{total_casos:,}".replace(',', '.'))
    
    if total_casos > 0:
        crime_top = df_filtrado['Natureza'].value_counts().index[0]
        tipo_predominante = "Homofobia" if "HOMO" in str(crime_top) else "Transfobia"
        kpi2.metric(label=":material/gavel: Tipificação Predominante", value=tipo_predominante)
    
    st.divider()
    
    # 1. Renderiza o Mapa Tático (AGORA COM TAXA POR 100K HABITANTES!)
    chart_mapa.render(df_filtrado)
    
    st.divider()
    
    # 2. Renderiza as Abas e chama os gráficos isolados
    st.markdown("### :material/monitoring: Dinâmica da Intolerância")
    
    # Adicionámos mais abas para comportar a matriz temporal e evolução
    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        ":material/group: Perfil da Vítima", 
        ":material/location_on: Locais e Tipificação",
        ":material/calendar_clock: Matriz de Risco",
        ":material/trending_up: Evolução Mensal",
        ":material/policy: Auditoria de Dados" 
    ])
    
    with aba1:
        chart_perfil.render(df_filtrado)
        
    with aba2:
        chart_locais.render(df_filtrado)
        
    with aba3:
        chart_matriz.render(df_filtrado)
        
    with aba4:
        chart_evolucao.render(df_filtrado)
        
    with aba5:
        chart_auditoria.render(df_filtrado)
    
    return df_filtrado
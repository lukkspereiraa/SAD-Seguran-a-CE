import streamlit as st
from services.data_handler import filtrar_dados_entorpecentes

# Importando os componentes isolados da subpasta entorpecentes
import components.entorpecentes.chart_mapa as chart_mapa_ent
import components.entorpecentes.chart_visao_geral as chart_visao_geral
import components.entorpecentes.chart_matriz_risco as chart_matriz_risco
import components.entorpecentes.chart_perfil_trafico as chart_perfil_trafico
import components.entorpecentes.chart_raio_x_ais as chart_raio_x_ais
import components.entorpecentes.chart_treemap as chart_treemap # <-- IMPORTANDO O TREEMAP

def render(df_ent, datas, municipios, ais):
    st.subheader(":material/local_police: Combate ao Tráfico de Drogas")
    
    with st.popover(":material/help: Metodologia e Leitura do Módulo"):
        st.markdown("""
        **Diretrizes de Leitura (Entorpecentes):**
        Este módulo é focado exclusivamente na logística financeira e no volume físico do narcotráfico. 
        Ao contrário dos crimes contra a vida (CVLI) que contam 'vítimas', aqui a principal grandeza de impacto é o **Peso (Kg)**.
        
        **Regras de Negócio e Filtros:**
        * **Filtro de Substância:** Você pode isolar a análise para tipos específicos (ex: ver a dinâmica apenas da Cocaína e do Crack).
        * **Total de Ocorrências:** Conta quantas vezes a polícia efetuou uma apreensão (Frequência do trabalho policial).
        * **Volume Total Apreendido:** Soma exata dos Quilos (Kg) retirados de circulação, que representa o verdadeiro prejuízo às facções.
        """)
        
    if df_ent.empty:
        st.warning(":material/warning: Base de dados de entorpecentes não encontrada ou vazia.")
        return df_ent
        
    # Filtro Específico para Entorpecentes
    col1, col2 = st.columns([1, 3])
    with col1:
        tipos_droga = st.multiselect(
            ":material/medication: Tipo de Entorpecente:", 
            sorted(df_ent['Tipo de Entorpecente'].dropna().unique())
        )
        
    # Processamento
    df_ent_filtrado = filtrar_dados_entorpecentes(df_ent, datas, municipios, ais, tipos_droga)
    
    if df_ent_filtrado.empty:
        st.warning(":material/search_off: Nenhum registro encontrado com estes filtros.")
        return df_ent_filtrado

    # KPIs Focados em Drogas
    kpi1, kpi2 = st.columns(2)
    kpi1.metric(label=":material/receipt_long: Total de Ocorrências", value=f"{df_ent_filtrado.shape[0]:,}".replace(',', '.'))
    
    total_kg = df_ent_filtrado['Quantidade (Kg)'].sum()
    kpi2.metric(label=":material/scale: Volume Total Apreendido (Kg)", value=f"{total_kg:,.2f}".replace('.', ','))
    
    st.divider()
    
    # 1. Renderiza o Mapa Multi-Camadas
    chart_mapa_ent.render(df_ent_filtrado)
    
    st.divider()
    
    # 2. Renderiza as Abas e chama os gráficos isolados
    st.markdown("### :material/monitoring: Dinâmica e Inteligência de Apreensões")
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        ":material/dashboard: Visão Geral", 
        ":material/calendar_clock: Matriz de Risco", 
        ":material/category: Perfil do Tráfico",
        ":material/share_location: Raio-X por AIS",
        ":material/account_tree: Árvore Hierárquica" # <-- NOVA ABA
    ])
    
    with aba1:
        chart_visao_geral.render(df_ent_filtrado)
        
    with aba2:
        chart_matriz_risco.render(df_ent_filtrado)
        
    with aba3:
        chart_perfil_trafico.render(df_ent_filtrado)
        
    with aba4:
        chart_raio_x_ais.render(df_ent_filtrado)
        
    with aba5:
        chart_treemap.render(df_ent_filtrado) # <-- RENDERIZANDO A ÁRVORE
    
    return df_ent_filtrado
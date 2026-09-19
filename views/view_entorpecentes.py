import streamlit as st
from services.data_handler import filtrar_dados_entorpecentes

# Importando os componentes da subpasta entorpecentes
import components.entorpecentes.chart_entorpecentes as chart_entorpecentes
import components.entorpecentes.chart_mapa as chart_mapa_ent

def render(df_ent, datas, municipios, ais):
    st.subheader(":material/local_police: Combate ao Tráfico de Drogas")
    
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
    
    # 2. Renderiza os Gráficos Analíticos (Rosca, Barras e Linha do Tempo)
    chart_entorpecentes.render(df_ent_filtrado)
    
    return df_ent_filtrado
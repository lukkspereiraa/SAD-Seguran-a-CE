import streamlit as st
import plotly.express as px
import pandas as pd
# Importação centralizada a partir do nosso novo serviço
from services.ibge import carregar_populacao_ibge_ceara, carregar_geojson, normalizar_texto

def render(df_filtrado):
    st.subheader("Mapa Criminal (Visão Municipal)")
    
    with st.popover("Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        O mapa exibe as subdivisões dos 184 municípios cearenses. Áreas mais claras indicam baixa incidência (ou zero ocorrências), enquanto tons escuros alertam para focos de violência letal.
        
        **Regras de Negócio e Tratamento:**
        * **Engenharia de Dados (Preenchimento de Vazios):** Municípios sem registros criminais no período filtrado são automaticamente injetados no painel com valor "0". Isso preserva a integridade geométrica do mapa e evita "buracos" visuais na renderização.
        * **Engenharia de Dados (Microsserviços):** A taxa populacional é consumida em tempo real via API do Censo 2022 do IBGE.
        """)
        
    if df_filtrado.empty: return

    # 1. Agrupa os crimes que aconteceram
    df_crimes = df_filtrado.groupby('Município').size().reset_index(name='Total Absoluto')
    df_crimes['Município_Tratado'] = df_crimes['Município'].apply(normalizar_texto)
    
    # 2. Carrega o mapa e a lista oficial de todas as cidades usando o Serviço Central
    geojson_ce, lista_cidades = carregar_geojson()
    populacao_ibge = carregar_populacao_ibge_ceara()
    
    # 3. Cria um DataFrame base com as 184 cidades e junta com os crimes
    df_base = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_base, df_crimes[['Município_Tratado', 'Total Absoluto']], on='Município_Tratado', how='left')
    
    # Preenche com 0 os municípios que não tiveram crimes
    df_mapa['Total Absoluto'] = df_mapa['Total Absoluto'].fillna(0)
    
    # Injeta a população oficial do IBGE e calcula a taxa
    df_mapa['População (IBGE)'] = df_mapa['Município_Tratado'].map(populacao_ibge).fillna(35000)
    df_mapa['Taxa (por 100k hab.)'] = round((df_mapa['Total Absoluto'] / df_mapa['População (IBGE)']) * 100000, 2)
    
    # Toggle (Radio Button) para escolher qual dado exibir
    metrica_mapa = st.radio(
        "Métrica de Análise Geográfica:", 
        options=["Total Absoluto", "Taxa (por 100k hab.)"], 
        horizontal=True
    )
    
    # Geração do mapa
    fig_mapa = px.choropleth(
        df_mapa, 
        geojson=geojson_ce, 
        locations='Município_Tratado', 
        featureidkey="properties.name", 
        color=metrica_mapa,
        color_continuous_scale="Reds" if metrica_mapa == "Total Absoluto" else "Inferno",
        hover_name='Município_Tratado',
        hover_data={'Município_Tratado': False, 'Total Absoluto': True, 'Taxa (por 100k hab.)': True, 'População (IBGE)': True},
        labels={metrica_mapa: 'Índice'}
    )
    
    # O segredo para não mostrar o globo terrestre:
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=650)
    
    st.plotly_chart(fig_mapa, use_container_width=True)
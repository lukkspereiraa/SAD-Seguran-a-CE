import streamlit as st
import plotly.express as px
import pandas as pd
# Importação centralizada a partir do nosso novo serviço
from services.ibge import carregar_populacao_ibge_ceara, carregar_geojson, normalizar_texto

def render(df_filtrado):
    st.subheader("Mapa Tático (Mancha de Intolerância)")
    
    with st.popover("Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        O mapa exibe as subdivisões dos 184 municípios cearenses focado nos casos de LGBTfobia. 
        É possível alternar a visualização para focar no número absoluto de casos ou na taxa por 100 mil habitantes.
        
        **Regras de Negócio e Tratamento:**
        * **Engenharia de Dados (Preenchimento de Vazios):** Municípios sem registros de casos no período filtrado recebem automaticamente o valor "0" (zero).
        * **Engenharia de Dados (Microsserviços):** A taxa populacional é consumida em tempo real via API do Censo 2022 do IBGE.
        """)

    if df_filtrado.empty: return

    # Conta o volume de casos
    df_agrupado = df_filtrado.groupby('Município').size().reset_index(name='Total de Casos')
    df_agrupado['Município_Tratado'] = df_agrupado['Município'].apply(normalizar_texto)
    
    # Carrega o mapa e a lista oficial de todas as cidades usando o Serviço Central
    geojson_ce, lista_cidades = carregar_geojson()
    populacao_ibge = carregar_populacao_ibge_ceara()
    
    # Cria um DataFrame base com as 184 cidades e junta com as ocorrencias
    df_base = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_base, df_agrupado[['Município_Tratado', 'Total de Casos']], on='Município_Tratado', how='left')
    
    # Cálculo da Taxa Demográfica e Preenchimento de Vazios
    df_mapa['Total de Casos'] = df_mapa['Total de Casos'].fillna(0)
    df_mapa['População (IBGE)'] = df_mapa['Município_Tratado'].map(populacao_ibge).fillna(35000)
    df_mapa['Taxa (Casos por 100k hab.)'] = round((df_mapa['Total de Casos'] / df_mapa['População (IBGE)']) * 100000, 2)
    
    # Toggle de Métrica
    metrica_mapa = st.radio(
        "Métrica de Análise Geográfica:", 
        options=["Total de Casos", "Taxa (Casos por 100k hab.)"], 
        horizontal=True
    )
    
    # Como a LGBTfobia usa a paleta Rainbow, mantemos para Absoluto, mas usamos Sunset para a Taxa para contrastar
    cor_escala = "Rainbow" if metrica_mapa == "Total de Casos" else "Sunset"

    fig_mapa = px.choropleth(
        df_mapa, 
        geojson=geojson_ce, 
        locations='Município_Tratado', 
        featureidkey="properties.name", 
        color=metrica_mapa,
        color_continuous_scale=cor_escala,
        hover_name='Município_Tratado',
        hover_data={'Município_Tratado': False, 'Total de Casos': True, 'Taxa (Casos por 100k hab.)': True, 'População (IBGE)': True},
        labels={metrica_mapa: 'Índice'}
    )
    
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=650)
    
    st.plotly_chart(fig_mapa, use_container_width=True)
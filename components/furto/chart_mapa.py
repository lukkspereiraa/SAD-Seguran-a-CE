import streamlit as st
import plotly.express as px
import pandas as pd
# Importação centralizada a partir do nosso novo serviço
from services.ibge import carregar_populacao_ibge_ceara, carregar_geojson, normalizar_texto

def render(df_filtrado):
    st.subheader("Mapa de Ocorrências (Taxa Oficial via API IBGE)")
    st.info("Engenharia de Dados: Este mapa consome a API REST do IBGE em tempo real, calculando a taxa proporcional ao tamanho da cidade com base no Censo 2022.")
    
    if df_filtrado.empty:
        return

    # 1. Contagem de Ocorrências
    df_agrupado = df_filtrado.groupby('Município').size().reset_index(name='Total')
    df_agrupado['Município_Tratado'] = df_agrupado['Município'].apply(normalizar_texto)
    
    # 2. Carregar Inteligência Geográfica e Populacional
    geojson_ce, lista_cidades = carregar_geojson()
    populacao_ibge = carregar_populacao_ibge_ceara()
    
    # 3. Mesclar Dados
    df_mapa = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_mapa, df_agrupado[['Município_Tratado', 'Total']], on='Município_Tratado', how='left').fillna(0)
    
    # 4. Cálculo Criminológico Correto
    df_mapa['População (IBGE)'] = df_mapa['Município_Tratado'].map(populacao_ibge).fillna(35000)
    df_mapa['Taxa (por 100k hab.)'] = round((df_mapa['Total'] / df_mapa['População (IBGE)']) * 100000, 2)
    
    metrica = st.radio(
        "Selecione a Métrica do Mapa:", 
        ["Volume Absoluto de Ocorrências", "Taxa de Ocorrências (por 100k hab.)"], 
        horizontal=True
    )
    coluna_metrica = 'Total' if "Volume" in metrica else 'Taxa (por 100k hab.)'
    
    # 5. Plotar Gráfico (Mude o color_continuous_scale dependendo do crime: 'Reds', 'Blues', 'Oranges')
    fig_mapa = px.choropleth(
        df_mapa, 
        geojson=geojson_ce, 
        locations='Município_Tratado', 
        featureidkey="properties.name", 
        color=coluna_metrica, 
        color_continuous_scale='Reds', 
        hover_name='Município_Tratado',
        hover_data={'Município_Tratado': False, 'Total': True, 'Taxa (por 100k hab.)': True, 'População (IBGE)': True}
    )
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=600)
     
    st.plotly_chart(fig_mapa, use_container_width=True)
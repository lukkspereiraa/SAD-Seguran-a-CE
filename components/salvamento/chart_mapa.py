import streamlit as st
import plotly.express as px
import urllib.request
import json
import pandas as pd
import unicodedata

POPULACAO_CE = {
    'FORTALEZA': 2428678, 'CAUCAIA': 355679, 'JUAZEIRO DO NORTE': 286120, 'MARACANAU': 234392, 
    'SOBRAL': 203682, 'CRATO': 131050, 'ITAPIPOCA': 131123, 'MARANGUAPE': 105093, 
    'IGUATU': 98064, 'QUIXADA': 88000, 'PACATUBA': 85000, 'AQUIRAZ': 80000, 
    'QUIXERAMOBIM': 80000, 'CANINDE': 75000, 'RUSSAS': 75000, 'CRATEUS': 75000, 
    'TIANGUA': 75000, 'ARACATI': 75000, 'CASCAVEL': 72000, 'PACAJUS': 70000, 
    'HORIZONTE': 68000, 'GUARACIABA DO NORTE': 40000
}

def normalizar_texto(texto):
    if pd.isna(texto): return ""
    texto_sem_acento = ''.join(c for c in unicodedata.normalize('NFD', str(texto)) if unicodedata.category(c) != 'Mn')
    return texto_sem_acento.upper().strip()

@st.cache_data
def carregar_geojson_municipios_ceara():
    url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-23-mun.json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        geojson = json.load(response)
    lista_todas_cidades = []
    for feature in geojson['features']:
        if 'name' in feature['properties']:
            nome_limpo = normalizar_texto(feature['properties']['name'])
            feature['properties']['name'] = nome_limpo
            lista_todas_cidades.append(nome_limpo)
    return geojson, lista_todas_cidades

def render(df_filtrado):
    st.subheader(":material/public: Mapa de Demanda por Resgates")
    
    if df_filtrado.empty: return

    # Como não tem coluna de quantidade, contamos quantas vezes a cidade aparece
    df_agrupado = df_filtrado.groupby('Município').size().reset_index(name='Total de Chamados')
    df_agrupado['Município_Tratado'] = df_agrupado['Município'].apply(normalizar_texto)
    
    geojson_ce, lista_cidades = carregar_geojson_municipios_ceara()
    df_base = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_base, df_agrupado[['Município_Tratado', 'Total de Chamados']], on='Município_Tratado', how='left')
    
    df_mapa['Total de Chamados'] = df_mapa['Total de Chamados'].fillna(0)
    df_mapa['População Estimada'] = df_mapa['Município_Tratado'].map(POPULACAO_CE).fillna(35000)
    df_mapa['Taxa (Chamados por 100k hab.)'] = round((df_mapa['Total de Chamados'] / df_mapa['População Estimada']) * 100000, 2)
    
    metrica_mapa = st.radio(
        "Métrica de Análise Geográfica:", 
        options=["Total de Chamados", "Taxa (Chamados por 100k hab.)"], 
        horizontal=True
    )
    
    # Cores azuis representam bem operações de salvamento/saúde
    cor_escala = "Blues" if metrica_mapa == "Total de Chamados" else "Purples"

    fig_mapa = px.choropleth(
        df_mapa, 
        geojson=geojson_ce, 
        locations='Município_Tratado', 
        featureidkey="properties.name", 
        color=metrica_mapa,
        color_continuous_scale=cor_escala,
        hover_name='Município_Tratado',
        hover_data={'Município_Tratado': False, 'Total de Chamados': True, 'Taxa (Chamados por 100k hab.)': True},
        labels={metrica_mapa: 'Demanda'}
    )
    
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=650)
    
    st.plotly_chart(fig_mapa, use_container_width=True)
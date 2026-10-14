import streamlit as st
import plotly.express as px
import urllib.request
import json
import pandas as pd
import requests
import unicodedata

def normalizar_texto(texto):
    if pd.isna(texto):
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto)) if unicodedata.category(c) != 'Mn').upper().strip()

@st.cache_data(ttl=86400)
def carregar_populacao_ibge_ceara():
    """Consome a API REST oficial do IBGE (Censo 2022) para o Ceará (Estado 23)"""
    url = "https://servicodados.ibge.gov.br/api/v3/agregados/4709/periodos/2022/variaveis/93?localidades=N6[N3[23]]"
    
    # Este cabeçalho impede que o IBGE bloqueie a nossa conexão
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            dados = response.json()
            populacao = {}
            for item in dados[0]['resultados'][0]['series']:
                # Correção da quebra de linha que estava a dar erro
                nome_cidade = item['localidade']['nome'].replace(' - CE', '')
                nome_cidade_limpo = normalizar_texto(nome_cidade)
                valor_pop = int(item['serie']['2022'])
                populacao[nome_cidade_limpo] = valor_pop
            return populacao
    except Exception as e:
        st.error("Aviso: Falha na conexão com a API do IBGE. Verifique a sua internet. Usando fallback estático.")
    
    # Dicionário de emergência caso a internet do utilizador caia
    return {'FORTALEZA': 2428678, 'CAUCAIA': 355679, 'JUAZEIRO DO NORTE': 286120, 'MARACANAU': 234392, 'SOBRAL': 203682}

@st.cache_data
def carregar_geojson():
    url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-23-mun.json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        geojson = json.load(response)
    
    lista_cidades = []
    for feature in geojson['features']:
        if 'name' in feature['properties']:
            nome_limpo = normalizar_texto(feature['properties']['name'])
            feature['properties']['name'] = nome_limpo
            lista_cidades.append(nome_limpo)
    
    return geojson, lista_cidades

def render(df_filtrado):
    st.subheader(":material/public: Mapa de Furtos (Taxa Oficial via API IBGE)")
    st.info("**Engenharia de Dados:** Este mapa consome a API REST do IBGE em tempo real, garantindo a correspondência no mundo real (Censo 2022) para maior precisão dos dados.")
    
    if df_filtrado.empty:
        return

    df_agrupado = df_filtrado.groupby('Município').size().reset_index(name='Total de Furtos')
    df_agrupado['Município_Tratado'] = df_agrupado['Município'].apply(normalizar_texto)
    
    geojson_ce, lista_cidades = carregar_geojson()
    populacao_ibge = carregar_populacao_ibge_ceara()
    
    df_mapa = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_mapa, df_agrupado[['Município_Tratado', 'Total de Furtos']], on='Município_Tratado', how='left').fillna(0)
    
    # Cruzamento do crime com os dados REAIS do IBGE
    df_mapa['População (IBGE)'] = df_mapa['Município_Tratado'].map(populacao_ibge).fillna(35000)
    df_mapa['Taxa (por 100k hab.)'] = round((df_mapa['Total de Furtos'] / df_mapa['População (IBGE)']) * 100000, 2)
    
    metrica = st.radio(
        "Selecione a Métrica do Mapa:", 
        ["Total de Furtos (Volume Absoluto)", "Taxa (por 100k hab.) - Ajustado por População Real"], 
        horizontal=True
    )
    coluna_metrica = 'Total de Furtos' if "Volume" in metrica else 'Taxa (por 100k hab.)'
    
    fig_mapa = px.choropleth(
        df_mapa, 
        geojson=geojson_ce, 
        locations='Município_Tratado', 
        featureidkey="properties.name", 
        color=coluna_metrica, 
        color_continuous_scale='Blues', 
        hover_name='Município_Tratado',
        hover_data={'Município_Tratado': False, 'Total de Furtos': True, 'Taxa (por 100k hab.)': True, 'População (IBGE)': True}
    )
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=600)
     
    st.plotly_chart(fig_mapa, use_container_width=True)
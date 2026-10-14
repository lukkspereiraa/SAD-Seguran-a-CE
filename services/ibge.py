import pandas as pd
import requests
import urllib.request
import json
import unicodedata
import streamlit as st

def normalizar_texto(texto):
    """Remove acentos e padroniza o texto para maiúsculas."""
    if pd.isna(texto):
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', str(texto)) if unicodedata.category(c) != 'Mn').upper().strip()

@st.cache_data(ttl=86400)
def carregar_populacao_ibge_ceara():
    """Consome a API REST oficial do IBGE (Censo 2022) para o Ceará (Estado 23)"""
    url = "https://servicodados.ibge.gov.br/api/v3/agregados/4709/periodos/2022/variaveis/93?localidades=N6[N3[23]]"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            dados = response.json()
            populacao = {}
            for item in dados[0]['resultados'][0]['series']:
                nome_cidade = item['localidade']['nome'].replace(' - CE', '')
                nome_cidade_limpo = normalizar_texto(nome_cidade)
                valor_pop = int(item['serie']['2022'])
                populacao[nome_cidade_limpo] = valor_pop
            return populacao
    except Exception:
        st.error("Aviso: Falha na conexão com a API do IBGE. Usando fallback estático.")
    
    # Fallback de emergência
    return {'FORTALEZA': 2428678, 'CAUCAIA': 355679, 'JUAZEIRO DO NORTE': 286120, 'MARACANAU': 234392, 'SOBRAL': 203682}

@st.cache_data
def carregar_geojson():
    """Descarrega a malha geográfica do Ceará para plotar o mapa."""
    url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-23-mun.json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            geojson = json.load(response)
        
        lista_cidades = []
        for feature in geojson['features']:
            if 'name' in feature['properties']:
                nome_limpo = normalizar_texto(feature['properties']['name'])
                feature['properties']['name'] = nome_limpo
                lista_cidades.append(nome_limpo)
        
        return geojson, lista_cidades
    except Exception:
        st.error("Aviso: Falha ao carregar a malha geográfica.")
        return None, []
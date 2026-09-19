import streamlit as st
import plotly.express as px
import urllib.request
import json
import pandas as pd
import unicodedata

# Estimativa populacional (Amostra para cálculo da taxa)
POPULACAO_CE = {
    'FORTALEZA': 2428678, 'CAUCAIA': 355679, 'JUAZEIRO DO NORTE': 286120, 'MARACANAU': 234392, 
    'SOBRAL': 203682, 'CRATO': 131050, 'ITAPIPOCA': 131123, 'MARANGUAPE': 105093, 
    'IGUATU': 98064, 'QUIXADA': 88000, 'PACATUBA': 85000, 'AQUIRAZ': 80000, 
    'QUIXERAMOBIM': 80000, 'CANINDE': 75000, 'RUSSAS': 75000, 'CRATEUS': 75000, 
    'TIANGUA': 75000, 'ARACATI': 75000, 'CASCAVEL': 72000, 'PACAJUS': 70000, 
    'HORIZONTE': 68000, 'GUARACIABA DO NORTE': 40000
}

def normalizar_texto(texto):
    """Remove acentos, espaços extras e transforma em maiúsculas"""
    if pd.isna(texto):
        return ""
    texto_sem_acento = ''.join(c for c in unicodedata.normalize('NFD', str(texto)) if unicodedata.category(c) != 'Mn')
    return texto_sem_acento.upper().strip()

@st.cache_data
def carregar_geojson_municipios_ceara():
    """Baixa o GeoJSON e extrai a lista de TODAS as cidades do Ceará."""
    url = 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-23-mun.json'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        geojson = json.load(response)
        
    lista_todas_cidades = []
    # Padroniza os nomes dentro do mapa para facilitar o cruzamento
    for feature in geojson['features']:
        if 'name' in feature['properties']:
            nome_limpo = normalizar_texto(feature['properties']['name'])
            feature['properties']['name'] = nome_limpo
            lista_todas_cidades.append(nome_limpo)
            
    return geojson, lista_todas_cidades

def render(df_filtrado):
    st.subheader(":material/public: Mapa Criminal (Visão Municipal)")
    
    with st.popover(":material/help: Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        O mapa exibe as subdivisões dos 184 municípios cearenses. Áreas mais claras indicam baixa incidência (ou zero ocorrências), enquanto tons escuros alertam para focos de violência letal.
        
        **Regras de Negócio e Tratamento:**
        * **Engenharia de Dados (Preenchimento de Vazios):** Municípios sem registros criminais no período filtrado são automaticamente injetados no painel com valor "0". Isso preserva a integridade geométrica do mapa e evita "buracos" visuais na renderização.
        """)
        
    # 1. Agrupa os crimes que aconteceram
    df_crimes = df_filtrado.groupby('Município').size().reset_index(name='Total Absoluto')
    df_crimes['Município_Tratado'] = df_crimes['Município'].apply(normalizar_texto)
    
    # 2. Carrega o mapa e a lista oficial de todas as cidades (para cobrir os buracos)
    geojson_ce, lista_cidades = carregar_geojson_municipios_ceara()
    
    # 3. Cria um DataFrame base com as 184 cidades e junta com os crimes
    df_base = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_base, df_crimes[['Município_Tratado', 'Total Absoluto']], on='Município_Tratado', how='left')
    
    # Preenche com 0 os municípios que não tiveram crimes
    df_mapa['Total Absoluto'] = df_mapa['Total Absoluto'].fillna(0)
    
    # Injeta a população e calcula a taxa
    df_mapa['População Estimada'] = df_mapa['Município_Tratado'].map(POPULACAO_CE).fillna(35000)
    df_mapa['Taxa (por 100k hab.)'] = round((df_mapa['Total Absoluto'] / df_mapa['População Estimada']) * 100000, 2)
    
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
        hover_data={'Município_Tratado': False, 'Total Absoluto': True, 'Taxa (por 100k hab.)': True, 'População Estimada': True},
        labels={metrica_mapa: 'Índice'}
    )
    
    # O segredo para não mostrar o globo terrestre:
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=650)
    
    st.plotly_chart(fig_mapa, use_container_width=True)
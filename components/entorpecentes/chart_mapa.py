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
    for feature in geojson['features']:
        if 'name' in feature['properties']:
            nome_limpo = normalizar_texto(feature['properties']['name'])
            feature['properties']['name'] = nome_limpo
            lista_todas_cidades.append(nome_limpo)
            
    return geojson, lista_todas_cidades

def render(df_filtrado):
    st.subheader(":material/public: Mapa Tático de Apreensões")
    
    with st.popover(":material/help: Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        O mapa exibe as subdivisões dos 184 municípios cearenses. É possível alternar a visualização para focar no volume apreendido (Peso em Kg), no número absoluto de ocorrências policiais, ou na taxa por 100 mil habitantes.
        
        **Regras de Negócio e Tratamento:**
        * **Engenharia de Dados (Preenchimento de Vazios):** Municípios sem registros de apreensão de drogas no período filtrado recebem automaticamente o valor "0" (zero).
        """)
        
    if df_filtrado.empty:
        st.warning("Nenhum dado para exibir no mapa.")
        return

    # 1. Agrupa os dados de entorpecentes (Ocorrências e Volume em Kg)
    df_agrupado = df_filtrado.groupby('Município').agg(
        Total_Ocorrencias=('Município', 'count'),
        Volume_Kg=('Quantidade (Kg)', 'sum')
    ).reset_index()
    
    df_agrupado['Município_Tratado'] = df_agrupado['Município'].apply(normalizar_texto)
    
    # 2. Carrega o mapa e a lista oficial de todas as cidades (para cobrir os buracos)
    geojson_ce, lista_cidades = carregar_geojson_municipios_ceara()
    
    # 3. Cria um DataFrame base com as 184 cidades e junta com os crimes
    df_base = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_base, df_agrupado[['Município_Tratado', 'Total_Ocorrencias', 'Volume_Kg']], on='Município_Tratado', how='left')
    
    # Preenche com 0 os municípios que não tiveram apreensões
    df_mapa['Total_Ocorrencias'] = df_mapa['Total_Ocorrencias'].fillna(0)
    df_mapa['Volume_Kg'] = df_mapa['Volume_Kg'].fillna(0)
    
    # Injeta a população e calcula a taxa de ocorrências por habitante
    df_mapa['População Estimada'] = df_mapa['Município_Tratado'].map(POPULACAO_CE).fillna(35000)
    df_mapa['Taxa (por 100k hab.)'] = round((df_mapa['Total_Ocorrencias'] / df_mapa['População Estimada']) * 100000, 2)
    
    # Renomeando as colunas para o mapa ficar bonito
    df_mapa = df_mapa.rename(columns={'Total_Ocorrencias': 'Total de Ocorrências', 'Volume_Kg': 'Volume (Kg)'})

    # Toggle (Radio Button) para escolher qual dado exibir
    metrica_mapa = st.radio(
        "Métrica de Análise Geográfica:", 
        options=["Total de Ocorrências", "Volume (Kg)", "Taxa (por 100k hab.)"], 
        horizontal=True
    )
    
    # Ajusta as escalas de cor para diferenciar do CVLI
    if metrica_mapa == "Total de Ocorrências":
        cor_escala = "Blues"
    elif metrica_mapa == "Volume (Kg)":
        cor_escala = "Greens"  # Verde para Entorpecentes!
    else:
        cor_escala = "Inferno"

    # Geração do mapa
    fig_mapa = px.choropleth(
        df_mapa, 
        geojson=geojson_ce, 
        locations='Município_Tratado', 
        featureidkey="properties.name", 
        color=metrica_mapa,
        color_continuous_scale=cor_escala,
        hover_name='Município_Tratado',
        hover_data={
            'Município_Tratado': False, 
            'Total de Ocorrências': True, 
            'Volume (Kg)': ':.2f', # Garante que o peso saia com 2 casas decimais
            'Taxa (por 100k hab.)': True, 
            'População Estimada': True
        },
        labels={metrica_mapa: 'Índice'}
    )
    
    # O segredo para não mostrar o globo terrestre:
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=650)
    
    st.plotly_chart(fig_mapa, use_container_width=True)
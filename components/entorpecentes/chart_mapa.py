import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

def render(df):
    if df.empty:
        return
        
    st.markdown("### :material/map: Mapeamento Tático de Apreensões")
    
    # 1. Agrupamento de Dados por Município
    df_mapa = df.groupby('Município').agg(
        Ocorrencias=('Município', 'count'),
        Volume_Kg=('Quantidade (Kg)', 'sum')
    ).reset_index()

    # 2. Mock/Exemplo de População (Substitua pela sua base real de população do IBGE que usa no CVLI)
    # Se você tiver um arquivo excel com a população, carregue-o e faça um pd.merge()
    populacao_ficticia = {mun: 50000 for mun in df_mapa['Município']} # População padrão de 50k para não quebrar o cálculo
    populacao_ficticia['Fortaleza'] = 2600000
    populacao_ficticia['Caucaia'] = 360000
    populacao_ficticia['Juazeiro do Norte'] = 270000
    populacao_ficticia['Sobral'] = 210000
    
    df_mapa['Populacao'] = df_mapa['Município'].map(populacao_ficticia).fillna(50000)
    
    # Cálculo da Taxa por 100 mil habitantes (Ocorrências)
    df_mapa['Taxa_100k'] = (df_mapa['Ocorrencias'] / df_mapa['Populacao']) * 100000

    # 3. Seletor de Camada do Mapa
    camada = st.radio(
        "Selecione a Métrica do Mapa:",
        options=["Total de Ocorrências", "Volume Apreendido (Kg)", "Taxa (Ocorrências por 100k hab)"],
        horizontal=True
    )

    # Configuração dinâmica de acordo com a seleção
    if camada == "Total de Ocorrências":
        coluna_valor = 'Ocorrencias'
        escala_cor = 'Blues'
        titulo_legenda = "Qtd. Ocorrências"
    elif camada == "Volume Apreendido (Kg)":
        coluna_valor = 'Volume_Kg'
        escala_cor = 'Reds' # Vermelho destaca bem o "Heatmap" de peso
        titulo_legenda = "Volume (Kg)"
    else:
        coluna_valor = 'Taxa_100k'
        escala_cor = 'Purples'
        titulo_legenda = "Taxa / 100k hab"

    # 4. Renderização do Mapa Coroplético
    # IMPORTANTE: Coloque o caminho correto do seu arquivo GeoJSON do Ceará aqui!
    caminho_geojson = 'dataSett/ceara.json' 
    
    if os.path.exists(caminho_geojson):
        with open(caminho_geojson, encoding='utf-8') as f:
            geojson_ce = json.load(f)
            
        fig_mapa = px.choropleth_mapbox(
            df_mapa,
            geojson=geojson_ce,
            locations='Município',
            featureidkey='properties.name', # Verifique se no seu GeoJSON o nome da cidade está em 'name'
            color=coluna_valor,
            color_continuous_scale=escala_cor,
            mapbox_style="carto-positron",
            zoom=5.5,
            center={"lat": -5.20, "lon": -39.53},
            opacity=0.7,
            hover_name='Município',
            hover_data={
                'Ocorrencias': True,
                'Volume_Kg': ':.2f',
                'Taxa_100k': ':.1f',
                'Município': False
            }
        )
        fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        st.warning(f":material/warning: Arquivo GeoJSON '{caminho_geojson}' não encontrado. Certifique-se de usar o mesmo caminho do mapa de CVLI.")
        
        # Fallback (Plano B): Se o GeoJSON falhar, renderiza um gráfico de barras focado na métrica escolhida
        fig_fallback = px.bar(df_mapa.sort_values(by=coluna_valor, ascending=False).head(15), 
                              x=coluna_valor, y='Município', orientation='h', color=coluna_valor, color_continuous_scale=escala_cor)
        fig_fallback.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_fallback, use_container_width=True) 
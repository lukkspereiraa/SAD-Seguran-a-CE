import streamlit as st
import plotly.express as px
import pandas as pd
from services.ibge import carregar_populacao_ibge_ceara, carregar_geojson, normalizar_texto

def render(df_filtrado):
    st.markdown("#### Mancha de Calor Geográfica")
    if df_filtrado.empty: return

    df_agrupado = df_filtrado.groupby('Município').size().reset_index(name='Focos de Incêndio')
    df_agrupado['Município_Tratado'] = df_agrupado['Município'].apply(normalizar_texto)
    
    geojson_ce, lista_cidades = carregar_geojson()
    populacao_ibge = carregar_populacao_ibge_ceara()
    
    df_base = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_base, df_agrupado[['Município_Tratado', 'Focos de Incêndio']], on='Município_Tratado', how='left').fillna(0)
    
    df_mapa['População (IBGE)'] = df_mapa['Município_Tratado'].map(populacao_ibge).fillna(35000)
    df_mapa['Taxa (por 100k hab.)'] = round((df_mapa['Focos de Incêndio'] / df_mapa['População (IBGE)']) * 100000, 2)
    
    metrica_mapa = st.radio("Métrica:", ["Focos de Incêndio", "Taxa (por 100k hab.)"], horizontal=True, key="mapa_fogo")
    
    # Paleta de Fogo: Oranges
    fig_mapa = px.choropleth(
        df_mapa, geojson=geojson_ce, locations='Município_Tratado', featureidkey="properties.name", 
        color=metrica_mapa, color_continuous_scale='Oranges', hover_name='Município_Tratado',
        hover_data={'Município_Tratado': False, 'Focos de Incêndio': True, 'Taxa (por 100k hab.)': True}
    )
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=600)
    st.plotly_chart(fig_mapa, use_container_width=True)
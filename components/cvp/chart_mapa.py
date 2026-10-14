import streamlit as st
import plotly.express as px
import pandas as pd
from services.ibge import carregar_populacao_ibge_ceara, carregar_geojson, normalizar_texto

def render(df_filtrado):
    st.subheader("Mapa Tático de Roubos (CVP)")
    
    with st.popover("Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        Mapeamento de roubos violentos. 
        * **Engenharia de Dados (Microsserviços):** A taxa populacional é consumida em tempo real via API do Censo 2022 do IBGE.
        * **Engenharia de Dados (Preenchimento de Vazios):** Municípios sem ocorrências recebem automaticamente o valor "0" (zero).
        """)

    if df_filtrado.empty: return

    df_agrupado = df_filtrado.groupby('Município').size().reset_index(name='Total de Roubos')
    df_agrupado['Município_Tratado'] = df_agrupado['Município'].apply(normalizar_texto)
    
    geojson_ce, lista_cidades = carregar_geojson()
    populacao_ibge = carregar_populacao_ibge_ceara()
    
    df_base = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_base, df_agrupado[['Município_Tratado', 'Total de Roubos']], on='Município_Tratado', how='left')
    
    df_mapa['Total de Roubos'] = df_mapa['Total de Roubos'].fillna(0)
    df_mapa['População (IBGE)'] = df_mapa['Município_Tratado'].map(populacao_ibge).fillna(35000)
    df_mapa['Taxa (Roubos por 100k hab.)'] = round((df_mapa['Total de Roubos'] / df_mapa['População (IBGE)']) * 100000, 2)
    
    metrica_mapa = st.radio("Métrica Geográfica:", ["Total de Roubos", "Taxa (Roubos por 100k hab.)"], horizontal=True)
    cor_escala = "Reds" if metrica_mapa == "Total de Roubos" else "Inferno"

    fig_mapa = px.choropleth(
        df_mapa, geojson=geojson_ce, locations='Município_Tratado', featureidkey="properties.name", 
        color=metrica_mapa, color_continuous_scale=cor_escala, hover_name='Município_Tratado',
        hover_data={'Município_Tratado': False, 'Total de Roubos': True, 'Taxa (Roubos por 100k hab.)': True, 'População (IBGE)': True}
    )
    
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=650)
    st.plotly_chart(fig_mapa, use_container_width=True)
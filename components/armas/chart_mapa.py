import streamlit as st
import plotly.express as px
import pandas as pd
# Importação centralizada a partir do nosso novo serviço
from services.ibge import carregar_populacao_ibge_ceara, carregar_geojson, normalizar_texto

def render(df_filtrado):
    st.subheader("Mapa Tático de Desarmamento")
    
    with st.popover("Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        O mapa exibe a concentração de desarmamento nas subdivisões dos 184 municípios cearenses focado em Armas de Fogo.
        
        **Regras de Negócio e Tratamento:**
        * **Total de Armas:** Soma o volume absoluto de armas apreendidas.
        * **Taxa por 100k hab.:** Calcula a densidade de apreensões proporcionalmente à população do município consumida em tempo real via API do Censo 2022 do IBGE. Isso revela se cidades do interior estão apresentando uma circulação de armas desproporcional ao seu tamanho.
        * **Engenharia de Dados (Preenchimento de Vazios):** Municípios sem registros de casos no período filtrado recebem automaticamente o valor "0" (zero).
        """)
        
    if df_filtrado.empty:
        st.warning("Nenhum dado para exibir no mapa.")
        return

    # Agrupamento de Dados (Ocorrências e Soma das Armas)
    df_agrupado = df_filtrado.groupby('Município').agg(
        Total_Ocorrencias=('Município', 'count'),
        Total_Armas=('Quantidade', 'sum')
    ).reset_index()
    
    df_agrupado['Município_Tratado'] = df_agrupado['Município'].apply(normalizar_texto)
    
    # Carrega o mapa e junta com os dados
    geojson_ce, lista_cidades = carregar_geojson()
    populacao_ibge = carregar_populacao_ibge_ceara()
    
    df_base = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_base, df_agrupado[['Município_Tratado', 'Total_Ocorrencias', 'Total_Armas']], on='Município_Tratado', how='left')
    
    # Preenchimento de vazios e cálculo de taxa
    df_mapa['Total_Ocorrencias'] = df_mapa['Total_Ocorrencias'].fillna(0)
    df_mapa['Total_Armas'] = df_mapa['Total_Armas'].fillna(0)
    
    # Injeta a população oficial do IBGE e calcula a taxa
    df_mapa['População (IBGE)'] = df_mapa['Município_Tratado'].map(populacao_ibge).fillna(35000)
    df_mapa['Taxa (Armas por 100k hab.)'] = round((df_mapa['Total_Armas'] / df_mapa['População (IBGE)']) * 100000, 2)
    
    df_mapa = df_mapa.rename(columns={'Total_Ocorrencias': 'Total de Ocorrências', 'Total_Armas': 'Total de Armas'})

    # Toggle de Métrica
    metrica_mapa = st.radio(
        "Métrica de Análise Geográfica:", 
        options=["Total de Armas", "Taxa (Armas por 100k hab.)"], 
        horizontal=True
    )
    
    cor_escala = "Reds" if metrica_mapa == "Total de Armas" else "Inferno"

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
            'Total de Armas': True, 
            'Taxa (Armas por 100k hab.)': True, 
            'População (IBGE)': True
        },
        labels={metrica_mapa: 'Índice'}
    )
    
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=650)
    
    st.plotly_chart(fig_mapa, use_container_width=True)
import streamlit as st
import plotly.express as px
import pandas as pd
# Importação centralizada a partir do nosso novo serviço
from services.ibge import carregar_populacao_ibge_ceara, carregar_geojson, normalizar_texto

def render(df_filtrado):
    st.subheader("Mapa Tático de Apreensões")
    
    with st.popover("Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        O mapa exibe as subdivisões dos 184 municípios cearenses. É possível alternar a visualização para focar no volume apreendido (Peso em Kg), no número absoluto de ocorrências policiais, ou na taxa por 100 mil habitantes.
        
        **Regras de Negócio e Tratamento:**
        * **Engenharia de Dados (Preenchimento de Vazios):** Municípios sem registros de apreensão de drogas no período filtrado recebem automaticamente o valor "0" (zero).
        * **Engenharia de Dados (Microsserviços):** A taxa populacional é consumida em tempo real via API do Censo 2022 do IBGE.
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
    
    # 2. Carrega o mapa e a lista oficial de todas as cidades usando o Serviço Central
    geojson_ce, lista_cidades = carregar_geojson()
    populacao_ibge = carregar_populacao_ibge_ceara()
    
    # 3. Cria um DataFrame base com as 184 cidades e junta com os crimes
    df_base = pd.DataFrame({'Município_Tratado': lista_cidades})
    df_mapa = pd.merge(df_base, df_agrupado[['Município_Tratado', 'Total_Ocorrencias', 'Volume_Kg']], on='Município_Tratado', how='left')
    
    # Preenche com 0 os municípios que não tiveram apreensões
    df_mapa['Total_Ocorrencias'] = df_mapa['Total_Ocorrencias'].fillna(0)
    df_mapa['Volume_Kg'] = df_mapa['Volume_Kg'].fillna(0)
    
    # 4. Injeta a população oficial do IBGE e calcula a taxa
    df_mapa['População (IBGE)'] = df_mapa['Município_Tratado'].map(populacao_ibge).fillna(35000)
    df_mapa['Taxa (por 100k hab.)'] = round((df_mapa['Total_Ocorrencias'] / df_mapa['População (IBGE)']) * 100000, 2)
    
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
            'População (IBGE)': True # Trocado para o dado do IBGE
        },
        labels={metrica_mapa: 'Índice'}
    )
    
    # O segredo para não mostrar o globo terrestre:
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":0}, height=650)
    
    st.plotly_chart(fig_mapa, use_container_width=True)
import streamlit as st
import pandas as pd
from services.data_handler import carregar_dados

# Importando os nossos novos módulos de visão
import views.view_cvli as view_cvli
import views.view_entorpecentes as view_entorpecentes

st.set_page_config(page_title="SAD | Segurança CE", page_icon=":material/shield:", layout="wide", initial_sidebar_state="expanded")
st.title(":material/analytics: SAD - Inteligência em Segurança Pública (Ceará)")
st.markdown("Plataforma Modular de Apoio à Decisão.")
st.divider()

# 1. CARREGAMENTO DOS DADOS
df_cvli, df_ent = carregar_dados()

# 2. MENU LATERAL: Filtros Globais
with st.sidebar:
    st.header(":material/tune: Parâmetros de Análise")
    datasets = st.multiselect(":material/database: Bases Ativas:", ["CVLI", "Entorpecentes"], default=["CVLI"])
    st.divider()
    
    min_d = df_cvli['Data'].min().date()
    max_d = df_cvli['Data'].max().date()
    datas = st.date_input(":material/calendar_month: Período:", value=(min_d, max_d), min_value=min_d, max_value=max_d)
    
    st.subheader(":material/map: Territorial e Tático")
    municipios = st.multiselect(":material/location_city: Municípios:", sorted(df_cvli['Município'].dropna().unique()))
    ais = st.multiselect(":material/share_location: AIS:", sorted(df_cvli['AIS'].dropna().unique()))

# 3. ROTEAMENTO DE RENDERIZAÇÃO
if not datasets:
    st.warning(":material/warning: Selecione pelo menos um módulo analítico na barra lateral.")
    st.stop()

abas = st.tabs(datasets)

# Dicionário para guardar os dataframes filtrados que retornarão das views
dataframes_filtrados = {}

for index, modulo in enumerate(datasets):
    with abas[index]:
        match modulo:
            case "CVLI":
                # Chama a view de CVLI e guarda o retorno
                df_filtrado = view_cvli.render(df_cvli, datas, municipios, ais)
                dataframes_filtrados["CVLI"] = df_filtrado
                
            case "Entorpecentes":
                # Chama a view de Entorpecentes e guarda o retorno
                df_filtrado = view_entorpecentes.render(df_ent, datas, municipios, ais)
                dataframes_filtrados["Entorpecentes"] = df_filtrado
                
            case _:
                st.error(":material/error: Módulo não reconhecido.")

# 4. EXIBIÇÃO DA TABELA BRUTA MESCLADA
st.divider()
if st.checkbox("Exibir Base de Dados Tratada (Dataframe)"):
    bases_mescladas = []
    
    if "CVLI" in dataframes_filtrados and not dataframes_filtrados["CVLI"].empty:
        bases_mescladas.append(dataframes_filtrados["CVLI"].assign(**{'Fonte dos Dados': 'CVLI'}))
        
    if "Entorpecentes" in dataframes_filtrados and not dataframes_filtrados["Entorpecentes"].empty:
        bases_mescladas.append(dataframes_filtrados["Entorpecentes"].assign(**{'Fonte dos Dados': 'Entorpecentes'}))
        
    if bases_mescladas:
        df_final = pd.concat(bases_mescladas, ignore_index=True)
        colunas_ordenadas = ['Fonte dos Dados'] + [col for col in df_final.columns if col != 'Fonte dos Dados']
        st.dataframe(df_final[colunas_ordenadas].drop(columns=['Hora_Pico', 'Idade Numérica'], errors='ignore'), use_container_width=True)
    else:
        st.warning("Não há dados para exibir com os filtros atuais.")
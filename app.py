import streamlit as st
import pandas as pd
from services.data_handler import carregar_dados

# Importando os nossos módulos de visão
import views.view_cvli as view_cvli
import views.view_entorpecentes as view_entorpecentes
import views.view_armas as view_armas
import views.view_salvamento as view_salvamento
import views.view_maria_penha as view_maria_penha # <-- NOVO MÓDULO IMPORTADO

st.set_page_config(page_title="SAD | Segurança CE", page_icon=":material/shield:", layout="wide", initial_sidebar_state="expanded")
st.title(":material/analytics: SAD - Inteligência em Segurança Pública (Ceará)")
st.markdown("Plataforma Modular de Apoio à Decisão.")
st.divider()

# 1. CARREGAMENTO DOS DADOS (Agora retorna 5 bases)
df_cvli, df_ent, df_armas, df_salvamento, df_mp = carregar_dados()

# 2. MENU LATERAL: Filtros Globais
with st.sidebar:
    st.header(":material/tune: Parâmetros de Análise")
    
    # Adicionamos "Maria da Penha" na lista
    datasets = st.multiselect(
        ":material/database: Bases Ativas:", 
        ["CVLI", "Entorpecentes", "Armas de Fogo", "Salvamento (CBMCE)", "Violência Doméstica (Maria da Penha)"], 
        default=[]
    )
    st.divider()
    
    min_d = df_cvli['Data'].min().date()
    max_d = df_cvli['Data'].max().date()
    datas = st.date_input(":material/calendar_month: Período:", value=(min_d, max_d), min_value=min_d, max_value=max_d)
    
    st.subheader(":material/map: Territorial e Tático")
    municipios = st.multiselect(":material/location_city: Municípios:", sorted(df_cvli['Município'].dropna().unique()))
    ais = st.multiselect(":material/share_location: AIS:", sorted(df_cvli['AIS'].dropna().unique()))

# 3. ROTEAMENTO DE RENDERIZAÇÃO (LANDING PAGE)
if not datasets:
    st.info(":material/swipe_left: **Selecione pelo menos um módulo analítico na barra lateral para iniciar a visualização.**")
    
    st.markdown("### Módulos Disponíveis:")
    st.markdown("**:material/emergency: CVLI (Crimes contra a Vida)**")
    st.markdown("**:material/local_police: Entorpecentes (Tráfico de Drogas)**")
    st.markdown("**:material/crisis_alert: Armas de Fogo (Desarmamento)**")
    st.markdown("**:material/medical_services: Salvamento (Bombeiros/Defesa Civil)**")
    st.markdown("**:material/family_restroom: Violência Doméstica (Maria da Penha)**") # <-- NOVO
    st.stop() 

abas = st.tabs(datasets)
dataframes_filtrados = {}

for index, modulo in enumerate(datasets):
    with abas[index]:
        match modulo:
            case "CVLI":
                df_filtrado = view_cvli.render(df_cvli, datas, municipios, ais)
                dataframes_filtrados["CVLI"] = df_filtrado
                
            case "Entorpecentes":
                df_filtrado = view_entorpecentes.render(df_ent, datas, municipios, ais)
                dataframes_filtrados["Entorpecentes"] = df_filtrado
                
            case "Armas de Fogo":
                df_filtrado = view_armas.render(df_armas, datas, municipios, ais)
                dataframes_filtrados["Armas de Fogo"] = df_filtrado
                
            case "Salvamento (CBMCE)":
                df_filtrado = view_salvamento.render(df_salvamento, datas, municipios, ais)
                dataframes_filtrados["Salvamento"] = df_filtrado
                
            case "Violência Doméstica (Maria da Penha)": # <-- ROTEAMENTO DA NOVA TELA
                df_filtrado = view_maria_penha.render(df_mp, datas, municipios, ais)
                dataframes_filtrados["Maria da Penha"] = df_filtrado
                
            case _:
                st.error(":material/error: Módulo não reconhecido.")

# 4. EXIBIÇÃO DA TABELA BRUTA MESCLADA
st.divider()
if st.checkbox("Exibir Base de Dados Tratada (Dataframe)"):
    bases_mescladas = []
    
    nomes_modulos = ["CVLI", "Entorpecentes", "Armas de Fogo", "Salvamento", "Maria da Penha"]
    
    for nome in nomes_modulos:
        if nome in dataframes_filtrados and not dataframes_filtrados[nome].empty:
            bases_mescladas.append(dataframes_filtrados[nome].assign(**{'Fonte dos Dados': nome}))
        
    if bases_mescladas:
        df_final = pd.concat(bases_mescladas, ignore_index=True)
        colunas_ordenadas = ['Fonte dos Dados'] + [col for col in df_final.columns if col != 'Fonte dos Dados']
        st.dataframe(df_final[colunas_ordenadas].drop(columns=['Hora_Pico', 'Idade Numérica'], errors='ignore'), use_container_width=True)
    else:
        st.warning("Não há dados para exibir com os filtros atuais.")
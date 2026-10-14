import streamlit as st
import pandas as pd
from services.data_handler import carregar_dados

# Importação dos módulos de visão (13 Módulos!)
import views.view_cvli as view_cvli
import views.view_entorpecentes as view_entorpecentes
import views.view_armas as view_armas
import views.view_salvamento as view_salvamento
import views.view_maria_penha as view_maria_penha
import views.view_lgbtfobia as view_lgbtfobia
import views.view_racismo as view_racismo 
import views.view_furto as view_furto
import views.view_cvp as view_cvp
import views.view_crimes_sexuais as view_crimes_sexuais
import views.view_indigenas as view_indigenas
import views.view_animais as view_animais
import views.view_incendios as view_incendios # <-- Importação Incêndios

st.set_page_config(page_title="SAD | Segurança CE", layout="wide", initial_sidebar_state="expanded")
st.title("SAD - Inteligência em Segurança Pública (Ceará)")
st.divider()

# 1. CARREGAMENTO DOS DADOS (As 13 bases)
df_cvli, df_ent, df_armas, df_salvamento, df_mp, df_lgbt, df_racismo, df_furto, df_cvp, df_sexuais, df_indigenas, df_animais, df_incendios = carregar_dados()

# 2. MENU LATERAL GERAL
with st.sidebar:
    st.header("Parâmetros de Análise")
    
    datasets = st.multiselect(
        "Módulos Analíticos:", 
        [
            "CVLI (Crimes contra a Vida)", 
            "Entorpecentes (Tráfico)", 
            "Armas de Fogo", 
            "Salvamento (CBMCE)", 
            "Maria da Penha (Violência Doméstica)", 
            "LGBTfobia (Intolerância)",
            "Racismo (Intolerância)", 
            "Furto (Crimes contra o Património)",
            "CVP (Roubos e Assaltos)",
            "Crimes Sexuais (Dignidade Sexual)",
            "Povos Indígenas (Violência contra Originários)",
            "Crimes Ambientais (Maus-Tratos a Animais)",
            "Incêndios (Operações CBMCE)" # <-- Último Módulo adicionado
        ], 
        default=[]
    )
    st.divider()
    
    min_d = df_cvli['Data'].min().date()
    max_d = df_cvli['Data'].max().date()
    datas = st.date_input("Período:", value=(min_d, max_d), min_value=min_d, max_value=max_d)
    
    st.subheader("Territorial e Tático")
    municipios = st.multiselect("Municípios:", sorted(df_cvli['Município'].dropna().unique()))
    ais = st.multiselect("AIS:", sorted(df_cvli['AIS'].dropna().unique()))

# 3. ROTEAMENTO
if not datasets:
    st.info("Selecione pelo menos um módulo analítico na barra lateral para iniciar a visualização.")
    st.stop() 

abas = st.tabs(datasets)
dataframes_filtrados = {}

for index, modulo in enumerate(datasets):
    with abas[index]:
        match modulo:
            case "CVLI (Crimes contra a Vida)":
                df_filtrado = view_cvli.render(df_cvli, datas, municipios, ais)
                dataframes_filtrados["CVLI"] = df_filtrado
            case "Entorpecentes (Tráfico)":
                df_filtrado = view_entorpecentes.render(df_ent, datas, municipios, ais)
                dataframes_filtrados["Entorpecentes"] = df_filtrado
            case "Armas de Fogo":
                df_filtrado = view_armas.render(df_armas, datas, municipios, ais)
                dataframes_filtrados["Armas de Fogo"] = df_filtrado
            case "Salvamento (CBMCE)":
                df_filtrado = view_salvamento.render(df_salvamento, datas, municipios, ais)
                dataframes_filtrados["Salvamento"] = df_filtrado
            case "Maria da Penha (Violência Doméstica)":
                df_filtrado = view_maria_penha.render(df_mp, datas, municipios, ais)
                dataframes_filtrados["Maria da Penha"] = df_filtrado
            case "LGBTfobia (Intolerância)":
                df_filtrado = view_lgbtfobia.render(df_lgbt, datas, municipios, ais)
                dataframes_filtrados["LGBTfobia"] = df_filtrado
            case "Racismo (Intolerância)":
                df_filtrado = view_racismo.render(df_racismo, datas, municipios, ais)
                dataframes_filtrados["Racismo"] = df_filtrado
            case "Furto (Crimes contra o Património)":
                df_filtrado = view_furto.render(df_furto, datas, municipios, ais)
                dataframes_filtrados["Furto"] = df_filtrado
            case "CVP (Roubos e Assaltos)":
                df_filtrado = view_cvp.render(df_cvp, datas, municipios, ais)
                dataframes_filtrados["CVP"] = df_filtrado
            case "Crimes Sexuais (Dignidade Sexual)":
                df_filtrado = view_crimes_sexuais.render(df_sexuais, datas, municipios, ais)
                dataframes_filtrados["Crimes Sexuais"] = df_filtrado
            case "Povos Indígenas (Violência contra Originários)":
                df_filtrado = view_indigenas.render(df_indigenas, datas, municipios, ais)
                dataframes_filtrados["Indigenas"] = df_filtrado
            case "Crimes Ambientais (Maus-Tratos a Animais)":
                df_filtrado = view_animais.render(df_animais, datas, municipios, ais)
                dataframes_filtrados["Animais"] = df_filtrado
            case "Incêndios (Operações CBMCE)":
                df_filtrado = view_incendios.render(df_incendios, datas, municipios, ais)
                dataframes_filtrados["Incendios"] = df_filtrado
            case _:
                st.error("Módulo não reconhecido.")

# 4. EXIBIÇÃO DA BASE MESCLADA (Download)
st.divider()
col1, col2 = st.columns([8, 2])
with col1:
    exibir_tabela = st.checkbox("Exibir Base de Dados Tratada (Dataframe)")

if exibir_tabela:
    bases_mescladas = []
    nomes_modulos = ["CVLI", "Entorpecentes", "Armas de Fogo", "Salvamento", "Maria da Penha", "LGBTfobia", "Racismo", "Furto", "CVP", "Crimes Sexuais", "Indigenas", "Animais", "Incendios"]
    
    for nome in nomes_modulos:
        if nome in dataframes_filtrados and not dataframes_filtrados[nome].empty:
            bases_mescladas.append(dataframes_filtrados[nome].assign(**{'Fonte dos Dados': nome}))
        
    if bases_mescladas:
        df_final = pd.concat(bases_mescladas, ignore_index=True)
        colunas_ordenadas = ['Fonte dos Dados'] + [col for col in df_final.columns if col != 'Fonte dos Dados']
        df_limpo = df_final[colunas_ordenadas].drop(columns=['Hora_Pico', 'Idade Numérica', 'Hora_Int'], errors='ignore')
        
        st.dataframe(df_limpo, use_container_width=True)
        
        with col2:
            csv = df_limpo.to_csv(index=False).encode('utf-8')
            st.download_button(label="Descarregar Relatório (CSV)", data=csv, file_name="SAD_Seguranca_Relatorio.csv", mime="text/csv", type="primary")
    else:
        st.warning("Não há dados para exibir.")
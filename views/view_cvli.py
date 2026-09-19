import streamlit as st
from services.data_handler import filtrar_dados_cvli

# Importações dos gráficos específicos de CVLI
import components.cvli.chart_territorio as chart_territorio
import components.cvli.chart_tempo as chart_tempo
import components.cvli.chart_cruzamentos as chart_cruzamentos
import components.cvli.chart_rodape as chart_rodape 
import components.cvli.chart_mapa as chart_mapa 

def render(df_cvli, datas, municipios, ais):
    st.subheader(":material/emergency: Análise de Crimes Violentos Letais Intencionais")
    
    # Filtros Específicos do CVLI (5 colunas)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: meios = st.multiselect(":material/hardware: Arma:", sorted(df_cvli['Meio Empregado'].dropna().unique()))
    with col2: generos = st.multiselect(":material/wc: Gênero:", sorted(df_cvli['Gênero'].dropna().unique()))
    with col3: faixas = st.multiselect(":material/calendar_today: Faixa Etária:", ['0 a 17 anos', '18 a 29 anos', '30 a 59 anos', '60+ anos (Idosos)', 'Não Informada'])
    with col4: escolaridades = st.multiselect(":material/school: Escolaridade:", sorted(df_cvli['Escolaridade da Vítima'].astype(str).unique()))
    with col5: naturezas = st.multiselect(":material/gavel: Natureza:", sorted(df_cvli['Natureza'].dropna().astype(str).unique()))
    
    # Processamento e Filtro
    df_cvli_filtrado = filtrar_dados_cvli(df_cvli, datas, municipios, ais, meios, faixas, escolaridades, generos, naturezas)
    
    if df_cvli_filtrado.empty:
        st.warning(":material/search_off: Nenhum registro encontrado com estes filtros.")
        return df_cvli_filtrado # Retorna vazio para a tabela do app.py não quebrar

    # Renderização dos KPIs e Gráficos
    st.metric(label=":material/troubleshoot: Total de CVLI", value=f"{df_cvli_filtrado.shape[0]:,}".replace(',', '.'))
    chart_mapa.render(df_cvli_filtrado)
    st.divider()
    
    aba_terr, aba_temp, aba_perf = st.tabs([":material/location_on: Territorial", ":material/schedule: Temporal", ":material/psychology: Cruzamentos"])
    with aba_terr: chart_territorio.render(df_cvli_filtrado)
    with aba_temp: chart_tempo.render(df_cvli_filtrado)
    with aba_perf: chart_cruzamentos.render(df_cvli_filtrado)
    
    chart_rodape.render(df_cvli_filtrado)
    
    # Devolve o dataframe filtrado para o Orquestrador (app.py) poder usar na tabela mesclada
    return df_cvli_filtrado
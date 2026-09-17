import streamlit as st
from services.data_handler import carregar_dados, filtrar_dados_cvli

import components.chart_territorio as chart_territorio
import components.chart_tempo as chart_tempo
import components.chart_cruzamentos as chart_cruzamentos
import components.chart_intervencao as chart_intervencao
import components.chart_rodape as chart_rodape 
import components.chart_mapa as chart_mapa 

# 1. Configuração inicial
st.set_page_config(page_title="SAD | Segurança CE", page_icon=":material/shield:", layout="wide", initial_sidebar_state="expanded")

# 2. Cabeçalho
st.title(":material/analytics: SAD - Inteligência em Segurança Pública (Ceará)")
st.markdown("Plataforma de Apoio à Decisão com análise demográfica e tática.")
st.divider()

# 3. Carregamento
df_cvli, df_ip, df_up = carregar_dados()

# 4. Barra Lateral (Sidebar)
st.sidebar.header(":material/tune: Parâmetros de Análise")

min_date, max_date = df_cvli['Data'].min().date(), df_cvli['Data'].max().date()
datas_selecionadas = st.sidebar.date_input("Período de Referência:", value=(min_date, max_date), min_value=min_date, max_value=max_date)

st.sidebar.divider()

st.sidebar.subheader(":material/map: Territorial e Tático")
municipios_selecionados = st.sidebar.multiselect("Municípios:", options=sorted(df_cvli['Município'].dropna().unique()))
ais_selecionadas = st.sidebar.multiselect("Área Integrada de Segurança (AIS):", options=sorted(df_cvli['AIS'].dropna().unique()))
meios_selecionados = st.sidebar.multiselect("Meio Empregado (Arma):", options=sorted(df_cvli['Meio Empregado'].dropna().unique()))

st.sidebar.subheader(":material/group: Perfil Social")
genero_selecionado = st.sidebar.multiselect("Gênero da Vítima:", options=sorted(df_cvli['Gênero'].dropna().unique()))
faixa_selecionada = st.sidebar.multiselect("Faixa Etária:", options=['0 a 17 anos', '18 a 29 anos', '30 a 59 anos', '60+ anos (Idosos)', 'Não Informada'])
escolaridade_selecionada = st.sidebar.multiselect("Grau de Escolaridade:", options=sorted(df_cvli['Escolaridade da Vítima'].astype(str).unique()))

# --- NOVO BLOCO NA BARRA LATERAL ---
st.sidebar.subheader(":material/gavel: Tipificação Penal")
natureza_selecionada = st.sidebar.multiselect("Natureza da Ocorrência:", options=sorted(df_cvli['Natureza'].dropna().astype(str).unique()))

# 5. Aplicação de Filtros
df_filtrado = filtrar_dados_cvli(
    df_cvli, datas_selecionadas, municipios_selecionados, ais_selecionadas, 
    meios_selecionados, faixa_selecionada, escolaridade_selecionada, genero_selecionado, natureza_selecionada
)

# --- TRAVA DE SEGURANÇA (FILTRO VAZIO) ---
if df_filtrado.empty:
    st.warning("⚠️ Nenhum registro encontrado para a combinação de filtros atual. Altere os parâmetros na barra lateral.")
    st.stop()

# 6. Painel de Indicadores
colA, colB, colC = st.columns(3)
colA.metric(label=":material/emergency: Registros CVLI", value=f"{df_filtrado.shape[0]:,}".replace(',', '.'))
colB.metric(label=":material/local_police: Intervenção Policial", value=f"{df_ip.shape[0]:,}".replace(',', '.'))
colC.metric(label=":material/lock: Sistema Prisional", value=f"{df_up.shape[0]:,}".replace(',', '.'))

st.divider()

# --- NOVO MAPA GLOBAL (EM CIMA DE TUDO) ---
chart_mapa.render(df_filtrado)
st.divider()

# 7. Renderização das Abas Superiores
aba1, aba2, aba3, aba4 = st.tabs([
    ":material/location_on: Análise Territorial", 
    ":material/schedule: Dinâmica Temporal", 
    ":material/psychology: Cruzamento de Perfis", 
    ":material/admin_panel_settings: Intervenções Policiais"
])

with aba1:
    chart_territorio.render(df_filtrado)
with aba2:
    chart_tempo.render(df_filtrado)
with aba3:
    chart_cruzamentos.render(df_filtrado)
with aba4:
    chart_intervencao.render(df_ip)

st.divider()

# 8. RENDERIZAÇÃO DOS GRÁFICOS GLOBAIS DE RODAPÉ
chart_rodape.render(df_filtrado)

st.divider()
if st.checkbox("Exibir Base de Dados Tratada (Dataframe)"):
    st.dataframe(df_filtrado.drop(columns=['Hora_Pico', 'Idade Numérica'], errors='ignore'), use_container_width=True)
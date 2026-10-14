import streamlit as st
import pandas as pd
from services.data_handler import filtrar_dados_crimes_sexuais

# Importação de todos os componentes
import components.sexuais.chart_demografia as chart_demografia
import components.sexuais.chart_vulnerabilidade as chart_vulnerabilidade
import components.sexuais.chart_mapa as chart_mapa
import components.sexuais.chart_temporal as chart_temporal
import components.sexuais.chart_pareto as chart_pareto
import components.sexuais.chart_evolucao as chart_evolucao         # NOVO
import components.sexuais.chart_probabilidade as chart_probabilidade # NOVO

def render(df_sexuais, datas, municipios, ais):
    st.subheader("Crimes Sexuais (Dignidade Sexual)")
    
    with st.popover("Metodologia e Leitura Tática"):
        st.markdown("""
        **Diretrizes de Leitura:**
        Esta métrica engloba crimes contra a dignidade sexual (Estupro, Estupro de Vulnerável, Importunação Sexual, etc.).
        
        **Foco Tático e Social:**
        A alta incidência em faixas etárias baixas sugere crimes intrafamiliares. O cruzamento de escolaridade e raça dita a alocação de assistentes sociais e delegacias especializadas.
        """)
        
    if df_sexuais.empty:
        st.warning("Base de dados não encontrada.")
        return df_sexuais

    # Filtro global (Data e Local)
    df_filtrado = filtrar_dados_crimes_sexuais(df_sexuais, datas, municipios, ais)
    
    if df_filtrado.empty:
        st.warning("Nenhum registo encontrado com os filtros selecionados.")
        return df_filtrado

    # --- INÍCIO: 5 FILTROS TÁTICOS DE DRILL-DOWN ---
    st.markdown("##### Filtros de Investigação")
    
    # Agora com 5 colunas para acomodar a Escolaridade!
    col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)
    
    with col_f1:
        if 'Gênero' in df_filtrado.columns:
            opcoes_genero = sorted(df_filtrado['Gênero'].dropna().unique())
            filtro_genero = st.multiselect("Isolar Género:", opcoes_genero, default=[])
        else: filtro_genero = []
            
    with col_f2:
        if 'Raça da Vítima' in df_filtrado.columns:
            opcoes_raca = sorted(df_filtrado['Raça da Vítima'].dropna().unique())
            filtro_raca = st.multiselect("Isolar Raça/Cor:", opcoes_raca, default=[])
        else: filtro_raca = []
        
    with col_f3:
        if 'Escolaridade da Vítima' in df_filtrado.columns:
            opcoes_esc = sorted(df_filtrado['Escolaridade da Vítima'].dropna().unique())
            filtro_esc = st.multiselect("Isolar Escolaridade:", opcoes_esc, default=[])
        else: filtro_esc = []
            
    with col_f4:
        if 'Dia da Semana' in df_filtrado.columns:
            dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            filtro_dias = st.multiselect("Isolar Dia:", dias_semana, default=[])
        else: filtro_dias = []
            
    with col_f5:
        filtro_horas = st.slider("Horário (0h-23h):", 0, 23, (0, 23))

    # Aplicação dos filtros
    if filtro_genero: df_filtrado = df_filtrado[df_filtrado['Gênero'].isin(filtro_genero)]
    if filtro_raca: df_filtrado = df_filtrado[df_filtrado['Raça da Vítima'].isin(filtro_raca)]
    if filtro_esc: df_filtrado = df_filtrado[df_filtrado['Escolaridade da Vítima'].isin(filtro_esc)] # Aplica Escolaridade
    if filtro_dias: df_filtrado = df_filtrado[df_filtrado['Dia da Semana'].isin(filtro_dias)]
        
    if 'Hora' in df_filtrado.columns:
        df_filtrado['Hora_Int'] = pd.to_datetime(df_filtrado['Hora'], format='%H:%M:%S', errors='coerce').dt.hour
        df_filtrado = df_filtrado[(df_filtrado['Hora_Int'] >= filtro_horas[0]) & (df_filtrado['Hora_Int'] <= filtro_horas[1])]

    if df_filtrado.empty:
        st.warning("A combinação de filtros selecionada não possui registos. Tente alargar a sua pesquisa.")
        return df_filtrado
    # --- FIM DOS FILTROS ---

    st.divider()
    kpi1, kpi2, kpi3 = st.columns(3)
    total_casos = df_filtrado.shape[0]
    kpi1.metric(label="Volume Filtrado", value=f"{total_casos:,}".replace(',', '.'))
    
    if total_casos > 0:
        cidade_pior = df_filtrado['Município'].mode()[0]
        kpi2.metric(label="Ponto Crítico (Município)", value=cidade_pior)
        
        if 'Idade da Vítima' in df_filtrado.columns:
            idades_numericas = pd.to_numeric(df_filtrado['Idade da Vítima'], errors='coerce')
            idade_med = idades_numericas.median()
            if pd.notna(idade_med): kpi3.metric(label="Idade Mediana da Vítima", value=f"{int(idade_med)} anos")
            else: kpi3.metric(label="Idade Mediana", value="S/ Info")
    
    st.divider()
    st.markdown("### Painéis Analíticos")
    
    # Adicionámos uma Aba extra para "Séries e Previsibilidade"
    aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs([
        "Perfil (ECA / Género)",
        "Vulnerabilidade Social",
        "Séries e Previsibilidade", # NOVA ABA
        "Geografia Criminológica",
        "Análise Temporal",
        "Foco Investigativo (Pareto)"
    ])
    
    with aba1:
        chart_demografia.render(df_filtrado)
    with aba2:
        chart_vulnerabilidade.render(df_filtrado) 
    with aba3:
        chart_evolucao.render(df_filtrado)
        st.divider()
        chart_probabilidade.render(df_filtrado)
    with aba4:
        chart_mapa.render(df_filtrado)
    with aba5:
        chart_temporal.render(df_filtrado)
    with aba6:
        chart_pareto.render(df_filtrado) 
    
    return df_filtrado
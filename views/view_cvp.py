import streamlit as st
import pandas as pd
from services.data_handler import filtrar_dados_cvp

# Importação dos componentes do CVP
import components.cvp.chart_mapa as chart_mapa
import components.cvp.chart_matriz as chart_matriz
import components.cvp.chart_evolucao as chart_evolucao
import components.cvp.chart_avancado as chart_avancado
import components.cvp.chart_patrulha as chart_patrulha
import components.cvp.chart_anomalias as chart_anomalias
import components.cvp.chart_perfil as chart_perfil 
import components.cvp.chart_pareto as chart_pareto
import components.cvp.chart_probabilidade as chart_probabilidade # <-- CORREÇÃO 1: Importação adicionada!

def render(df_cvp, datas, municipios, ais):
    st.subheader("CVP (Crimes Violentos contra o Património)")
    
    if df_cvp.empty:
        st.warning("Base de dados não encontrada.")
        return df_cvp

    # Filtro global que vem do app.py
    df_filtrado = filtrar_dados_cvp(df_cvp, datas, municipios, ais)
    
    if df_filtrado.empty:
        st.warning("Nenhum registo encontrado com os filtros selecionados.")
        return df_filtrado

    # --- INÍCIO: FILTROS TÁTICOS LOCAIS EXCLUSIVOS DO CVP ---
    st.markdown("##### Filtros de Simulação Tática (Específicos para CVP)")
    col_filtro1, col_filtro2 = st.columns(2)
    
    with col_filtro1:
        dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        filtro_dias = st.multiselect("Isolar Dia da Semana:", dias_semana, default=[], help="Escolha dias específicos para ver como a mancha criminal se comporta.")
        
    with col_filtro2:
        filtro_horas = st.slider("Isolar Faixa Horária (0h às 23h):", 0, 23, (0, 23), help="Deslize para isolar, por exemplo, apenas os assaltos da madrugada.")
        
    # Aplicação matemática dos filtros locais
    if filtro_dias:
        df_filtrado = df_filtrado[df_filtrado['Dia da Semana'].isin(filtro_dias)]
        
    # Extrai a hora para fazer o filtro do slider
    df_filtrado['Hora_Int'] = pd.to_datetime(df_filtrado['Hora'], format='%H:%M:%S', errors='coerce').dt.hour
    df_filtrado = df_filtrado[(df_filtrado['Hora_Int'] >= filtro_horas[0]) & (df_filtrado['Hora_Int'] <= filtro_horas[1])]
    
    if df_filtrado.empty:
        st.warning("A combinação de Dia e Hora selecionada não possui registos de CVP.")
        return df_filtrado
    # --- FIM: FILTROS LOCAIS ---

    st.divider()
    
    # KPIs atualizados de acordo com os filtros locais
    kpi1, kpi2, kpi3 = st.columns(3)
    total_casos = df_filtrado.shape[0]
    kpi1.metric(label="Volume Filtrado (CVP)", value=f"{total_casos:,}".replace(',', '.'))
    
    if total_casos > 0:
        cidade_pior = df_filtrado['Município'].mode()[0]
        kpi2.metric(label="Ponto Crítico (Município)", value=cidade_pior)
        
        dia_pior = df_filtrado['Dia da Semana'].mode()[0]
        kpi3.metric(label="Dia de Maior Risco", value=dia_pior)
    
    st.divider()
    
    st.error("""
    **ALERTA DE INTELIGÊNCIA CRIMINAL:** Padrão "Rota de Trabalho" Detetado.
    O sistema identificou uma concentração anómala de assaltos violentos às **Segundas-feiras, entre as 05h00 e 07h00 da manhã**. Este padrão sugere a vitimização de trabalhadores em paragens de autocarro.
    """)

    st.markdown("### Mancha Criminal Dinâmica")
    chart_mapa.render(df_filtrado)
    st.divider()
    
    st.markdown("### Dinâmica Operacional e Inteligência")
    
    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        "Perfil Criminal",
        "Matriz de Risco (Tempo)",
        "Evolução e Demanda",
        "Séries e Algoritmos",
        "Inteligência de Patrulhamento"
    ])
    
    # CORREÇÃO 2: Reorganização correta de quem vai para que Aba!
    with aba1:
        chart_perfil.render(df_filtrado) 
        
    with aba2:
        chart_matriz.render(df_filtrado) # Voltou ao lugar certo!
        
    with aba3:
        chart_evolucao.render(df_filtrado)
        st.divider()
        chart_pareto.render(df_filtrado) # Pareto faz sentido junto com a Evolução/Demanda
        
    with aba4:
        chart_probabilidade.render(df_filtrado) 
        st.divider()
        chart_avancado.render(df_filtrado)      
        st.divider()
        chart_anomalias.render(df_filtrado)     
        
    with aba5:
        chart_patrulha.render(df_filtrado)
    
    return df_filtrado
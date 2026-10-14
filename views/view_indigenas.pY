import streamlit as st
import pandas as pd
from services.data_handler import filtrar_dados_indigenas

# Reaproveitamento dos componentes demográficos!
import components.sexuais.chart_demografia as chart_demografia
import components.sexuais.chart_vulnerabilidade as chart_vulnerabilidade
import components.sexuais.chart_mapa as chart_mapa
import components.sexuais.chart_temporal as chart_temporal
import components.sexuais.chart_pareto as chart_pareto

def render(df_base, datas, municipios, ais):
    st.subheader("Povos Indígenas (Violência contra Originários)")
    
    with st.popover("Metodologia e Leitura Tática"):
        st.markdown("""
        **Diretrizes de Leitura:**
        Módulo dedicado à análise de violência contra populações indígenas do Ceará.
        
        **Foco Tático e Direitos Humanos:**
        O volume histórico tende a concentrar-se em municípios com reservas reconhecidas (ex: Tapebas em Caucaia, Pitaguary em Maracanaú, Tremembé em Itarema). A análise serve para orientar o Policiamento Comunitário e a articulação com a FUNAI e Secretarias de Direitos Humanos.
        """)
        
    if df_base.empty:
        st.warning("Base de dados não encontrada.")
        return df_base

    df_filtrado = filtrar_dados_indigenas(df_base, datas, municipios, ais)
    
    if df_filtrado.empty:
        st.warning("Nenhum registo encontrado com os filtros selecionados.")
        return df_filtrado

    # --- INÍCIO: FILTROS TÁTICOS (Drill-Down) ---
    st.markdown("##### Filtros de Proteção Social")
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        if 'Gênero' in df_filtrado.columns:
            opcoes_genero = sorted(df_filtrado['Gênero'].dropna().unique())
            filtro_genero = st.multiselect("Isolar Género:", opcoes_genero, default=[])
        else: filtro_genero = []
            
    with col_f2:
        if 'Escolaridade da Vítima' in df_filtrado.columns:
            opcoes_esc = sorted(df_filtrado['Escolaridade da Vítima'].dropna().unique())
            filtro_esc = st.multiselect("Isolar Escolaridade:", opcoes_esc, default=[])
        else: filtro_esc = []
            
    with col_f3:
        if 'Dia da Semana' in df_filtrado.columns:
            dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            filtro_dias = st.multiselect("Isolar Dia:", dias_semana, default=[])
        else: filtro_dias = []
            
    with col_f4:
        filtro_horas = st.slider("Horário (0h-23h):", 0, 23, (0, 23), key="indigena_slider")

    if filtro_genero: df_filtrado = df_filtrado[df_filtrado['Gênero'].isin(filtro_genero)]
    if filtro_esc: df_filtrado = df_filtrado[df_filtrado['Escolaridade da Vítima'].isin(filtro_esc)]
    if filtro_dias: df_filtrado = df_filtrado[df_filtrado['Dia da Semana'].isin(filtro_dias)]
        
    if 'Hora' in df_filtrado.columns:
        df_filtrado['Hora_Int'] = pd.to_datetime(df_filtrado['Hora'], format='%H:%M:%S', errors='coerce').dt.hour
        df_filtrado = df_filtrado[(df_filtrado['Hora_Int'] >= filtro_horas[0]) & (df_filtrado['Hora_Int'] <= filtro_horas[1])]

    if df_filtrado.empty:
        st.warning("Sem dados para esta combinação de filtros.")
        return df_filtrado
    # --- FIM: FILTROS LOCAIS ---

    st.divider()
    kpi1, kpi2, kpi3 = st.columns(3)
    
    total_casos = df_filtrado.shape[0]
    kpi1.metric(label="Volume de Ocorrências", value=f"{total_casos:,}".replace(',', '.'))
    
    if total_casos > 0:
        cidade_pior = df_filtrado['Município'].mode()[0]
        kpi2.metric(label="Município de Maior Incidência", value=cidade_pior)
        
        if 'Idade da Vítima' in df_filtrado.columns:
            idades_numericas = pd.to_numeric(df_filtrado['Idade da Vítima'], errors='coerce')
            idade_med = idades_numericas.median()
            if pd.notna(idade_med):
                kpi3.metric(label="Idade Mediana da Vítima", value=f"{int(idade_med)} anos")
            else:
                kpi3.metric(label="Idade Mediana", value="S/ Info")
    
    st.divider()
    
    # Alerta Inteligente focado em Território
    st.error("""
    **ALERTA DE DIREITOS HUMANOS:** O mapeamento territorial cruza diretamente com áreas de demarcação e presença histórica indígena (ex: Caucaia e Maracanaú). A Polícia Militar deve acionar o policiamento preventivo de proximidade nestas regiões.
    """)

    st.markdown("### Mancha Criminal e Vulnerabilidade")
    
    aba1, aba2, aba3, aba4 = st.tabs([
        "Geografia e Território",
        "Demografia da Vítima",
        "Vulnerabilidade Social",
        "Análise Temporal"
    ])
    
    with aba1:
        chart_mapa.render(df_filtrado)
    with aba2:
        chart_demografia.render(df_filtrado)
    with aba3:
        chart_vulnerabilidade.render(df_filtrado)
    with aba4:
        chart_temporal.render(df_filtrado)
    
    return df_filtrado
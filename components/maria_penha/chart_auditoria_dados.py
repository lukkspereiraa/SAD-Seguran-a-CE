import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def render(df):
    if df.empty: return
    
    with st.popover(":material/policy: Metodologia de Auditoria Pública"):
        st.markdown("""
        **Índice de Qualidade do Registo Policial (Apagão Demográfico):**
        * A ausência de dados sociodemográficos (Idade, Raça, Escolaridade) nos Boletins de Ocorrência prejudica severamente a formulação de políticas públicas.
        * **Valor Tático (Governança):** O SAD audita o próprio trabalho do Estado. Taxas altas de preenchimento "Não Informado" exigem intervenção do Comando nas delegacias para melhorar o protocolo de atendimento e humanização no registo de crimes de Violência Doméstica.
        """)

    st.markdown("#### :material/fact_check: Auditoria de Preenchimento (Dados Ausentes)")
    
    total_linhas = len(df)
    
    # Cálculos dos dados ausentes ou "Não Informados"
    idade_nula = df['Faixa Etária'].apply(lambda x: 1 if pd.isna(x) or str(x).strip() == 'Não Informada' else 0).sum()
    esc_nula = df['Escolaridade da Vítima'].apply(lambda x: 1 if pd.isna(x) or str(x).strip() == 'Não Informada' else 0).sum()
    raca_nula = df['Raça da Vítima'].apply(lambda x: 1 if pd.isna(x) or str(x).strip() == 'Não Informada' else 0).sum()
    
    tx_idade = (idade_nula / total_linhas) * 100
    tx_esc = (esc_nula / total_linhas) * 100
    tx_raca = (raca_nula / total_linhas) * 100
    
    col1, col2, col3 = st.columns(3)
    
    # 1. Indicador de Idade
    with col1:
        cor_idade = "green" if tx_idade < 15 else "orange" if tx_idade < 30 else "red"
        st.metric(
            label="Idade Não Informada", 
            value=f"{tx_idade:.1f}%", 
            delta=f"{idade_nula} registos em branco", 
            delta_color="inverse"
        )
        if tx_idade >= 30: st.error("Crítico: Falha na identificação geracional.")
        
    # 2. Indicador de Escolaridade
    with col2:
        cor_esc = "green" if tx_esc < 15 else "orange" if tx_esc < 30 else "red"
        st.metric(
            label="Escolaridade Não Informada", 
            value=f"{tx_esc:.1f}%", 
            delta=f"{esc_nula} registos em branco",
            delta_color="inverse"
        )
        if tx_esc >= 30: st.error("Crítico: Falha no mapeamento socioeconómico.")
        
    # 3. Indicador de Raça (Este costuma ser o pior)
    with col3:
        cor_raca = "green" if tx_raca < 15 else "orange" if tx_raca < 30 else "red"
        st.metric(
            label="Raça Não Informada", 
            value=f"{tx_raca:.1f}%", 
            delta=f"{raca_nula} registos em branco",
            delta_color="inverse"
        )
        if tx_raca >= 30: st.error("Crítico: Risco de Apagão Demográfico no registo da cor/raça.")

    st.divider()
    
    # Gráfico de Barras de Erro Comparativo
    df_erros = pd.DataFrame({
        'Campo Demográfico': ['Idade da Vítima', 'Escolaridade', 'Raça/Cor'],
        'Taxa de Falha (%)': [tx_idade, tx_esc, tx_raca]
    }).sort_values(by='Taxa de Falha (%)', ascending=True)
    
    fig_auditoria = px.bar(
        df_erros, 
        x='Taxa de Falha (%)', 
        y='Campo Demográfico',
        orientation='h',
        text_auto='.1f',
        title="Impacto do Apagão Demográfico nos Registos (Omissão de Dados)",
        color='Taxa de Falha (%)',
        color_continuous_scale='Reds' # Mantemos o vermelho aqui pois é um Alerta de Gestão
    )
    
    fig_auditoria.add_vline(x=20, line_dash="dot", line_color="black", annotation_text="Limite Tolerável (20%)")
    fig_auditoria.update_traces(textposition="outside")
    fig_auditoria.update_layout(xaxis=dict(range=[0, max(100, df_erros['Taxa de Falha (%)'].max() + 10)]))
    
    st.plotly_chart(fig_auditoria, use_container_width=True)
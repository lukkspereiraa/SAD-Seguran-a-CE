import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    st.markdown("#### :material/fact_check: Auditoria de Registo (Apagão Demográfico)")
    st.info("Crimes de intolerância frequentemente sofrem de dupla omissão: além da subnotificação geral, quando o crime é reportado, a polícia falha em registar aspetos identitários cruciais, como a Raça e a Identidade de Género real da vítima.")
    
    total_linhas = len(df)
    
    raca_nula = df['Raça da Vítima'].apply(lambda x: 1 if pd.isna(x) or str(x).strip() in ['Não Informada', 'Não Informado'] else 0).sum()
    id_nula = df['Identidade de Gênero'].apply(lambda x: 1 if pd.isna(x) or str(x).strip() in ['Não Informada', 'Não Informado'] else 0).sum()
    ori_nula = df['Orientação Sexual'].apply(lambda x: 1 if pd.isna(x) or str(x).strip() in ['Não Informada', 'Não Informado'] else 0).sum()
    
    tx_raca = (raca_nula / total_linhas) * 100
    tx_id = (id_nula / total_linhas) * 100
    tx_ori = (ori_nula / total_linhas) * 100
    
    df_erros = pd.DataFrame({
        'Campo Demográfico': ['Raça/Cor', 'Identidade de Género', 'Orientação Sexual'],
        'Taxa de Falha (%)': [tx_raca, tx_id, tx_ori]
    }).sort_values(by='Taxa de Falha (%)', ascending=True)
    
    fig_auditoria = px.bar(
        df_erros, 
        x='Taxa de Falha (%)', 
        y='Campo Demográfico',
        orientation='h',
        text_auto='.1f',
        title="Omissão de Dados no Registo Policial",
        color='Taxa de Falha (%)',
        color_continuous_scale='Reds'
    )
    
    fig_auditoria.add_vline(x=20, line_dash="dot", line_color="black", annotation_text="Limite Tolerável (20%)")
    fig_auditoria.update_traces(textposition="outside")
    fig_auditoria.update_layout(xaxis=dict(range=[0, max(100, df_erros['Taxa de Falha (%)'].max() + 10)]))
    
    st.plotly_chart(fig_auditoria, use_container_width=True)
import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    st.markdown("#### :material/fact_check: Auditoria de Registo Policial")
    st.error("Alerta Crítico: Num crime tipificado por preconceito de raça/cor, omitir a raça da vítima no B.O. impede análises estruturais e mascaram a realidade social.")
    
    total = len(df)
    raca_nula = df['Raça da Vítima'].apply(lambda x: 1 if pd.isna(x) or str(x).strip() in ['Não Informada', 'Não Informado'] else 0).sum()
    esc_nula = df['Escolaridade da Vítima'].apply(lambda x: 1 if pd.isna(x) or str(x).strip() in ['Não Informada', 'Não Informado'] else 0).sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Raça Omitida no B.O.", f"{(raca_nula/total)*100:.1f}%", f"{raca_nula} registos em branco", delta_color="inverse")
    with col2:
        st.metric("Escolaridade Omitida", f"{(esc_nula/total)*100:.1f}%", f"{esc_nula} registos em branco", delta_color="inverse")
        
    df_erros = pd.DataFrame({
        'Campo Demográfico': ['Raça/Cor', 'Escolaridade'],
        'Taxa de Falha (%)': [(raca_nula/total)*100, (esc_nula/total)*100]
    }).sort_values(by='Taxa de Falha (%)', ascending=True)
    
    fig_auditoria = px.bar(
        df_erros, x='Taxa de Falha (%)', y='Campo Demográfico', orientation='h', text_auto='.1f',
        title="Impacto do Apagão Demográfico nos Registos", color='Taxa de Falha (%)', color_continuous_scale='Reds'
    )
    fig_auditoria.add_vline(x=20, line_dash="dot", line_color="black", annotation_text="Limite Tolerável (20%)")
    fig_auditoria.update_layout(xaxis=dict(range=[0, max(100, df_erros['Taxa de Falha (%)'].max() + 10)]))
    st.plotly_chart(fig_auditoria, use_container_width=True)
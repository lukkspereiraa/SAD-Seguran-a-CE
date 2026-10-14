import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'Data' not in df.columns: return

    st.markdown("#### Deteção Algorítmica de Anomalias (Z-Score)")
    
    df_diario = df.groupby(df['Data'].dt.date).size().reset_index(name='Casos')
    df_diario['Data'] = pd.to_datetime(df_diario['Data'])

    if len(df_diario) < 2: return

    media = df_diario['Casos'].mean()
    desvio_padrao = df_diario['Casos'].std()
    limite_tolerancia = media + (2 * desvio_padrao)
    
    df_diario['Anomalia'] = df_diario['Casos'] > limite_tolerancia
    df_diario['Classificação'] = df_diario['Anomalia'].map({True: 'Alerta Crítico (Outlier)', False: 'Volume Normal'})

    fig = px.scatter(
        df_diario, x='Data', y='Casos', color='Classificação',
        color_discrete_map={'Alerta Crítico (Outlier)': '#67000D', 'Volume Normal': '#FC9272'},
        title="Mapeamento de Picos Anormais de CVP"
    )

    fig.add_hline(y=media, line_dash="dash", line_color="gray", annotation_text="Média Histórica")
    fig.add_hline(y=limite_tolerancia, line_dash="dot", line_color="red", annotation_text="Teto Estatístico (Z-Score > 2)")

    fig.update_traces(marker=dict(size=7), selector=dict(name='Volume Normal'))
    fig.update_traces(marker=dict(size=12, symbol='x'), selector=dict(name='Alerta Crítico (Outlier)'))

    st.plotly_chart(fig, use_container_width=True)

    total_anomalias = df_diario['Anomalia'].sum()
    if total_anomalias > 0:
        st.error(f"Auditoria Necessária: Detetado(s) {total_anomalias} dia(s) com volume de roubos estatisticamente anormal.")
    else:
        st.success("O volume de roubos manteve-se dentro do limite estatístico.")
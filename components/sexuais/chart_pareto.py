import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render(df):
    if df.empty or 'AIS' not in df.columns: return
    
    st.markdown("#### Foco Investigativo (Teorema de Pareto 80/20)")
    st.info("Estratégia de Polícia Judiciária: Crimes contra a dignidade sexual exigem investigação especializada. O gráfico identifica quais as Áreas Integradas de Segurança (AIS) que necessitam de priorização imediata para instalação ou reforço de Delegacias de Defesa da Mulher (DDM) ou de Proteção à Criança (DCA).")
    
    df_pareto = df['AIS'].value_counts().reset_index()
    df_pareto.columns = ['AIS', 'Ocorrências']
    df_pareto = df_pareto[df_pareto['AIS'].str.contains('AIS', na=False, case=False)]
    df_pareto = df_pareto.sort_values(by='Ocorrências', ascending=False)
    
    if df_pareto.empty: return
    
    df_pareto['Acumulado'] = df_pareto['Ocorrências'].cumsum()
    df_pareto['% Acumulado'] = (df_pareto['Acumulado'] / df_pareto['Ocorrências'].sum()) * 100
    df_pareto_top = df_pareto.head(15)
    
    fig = go.Figure()
    
    # Eixo Y1: Barras
    fig.add_trace(go.Bar(
        x=df_pareto_top['AIS'], y=df_pareto_top['Ocorrências'],
        name='Volume de Denúncias', marker_color='#DF65B0' 
    ))
    
    # Eixo Y2: Linha Acumulada
    fig.add_trace(go.Scatter(
        x=df_pareto_top['AIS'], y=df_pareto_top['% Acumulado'],
        name='% Acumulado', yaxis='y2', 
        line=dict(color='#980043', width=4), mode='lines+markers'
    ))
    
    fig.update_layout(
        title="Curva de Concentração de Inquéritos por Batalhão (AIS)",
        yaxis=dict(title='Volume de Denúncias'),
        yaxis2=dict(title='% Acumulado', overlaying='y', side='right', range=[0, 105]),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        margin=dict(t=60, b=0, l=0, r=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
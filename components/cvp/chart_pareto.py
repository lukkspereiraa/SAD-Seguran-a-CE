import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render(df):
    if df.empty or 'AIS' not in df.columns: return
    
    st.markdown("#### Teorema de Pareto (Regra 80/20)")
    st.info("Foco Operacional e Otimização de Recursos: O gráfico de Pareto identifica quais Batalhões (AIS) concentram a maior parte dos assaltos. Ao focar o patrulhamento nas áreas que geram mais problemas, a Polícia otimiza recursos e reduz custos.")
    
    # Conta os casos por AIS
    df_pareto = df['AIS'].value_counts().reset_index()
    df_pareto.columns = ['AIS', 'Ocorrências']
    
    # Remove as linhas sem AIS preenchida adequadamente
    df_pareto = df_pareto[df_pareto['AIS'].str.contains('AIS', na=False, case=False)]
    
    # Ordena do maior para o menor
    df_pareto = df_pareto.sort_values(by='Ocorrências', ascending=False)
    
    if df_pareto.empty: return
    
    # Matemática do Pareto: Cálculo do Acumulado
    df_pareto['Acumulado'] = df_pareto['Ocorrências'].cumsum()
    df_pareto['% Acumulado'] = (df_pareto['Acumulado'] / df_pareto['Ocorrências'].sum()) * 100
    
    # Limitar ao Top 15 Batalhões para manter o gráfico limpo e executivo
    df_pareto_top = df_pareto.head(15)
    
    # Criação do Gráfico de Duplo Eixo (Plotly Graph Objects)
    fig = go.Figure()
    
    # Eixo Y1: Barras (Volume Absoluto)
    fig.add_trace(go.Bar(
        x=df_pareto_top['AIS'], 
        y=df_pareto_top['Ocorrências'],
        name='Volume de Roubos', 
        marker_color='#FC9272' # Vermelho suave
    ))
    
    # Eixo Y2: Linha (Percentagem Acumulada)
    fig.add_trace(go.Scatter(
        x=df_pareto_top['AIS'], 
        y=df_pareto_top['% Acumulado'],
        name='% Acumulado', 
        yaxis='y2', 
        line=dict(color='#67000D', width=4), # Vermelho muito escuro
        mode='lines+markers'
    ))
    
    # Configuração dos eixos sobrepostos
    fig.update_layout(
        title="Curva de Pareto - Concentração de CVP por Batalhão (AIS)",
        yaxis=dict(title='Volume de Roubos'),
        yaxis2=dict(title='% Acumulado', overlaying='y', side='right', range=[0, 105]),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
        margin=dict(t=60, b=0, l=0, r=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Algoritmo de Inteligência: Avalia se os primeiros batalhões já somam um valor muito alto
    atingiu_critico = df_pareto_top[df_pareto_top['% Acumulado'] >= 50]
    if not atingiu_critico.empty:
        qtd_ais = atingiu_critico.index[0] + 1
        st.success(f"**Estratégia Preditiva:** Apenas **{qtd_ais} Batalhões (AIS)** são responsáveis por **metade (50%)** de todos os roubos do filtro selecionado. Direcionar equipas especializadas (como o RAIO ou COTAM) unicamente para estas {qtd_ais} áreas trará a maior redução criminal do estado com o menor esforço logístico.")
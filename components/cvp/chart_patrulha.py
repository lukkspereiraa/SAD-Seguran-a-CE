import streamlit as st
import plotly.express as px
import pandas as pd

def classificar_turno(hora_str):
    try:
        h = int(str(hora_str).split(':')[0])
        if 0 <= h < 6: return '1. Madrugada (00h-06h)'
        elif 6 <= h < 12: return '2. Manhã (06h-12h)'
        elif 12 <= h < 18: return '3. Tarde (12h-18h)'
        else: return '4. Noite (18h-00h)'
    except: return 'Não Informado'

def render(df):
    if df.empty: return
    
    st.markdown("#### Matriz de Alocação de Viaturas (Espaço x Tempo)")
    
    df_turno = df.copy()
    df_turno['Turno'] = df_turno['Hora'].apply(classificar_turno)
    df_cross = pd.crosstab(df_turno['AIS'], df_turno['Turno'])
    
    top_ais = df_turno['AIS'].value_counts().head(15).index
    df_cross_top = df_cross.loc[top_ais]
    df_cross_top['Total'] = df_cross_top.sum(axis=1)
    df_cross_top = df_cross_top.sort_values('Total', ascending=True).drop(columns=['Total'])
    
    fig_heat = px.imshow(
        df_cross_top, labels=dict(x="Turnos Policiais", y="Batalhões (Top 15 AIS)", color="Concentração de Roubos"),
        x=df_cross_top.columns, y=df_cross_top.index, color_continuous_scale="Reds", aspect="auto", text_auto=True
    )
    fig_heat.update_xaxes(side="top")
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.divider()
    st.markdown("#### Velocímetro Criminal (CVP)")
    if 'Data' in df.columns and not df.empty:
        df['Data'] = pd.to_datetime(df['Data'])
        dias_totais = (df['Data'].max() - df['Data'].min()).days
        if dias_totais > 0:
            furtos_por_dia = len(df) / dias_totais
            minutos_por_furto = (24 * 60) / furtos_por_dia
            
            col1, col2 = st.columns(2)
            with col1: st.metric("Taxa Diária", f"{int(furtos_por_dia)} roubos / dia", "Impacto Estadual", delta_color="inverse")
            with col2: st.metric("Frequência", f"1 roubo a cada {int(minutos_por_furto)} minutos", "Velocidade da Violência", delta_color="inverse")
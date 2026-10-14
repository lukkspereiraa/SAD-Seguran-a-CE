import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'Hora' not in df.columns: return
    
    st.markdown("#### Matriz de Registo (Horário da Denúncia)")
    st.info("Atenção Tática: Diferente dos crimes de rua, o pico matutino/comercial nos crimes sexuais reflete frequentemente o momento em que a vítima ou responsáveis procuram a delegacia ou rede de apoio, e não o momento da agressão.")
    
    df_temp = df.copy()
    df_temp['Hora_Pico'] = pd.to_datetime(df_temp['Hora'], format='%H:%M:%S', errors='coerce').dt.hour
    df_heatmap = df_temp.groupby(['Dia da Semana', 'Hora_Pico']).size().reset_index(name='Volume')
    df_heatmap = df_heatmap.dropna().sort_values('Hora_Pico')
    df_heatmap['Hora_Pico'] = df_heatmap['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
    
    fig_heat = px.density_heatmap(
        df_heatmap, x='Hora_Pico', y='Dia da Semana', z='Volume',
        color_continuous_scale='PuRd', title='Concentração Temporal de Registos'
    )
    
    ordem_dias = ['Domingo', 'Sábado', 'Sexta', 'Quinta', 'Quarta', 'Terça', 'Segunda']
    fig_heat.update_yaxes(categoryorder='array', categoryarray=ordem_dias)
    st.plotly_chart(fig_heat, use_container_width=True)
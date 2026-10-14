import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'Hora_Pico' not in df.columns: return
    
    st.markdown("#### :material/calendar_clock: Matriz de Risco (Dias vs Horas)")
    st.info("Padrão Identificado: Os furtos concentram-se fortemente durante os finais de semana e no período diurno (especialmente aos domingos às 10h), sugerindo furtos em zonas de comércio, mercados e eventos públicos.")
    
    df_heatmap = df.groupby(['Dia da Semana', 'Hora_Pico']).size().reset_index(name='Volume')
    df_heatmap['Hora_Pico'] = pd.to_numeric(df_heatmap['Hora_Pico'], errors='coerce')
    df_heatmap = df_heatmap.dropna().sort_values('Hora_Pico')
    df_heatmap['Hora_Pico'] = df_heatmap['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
    
    fig_heat = px.density_heatmap(
        df_heatmap, x='Hora_Pico', y='Dia da Semana', z='Volume',
        color_continuous_scale='Blues', title='Concentração Temporal de Furtos'
    )
    
    ordem_dias = ['Domingo', 'Sábado', 'Sexta', 'Quinta', 'Quarta', 'Terça', 'Segunda']
    fig_heat.update_yaxes(categoryorder='array', categoryarray=ordem_dias)
    st.plotly_chart(fig_heat, use_container_width=True)
import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'Hora_Pico' not in df.columns: return
    
    st.markdown("#### :material/calendar_clock: Mapa de Calor Temporal")
    st.info("Quanto mais escuro o bloco (tons de vermelho), maior é a incidência de crimes de ódio naquele horário específico.")
    
    df_heatmap = df.groupby(['Dia da Semana', 'Hora_Pico']).size().reset_index(name='Ocorrências')
    
    df_heatmap['Hora_Pico'] = pd.to_numeric(df_heatmap['Hora_Pico'], errors='coerce')
    df_heatmap = df_heatmap.dropna(subset=['Hora_Pico']).sort_values('Hora_Pico')
    df_heatmap['Hora_Pico'] = df_heatmap['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
    
    fig_heat = px.density_heatmap(
        df_heatmap, 
        x='Hora_Pico', 
        y='Dia da Semana', 
        z='Ocorrências',
        color_continuous_scale='YlOrRd', # Alterado para Amarelo->Laranja->Vermelho (muito mais claro de ler)
        title='Horários Críticos para Crimes de Ódio'
    )
    
    ordem_dias = ['Domingo', 'Sábado', 'Sexta', 'Quinta', 'Quarta', 'Terça', 'Segunda']
    fig_heat.update_yaxes(categoryorder='array', categoryarray=ordem_dias)
    
    st.plotly_chart(fig_heat, use_container_width=True)
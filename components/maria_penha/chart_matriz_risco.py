import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'Hora_Pico' not in df.columns: return
    
    with st.popover(":material/help: Metodologia da Matriz"):
        st.markdown("""
        **Padrão Comportamental do Agressor:**
        Ao contrário de crimes patrimoniais (roubo) que ocorrem mais em dias úteis, a violência doméstica costuma apresentar **picos nos finais de semana (Sábado à noite e Domingo)**, períodos em que agressor e vítima passam mais tempo confinados na mesma residência.
        """)
    
    df_heatmap = df.groupby(['Dia da Semana', 'Hora_Pico']).size().reset_index(name='Ocorrências')
    
    df_heatmap['Hora_Pico'] = pd.to_numeric(df_heatmap['Hora_Pico'], errors='coerce')
    df_heatmap = df_heatmap.dropna(subset=['Hora_Pico']).sort_values('Hora_Pico')
    df_heatmap['Hora_Pico'] = df_heatmap['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
    
    fig_heat = px.density_heatmap(
        df_heatmap, 
        x='Hora_Pico', 
        y='Dia da Semana', 
        z='Ocorrências',
        color_continuous_scale='Purples',
        title='Mapa de Calor: Ocorrências por Dia e Hora'
    )
    
    ordem_dias = ['Domingo', 'Sábado', 'Sexta', 'Quinta', 'Quarta', 'Terça', 'Segunda']
    fig_heat.update_yaxes(categoryorder='array', categoryarray=ordem_dias)
    
    st.plotly_chart(fig_heat, use_container_width=True)
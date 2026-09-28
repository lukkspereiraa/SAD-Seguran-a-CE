import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    with st.popover(":material/help: Metodologia e Leitura"):
        st.markdown("""
        **Matriz de Concentração Criminal (Heatmap):**
        * O gráfico cruza os dias da semana com as horas do dia (00h às 23h).
        * **Tons de Verde Escuro:** Indicam horários críticos com altíssima incidência de ocorrências de tráfico. Ideal para direcionar patrulhamento tático/preventivo.
        * **Tons Claros/Branco:** Baixa incidência ou ausência de registros policiais no cruzamento.
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
        color_continuous_scale='Greens',
        title='Heatmap: Ocorrências de Tráfico por Dia e Horário'
    )
    
    ordem_dias = ['Domingo', 'Sábado', 'Sexta', 'Quinta', 'Quarta', 'Terça', 'Segunda']
    fig_heat.update_yaxes(categoryorder='array', categoryarray=ordem_dias)
    
    st.plotly_chart(fig_heat, use_container_width=True)
import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'Hora_Pico' not in df.columns: return
    
    with st.popover(":material/help: Metodologia e Leitura"):
        st.markdown("""
        **Matriz de Circulação Bélica (Heatmap):**
        * O gráfico cruza os dias da semana com as horas do dia (00h às 23h).
        * **Tons de Vermelho Escuro:** Indicam os horários em que a polícia mais intercepta armas de fogo em circulação.
        * **Valor Tático:** Orienta a montagem de blitzes e barreiras policiais focadas em desarmamento nos horários de maior fluxo criminoso.
        """)
    
    # Soma a quantidade de armas pelo cruzamento de Dia e Hora
    df_heatmap = df.groupby(['Dia da Semana', 'Hora_Pico'])['Quantidade'].sum().reset_index(name='Total de Armas')
    
    df_heatmap['Hora_Pico'] = pd.to_numeric(df_heatmap['Hora_Pico'], errors='coerce')
    df_heatmap = df_heatmap.dropna(subset=['Hora_Pico']).sort_values('Hora_Pico')
    df_heatmap['Hora_Pico'] = df_heatmap['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
    
    fig_heat = px.density_heatmap(
        df_heatmap, 
        x='Hora_Pico', 
        y='Dia da Semana', 
        z='Total de Armas',
        color_continuous_scale='Reds',
        title='Heatmap: Apreensão de Armas por Dia e Horário'
    )
    
    ordem_dias = ['Domingo', 'Sábado', 'Sexta', 'Quinta', 'Quarta', 'Terça', 'Segunda']
    fig_heat.update_yaxes(categoryorder='array', categoryarray=ordem_dias)
    
    st.plotly_chart(fig_heat, use_container_width=True)
import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'Hora' not in df.columns: return
    
    col1, col2 = st.columns(2)
    df_temp = df.copy()
    df_temp['Hora_Pico'] = pd.to_datetime(df_temp['Hora'], format='%H:%M:%S', errors='coerce').dt.hour
    
    with col1:
        st.markdown("#### Matriz de Risco (Dia x Hora)")
        df_heatmap = df_temp.groupby(['Dia da Semana', 'Hora_Pico']).size().reset_index(name='Volume')
        df_heatmap = df_heatmap.dropna().sort_values('Hora_Pico')
        df_heatmap['Hora_Pico'] = df_heatmap['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
        
        fig_heat = px.density_heatmap(
            df_heatmap, x='Hora_Pico', y='Dia da Semana', z='Volume',
            color_continuous_scale='Oranges', title='Concentração de Combate a Incêndios'
        )
        ordem_dias = ['Domingo', 'Sábado', 'Sexta', 'Quinta', 'Quarta', 'Terça', 'Segunda']
        fig_heat.update_yaxes(categoryorder='array', categoryarray=ordem_dias)
        st.plotly_chart(fig_heat, use_container_width=True)

    with col2:
        st.markdown("#### Relógio de Fogo (Radar 24h)")
        df_hora = df_temp.groupby('Hora_Pico').size().reset_index(name='Ocorrências')
        df_hora = df_hora.dropna().sort_values('Hora_Pico')
        df_hora['Hora (Texto)'] = df_hora['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
        
        if not df_hora.empty:
            df_radar = pd.concat([df_hora, df_hora.iloc[[0]]], ignore_index=True)
            fig_radar = px.line_polar(df_radar, r='Ocorrências', theta='Hora (Texto)', line_close=True, markers=True)
            # Laranja Escuro
            fig_radar.update_traces(fill='toself', line_color='#E6550D', fillcolor='rgba(230, 85, 13, 0.4)')
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)))
            st.plotly_chart(fig_radar, use_container_width=True)
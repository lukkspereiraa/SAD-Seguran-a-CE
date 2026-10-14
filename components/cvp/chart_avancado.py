import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render(df):
    if df.empty: return
    
    st.markdown("#### Ciência de Dados Aplicada (Previsibilidade)")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Filtro de Ruído (Média Móvel 7 Dias)")
        df_serie = df.groupby(df['Data'].dt.date).size().reset_index(name='Casos')
        df_serie['Data'] = pd.to_datetime(df_serie['Data'])
        df_serie = df_serie.sort_values('Data')
        df_serie['Média Móvel'] = df_serie['Casos'].rolling(window=7).mean()
        
        fig_tend = go.Figure()
        fig_tend.add_trace(go.Bar(x=df_serie['Data'], y=df_serie['Casos'], name='Roubos Reais', marker_color='#FC9272', opacity=0.5))
        fig_tend.add_trace(go.Scatter(x=df_serie['Data'], y=df_serie['Média Móvel'], mode='lines', name='Tendência (MM 7D)', line=dict(color='#CB181D', width=3)))
        fig_tend.update_layout(hovermode="x unified", legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        st.plotly_chart(fig_tend, use_container_width=True)

    with col2:
        st.markdown("##### Radar Tático (Relógio Criminal 24h)")
        if 'Hora_Pico' in df.columns:
            df_hora = df.groupby('Hora_Pico').size().reset_index(name='Ocorrências')
            df_hora['Hora_Pico'] = pd.to_numeric(df_hora['Hora_Pico'], errors='coerce')
            df_hora = df_hora.dropna().sort_values('Hora_Pico')
            df_hora['Hora (Texto)'] = df_hora['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
            
            if not df_hora.empty:
                df_radar = pd.concat([df_hora, df_hora.iloc[[0]]], ignore_index=True)
                fig_radar = px.line_polar(df_radar, r='Ocorrências', theta='Hora (Texto)', line_close=True, markers=True)
                fig_radar.update_traces(fill='toself', line_color='#CB181D', fillcolor='rgba(203, 24, 29, 0.4)')
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)))
                st.plotly_chart(fig_radar, use_container_width=True)
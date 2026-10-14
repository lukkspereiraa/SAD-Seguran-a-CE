import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render(df):
    if df.empty: return
    
    st.markdown("#### :material/psychology: Ciência de Dados Aplicada (Previsibilidade)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### :material/ssid_chart: Filtro de Ruído (Média Móvel 7 Dias)")
        st.info("A Linha de Tendência suaviza os picos do fim de semana, revelando se a curva criminal real está a crescer ou a ser controlada pela polícia.")
        
        # Agrupa os crimes dia a dia
        df_serie = df.groupby(df['Data'].dt.date).size().reset_index(name='Casos')
        df_serie['Data'] = pd.to_datetime(df_serie['Data'])
        df_serie = df_serie.sort_values('Data')
        
        # Cálculo da Média Móvel (Algoritmo Financeiro aplicado ao crime)
        df_serie['Média Móvel'] = df_serie['Casos'].rolling(window=7).mean()
        
        fig_tend = go.Figure()
        # Barras diárias (fracas)
        fig_tend.add_trace(go.Bar(x=df_serie['Data'], y=df_serie['Casos'], name='Ocorrências Reais', marker_color='#9ECAE1', opacity=0.5))
        # Linha de tendência (forte)
        fig_tend.add_trace(go.Scatter(x=df_serie['Data'], y=df_serie['Média Móvel'], mode='lines', name='Tendência (MM 7D)', line=dict(color='#08519C', width=3)))
        
        fig_tend.update_layout(hovermode="x unified", legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        st.plotly_chart(fig_tend, use_container_width=True)

    with col2:
        st.markdown("##### :material/radar: Radar Tático (Relógio Criminal 24h)")
        if 'Hora_Pico' in df.columns:
            # Agrupa os crimes por cada hora do dia
            df_hora = df.groupby('Hora_Pico').size().reset_index(name='Ocorrências')
            df_hora['Hora_Pico'] = pd.to_numeric(df_hora['Hora_Pico'], errors='coerce')
            df_hora = df_hora.dropna().sort_values('Hora_Pico')
            df_hora['Hora (Texto)'] = df_hora['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
            
            # Para o radar fechar o círculo perfeitamente, o último ponto deve ligar-se ao primeiro
            if not df_hora.empty:
                df_radar = pd.concat([df_hora, df_hora.iloc[[0]]], ignore_index=True)
                
                fig_radar = px.line_polar(
                    df_radar, r='Ocorrências', theta='Hora (Texto)', line_close=True,
                    markers=True
                )
                fig_radar.update_traces(fill='toself', line_color='#3182BD', fillcolor='rgba(49, 130, 189, 0.4)')
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)))
                st.plotly_chart(fig_radar, use_container_width=True)
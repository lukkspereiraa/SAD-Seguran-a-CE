import streamlit as st
import plotly.express as px
import pandas as pd

def classificar_turno(hora_str):
    try:
        h = int(hora_str)
        if 0 <= h < 6: return '1. Madrugada (00h-06h)'
        elif 6 <= h < 12: return '2. Manhã (06h-12h)'
        elif 12 <= h < 18: return '3. Tarde (12h-18h)'
        else: return '4. Noite (18h-00h)'
    except:
        return 'Não Informado'

def render(df):
    if df.empty: return
    
    st.markdown("#### :material/local_police: Planeamento Operacional (AIS e Turnos)")
    st.info("Painel desenhado para a gestão de efetivo: identifica qual é o Batalhão (AIS) com maior mancha criminal e qual o turno com maior probabilidade de ocorrência.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Ranking Operacional por AIS
        if 'AIS' in df.columns:
            df_ais = df['AIS'].value_counts().reset_index()
            df_ais.columns = ['Área Integrada (AIS)', 'Ocorrências']
            df_ais = df_ais.head(10) # Top 10 AIS mais críticas
            
            fig_ais = px.bar(
                df_ais, x='Ocorrências', y='Área Integrada (AIS)', orientation='h',
                title="Top 10 Batalhões (AIS) com Maior Demanda",
                color='Ocorrências', color_continuous_scale='Reds'
            )
            fig_ais.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_ais, use_container_width=True)

    with col2:
        # Alocação de Efetivo por Turnos
        if 'Hora_Pico' in df.columns:
            # Cria a coluna de turno
            df_turno = df.copy()
            df_turno['Turno Policial'] = df_turno['Hora_Pico'].apply(classificar_turno)
            
            df_t = df_turno['Turno Policial'].value_counts().reset_index()
            df_t.columns = ['Turno Policial', 'Volume']
            df_t = df_t.sort_values('Turno Policial')
            
            fig_turno = px.pie(
                df_t, values='Volume', names='Turno Policial', hole=0.5,
                title="Distribuição por Turnos de Patrulha",
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            st.plotly_chart(fig_turno, use_container_width=True)
            
    st.divider()
    
    # Análise Sociológica de Acesso à Justiça
    st.markdown("#### :material/gavel: Índice de Acesso à Justiça (Viés de Escolaridade)")
    st.warning("Se o gráfico abaixo revelar uma predominância de vítimas com Ensino Médio ou Superior, há um forte indício de **subnotificação na base da pirâmide social**. Pessoas com baixa escolaridade podem estar a sofrer racismo sem conseguir formalizar a queixa por falta de acesso à informação ou medo do sistema de justiça.")
    
    if 'Escolaridade da Vítima' in df.columns:
        df_esc = df['Escolaridade da Vítima'].value_counts().reset_index()
        df_esc.columns = ['Grau de Instrução', 'Volume de Denúncias']
        
        fig_esc2 = px.bar(
            df_esc, x='Grau de Instrução', y='Volume de Denúncias',
            color='Volume de Denúncias', color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig_esc2, use_container_width=True)
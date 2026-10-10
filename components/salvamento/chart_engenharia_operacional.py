import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render(df):
    # Verificação de segurança
    if df.empty or 'Data' not in df.columns or 'Hora' not in df.columns: 
        return
        
    with st.popover(":material/help: Metodologia da Engenharia Operacional"):
        st.markdown("""
        **1. Relógio de Resgate:** Calcula o intervalo médio exato (em minutos) entre cada acionamento das viaturas.
        **2. Carga por Plantão:** Divide as 24h nos 4 turnos clássicos da Segurança Pública (Madrugada, Manhã, Tarde, Noite).
        **3. Detector de Crise (Outliers):** Identifica dias em que o volume de chamados ultrapassou o limite crítico de segurança matemática (**Média + 2 Desvios Padrões**), indicando possíveis calamidades, temporais ou grandes acidentes.
        """)
        
    # ==========================================
    # 1. RELÓGIO DE RESGATE (Gráfico de Velocímetro)
    # ==========================================
    total_chamados = len(df)
    dias_no_periodo = (df['Data'].max() - df['Data'].min()).days
    dias_no_periodo = dias_no_periodo if dias_no_periodo > 0 else 1 # Evita divisão por zero
    minutos_totais = dias_no_periodo * 24 * 60
    
    frequencia_minutos = minutos_totais / total_chamados if total_chamados > 0 else 0
    
    st.markdown("### :material/timer: O Relógio de Resgate")
    
    col_relogio_1, col_relogio_2 = st.columns([1, 2])
    
    with col_relogio_1:
        # Gráfico de Velocímetro (Gauge)
        limite_max = max(60, frequencia_minutos + 10)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = frequencia_minutos,
            number = {'suffix': " min", 'font': {'size': 36, 'color': '#8B0000'}},
            title = {'text': "Intervalo entre Chamados", 'font': {'size': 16}},
            gauge = {
                'axis': {'range': [0, limite_max], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#8B0000"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 15], 'color': "#ffcccb"}, # Vermelho claro (zona crítica, chamados muito rápidos)
                    {'range': [15, limite_max], 'color': "#e0f3ff"} # Azul claro (zona normal)
                ]
            }
        ))
        fig_gauge.update_layout(height=220, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    with col_relogio_2:
        st.write("") # Espaçamento
        st.write("")
        st.error(f"**Frequência Operacional Crítica:**\n\nNeste período selecionado, a central de operações registou um volume tão intenso que as viaturas de resgate e salvamento foram acionadas, em média, **1 vez a cada {frequencia_minutos:.0f} minutos**. Este ritmo ininterrupto justifica a necessidade de reavaliação de efetivo e frota disponível.")
        
    st.divider()

    # Dividimos a tela para os próximos dois gráficos
    col1, col2 = st.columns(2)
    
    # ==========================================
    # 2. CARGA POR PLANTÃO (Turnos de Serviço)
    # ==========================================
    with col1:
        st.markdown("#### :material/work_history: Sobrecarga por Plantão")
        
        df_turnos = df.copy()
        # Converte a hora para numérico para facilitar a separação
        df_turnos['Hora_Int'] = df_turnos['Hora'].astype(str).str.split(':').str[0].astype(float)
        
        def classificar_turno(h):
            if pd.isna(h): return 'Não Informado'
            if 0 <= h < 6: return '1. Madrugada (00h-05h59)'
            elif 6 <= h < 12: return '2. Manhã (06h-11h59)'
            elif 12 <= h < 18: return '3. Tarde (12h-17h59)'
            else: return '4. Noite (18h-23h59)'
            
        df_turnos['Turno'] = df_turnos['Hora_Int'].apply(classificar_turno)
        df_grupo_turnos = df_turnos.groupby('Turno').size().reset_index(name='Chamados')
        
        fig_turnos = px.bar(
            df_grupo_turnos, 
            x='Turno', 
            y='Chamados',
            color='Turno',
            color_discrete_sequence=px.colors.sequential.Blues_r,
            title="Volume de Ocorrências por Turno de 6 Horas",
            text_auto=True
        )
        fig_turnos.update_layout(showlegend=False)
        st.plotly_chart(fig_turnos, use_container_width=True)
        
    # ==========================================
    # 3. DETECTOR DE DIAS DE CRISE (Outliers)
    # ==========================================
    with col2:
        st.markdown("#### :material/warning: Detector de Crises Diárias")
        
        # Conta as ocorrências dia por dia
        df_dias = df.groupby(df['Data'].dt.date).size().reset_index(name='Chamados')
        
        # Matemática Estatística Crítica
        media_dias = df_dias['Chamados'].mean()
        std_dias = df_dias['Chamados'].std()
        limite_critico = media_dias + (2 * std_dias) # Regra dos 2 sigmas para outliers
        
        df_dias['Status'] = df_dias['Chamados'].apply(
            lambda x: 'Crise/Pico Anormal' if x > limite_critico else 'Rotina Operacional'
        )
        
        fig_crise = px.scatter(
            df_dias, 
            x='Data', 
            y='Chamados',
            color='Status',
            color_discrete_map={'Rotina Operacional': '#6BAED6', 'Crise/Pico Anormal': '#CB181D'},
            title="Série Histórica e Limite de Calamidade"
        )
        
        # Desenha as linhas de segurança e limite no gráfico
        fig_crise.add_hline(y=limite_critico, line_dash="dot", line_color="red", annotation_text="Limite Crítico", annotation_position="top right")
        fig_crise.add_hline(y=media_dias, line_dash="dash", line_color="gray", annotation_text="Média Diária", annotation_position="bottom right")
        
        fig_crise.update_traces(marker=dict(size=9, opacity=0.8, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_crise, use_container_width=True)
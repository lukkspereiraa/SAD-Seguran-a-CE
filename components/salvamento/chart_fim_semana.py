import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'Data' not in df.columns: 
        return
        
    with st.popover(":material/help: Metodologia e Leitura (Fator Fim de Semana)"):
        st.markdown("""
        **Análise de Sobrecarga Operacional (Dias Úteis x Fim de Semana):**
        * **Engenharia de Dados:** O sistema agrupa todos os registros por data exata, identifica se o dia foi útil (Seg-Sex) ou fim de semana (Sáb-Dom), e calcula a **Média Diária** de chamados de cada grupo.
        * **Valor Tático:** Prova estatisticamente o aumento da demanda nos finais de semana. Um delta percentual alto justifica matematicamente o empenho de efetivo extra (IRSO) e reforço de viaturas de resgate para sábados e domingos.
        """)
        
    # 1. Agrupa os dados por dia exato para calcular a média real de chamados por dia
    df_dias = df.groupby(df['Data'].dt.date).size().reset_index(name='Chamados')
    df_dias['Data'] = pd.to_datetime(df_dias['Data'])
    
    # 2. Classifica: 0 a 4 = Segunda a Sexta / 5 e 6 = Sábado e Domingo
    df_dias['Tipo de Dia'] = df_dias['Data'].dt.dayofweek.apply(
        lambda x: 'Final de Semana (Sáb-Dom)' if x >= 5 else 'Dias Úteis (Seg-Sex)'
    )
    
    # 3. Calcula as médias
    df_medias = df_dias.groupby('Tipo de Dia')['Chamados'].mean().reset_index()
    df_medias['Chamados'] = df_medias['Chamados'].round(1)
    
    if df_medias.empty: return
    
    # 4. Prepara os KPIs
    media_util = df_medias[df_medias['Tipo de Dia'] == 'Dias Úteis (Seg-Sex)']['Chamados'].sum()
    media_fds = df_medias[df_medias['Tipo de Dia'] == 'Final de Semana (Sáb-Dom)']['Chamados'].sum()
    
    # Calcula o percentual de aumento/sobrecarga
    aumento = 0
    if media_util > 0:
        aumento = ((media_fds - media_util) / media_util) * 100

    # 5. Renderização (Dividido em Métricas e Gráfico)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### :material/assignment_ind: Escala e Gestão de Efetivo")
        
        st.metric(label="Média de Resgates (Dias Úteis)", value=f"{media_util:.1f} / dia")
        
        st.metric(
            label="Média de Resgates (Fim de Semana)", 
            value=f"{media_fds:.1f} / dia",
            delta=f"+ {aumento:.1f}% de sobrecarga" if aumento > 0 else f"{aumento:.1f}% de variação",
            delta_color="inverse" # Fica vermelho se for positivo (alerta de sobrecarga na tropa)
        )
        
        st.info(":material/campaign: **Decisão Tática:** O painel estatístico evidencia o comportamento da demanda. Se houver sobrecarga, recomenda-se alocação de IRSO para cobrir as áreas críticas mapeadas.")
        
    with col2:
        # Gráfico de Rosca para comparar a proporção das médias
        fig = px.pie(
            df_medias, 
            values='Chamados', 
            names='Tipo de Dia', 
            hole=0.5,
            title="Proporção da Carga Operacional Diária",
            color='Tipo de Dia',
            color_discrete_map={
                'Final de Semana (Sáb-Dom)': '#08306B', # Azul bem escuro (foco do alerta)
                'Dias Úteis (Seg-Sex)': '#6BAED6'      # Azul claro (rotina normal)
            }
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(margin=dict(t=50, l=0, r=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
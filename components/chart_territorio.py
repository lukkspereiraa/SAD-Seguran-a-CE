import streamlit as st
import plotly.express as px

def render(df_filtrado):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(":material/bar_chart: Municípios de Maior Incidência")
        with st.popover(":material/help: Metodologia e Leitura"):
            st.markdown("""
            **Diretrizes de Leitura:**
            O eixo horizontal representa o volume absoluto de ocorrências, enquanto o eixo vertical lista os municípios. Cores mais intensas (tons de vermelho escuro) reforçam visualmente as barras com maiores valores.
            
            **Regras de Negócio e Tratamento:**
            * Fonte de Dados: Coluna `Município` da aba CVLI.
            * Processamento: Realiza-se a contagem absoluta (`value_counts`) das linhas que atendem aos filtros globais selecionados pelo usuário.
            * Limitação: O painel exibe estritamente os 10 municípios com os maiores índices (Top 10) para evitar poluição visual, ordenados de forma decrescente.
            """)
            
        top_mun = df_filtrado['Município'].value_counts().head(10).reset_index()
        top_mun.columns = ['Município', 'Ocorrências']
        fig_mun = px.bar(top_mun, x='Ocorrências', y='Município', orientation='h', color='Ocorrências', color_continuous_scale='Reds')
        fig_mun.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_mun, use_container_width=True)

    with col2:
        st.subheader(":material/stacked_bar_chart: Concentração por AIS")
        with st.popover(":material/help: Metodologia e Leitura"):
            st.markdown("""
            **Diretrizes de Leitura:**
            O eixo vertical representa o volume de vítimas e o eixo horizontal lista as Áreas Integradas de Segurança (AIS). Permite identificar rapidamente qual zona tática demanda maior alocação de recursos preventivos.
            
            **Regras de Negócio e Tratamento:**
            * Fonte de Dados: Coluna `AIS` da aba CVLI.
            * Processamento: Agrupamento e soma de ocorrências por área territorial tática definida pela Secretaria de Segurança, respeitando os filtros de data e perfil ativos na barra lateral.
            """)
            
        top_ais = df_filtrado['AIS'].value_counts().reset_index()
        top_ais.columns = ['AIS', 'Ocorrências']
        fig_ais = px.bar(top_ais, x='AIS', y='Ocorrências', text='Ocorrências', color_discrete_sequence=['#8B0000'])
        st.plotly_chart(fig_ais, use_container_width=True)
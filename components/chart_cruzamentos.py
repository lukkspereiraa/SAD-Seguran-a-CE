import streamlit as st
import plotly.express as px

def render(df_filtrado):
    # --- NOVO GRÁFICO: NATUREZA DO CRIME (Largura Total) ---
    st.subheader(":material/gavel: Incidência por Natureza Criminal")
    with st.popover(":material/help: Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        Classificação legal ou tipificação da ocorrência. O gráfico apresenta o volume absoluto de casos segmentado pela natureza registrada no documento policial, ordenado da maior para a menor incidência.
        
        **Regras de Negócio e Tratamento:**
        * Fonte de Dados: Coluna `Natureza` da aba CVLI.
        * Processamento: Realiza-se a contagem absoluta (`value_counts`) das tipificações ativas de acordo com os filtros.
        """)
        
    df_natureza = df_filtrado['Natureza'].value_counts().reset_index()
    df_natureza.columns = ['Natureza', 'Quantidade']
    
    fig_nat = px.bar(
        df_natureza, 
        x='Quantidade', 
        y='Natureza', 
        orientation='h', 
        color='Quantidade', 
        color_continuous_scale='Reds'
    )
    fig_nat.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_nat, use_container_width=True)

    st.divider()

    # --- GRÁFICOS DIVIDIDOS EM DUAS COLUNAS ---
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader(":material/query_stats: Arma vs. Faixa Etária")
        with st.popover(":material/help: Metodologia e Leitura"):
            st.markdown("""
            **Diretrizes de Leitura:**
            Gráfico de barras agrupadas. O eixo horizontal divide as vítimas por idade. Dentro de cada grupo etário, barras de cores diferentes mostram qual arma foi utilizada.
            
            **Regras de Negócio e Tratamento:**
            * Fonte de Dados: Colunas `Idade da Vítima` e `Meio Empregado`.
            * Processamento (Data Binning): A idade bruta é fatiada por meio da função `pd.cut()` em quatro classes demográficas. Casos sem idade informada recebem a flag "Não Informada".
            """)
            
        cross = df_filtrado.groupby(['Faixa Etária', 'Meio Empregado']).size().reset_index(name='Quantidade')
        fig_cross = px.bar(cross, x='Faixa Etária', y='Quantidade', color='Meio Empregado', barmode='group', color_discrete_sequence=px.colors.qualitative.Safe)
        fig_cross.update_layout(legend_title_text='Arma Utilizada', margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_cross, use_container_width=True)
        
    with col4:
        st.subheader(":material/school: Grau de Escolaridade")
        with st.popover(":material/help: Metodologia e Leitura"):
            st.markdown("""
            **Diretrizes de Leitura:**
            Correlaciona o nível de instrução formal da vítima com a probabilidade de vitimização letal.
            
            **Regras de Negócio e Tratamento:**
            * Fonte de Dados: Coluna `Escolaridade da Vítima`.
            * Processamento: Os dados são tipados para `String`. Realiza-se a contagem absoluta de frequência e ordenação decrescente da carga de dados filtrada.
            """)
            
        df_escolaridade = df_filtrado['Escolaridade da Vítima'].value_counts().reset_index()
        df_escolaridade.columns = ['Escolaridade', 'Quantidade']
        fig_escola = px.bar(df_escolaridade, x='Quantidade', y='Escolaridade', orientation='h', color='Quantidade', color_continuous_scale='Blues')
        fig_escola.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_escola, use_container_width=True)
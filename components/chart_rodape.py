import streamlit as st
import plotly.express as px

def render(df_filtrado):
    # Divide a tela em duas colunas (60% para a linha, 40% para a pizza)
    col_linha, col_pizza = st.columns([6, 4])
    
    with col_linha:
        st.subheader(":material/timeline: Evolução Diária das Ocorrências")
        with st.popover(":material/help: Metodologia e Leitura"):
            st.markdown("""
            **Diretrizes de Leitura:**
            O gráfico de linhas evidencia a flutuação do volume de crimes dia a dia. Picos (pontos altos na linha) revelam surtos de violência em datas específicas.
            
            **Regras de Negócio e Tratamento:**
            * Fonte de Dados: Coluna `Data` da aba CVLI.
            * Processamento: Agrupamento da soma total de ocorrências por dia exato. Interage nativamente com todos os recortes de filtro da barra lateral.
            """)
            
        # Agrupa os dados pela data exata
        df_tendencia = df_filtrado.groupby('Data').size().reset_index(name='Casos')
        
        fig_linha = px.line(
            df_tendencia, 
            x='Data', 
            y='Casos', 
            markers=True, 
            color_discrete_sequence=['#d32f2f'] # Vermelho alerta
        )
        fig_linha.update_layout(xaxis_title="Data da Ocorrência", yaxis_title="Vítimas", margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_linha, use_container_width=True)
        
    with col_pizza:
        st.subheader(":material/pie_chart: Distribuição por Gênero")
        with st.popover(":material/help: Metodologia e Leitura"):
            st.markdown("""
            **Diretrizes de Leitura:**
            O gráfico de setores (pizza) exibe a proporção de vitimização entre os gêneros registrados, permitindo identificar rapidamente o alvo demográfico majoritário.
            
            **Regras de Negócio e Tratamento:**
            * Fonte de Dados: Coluna `Gênero` da aba CVLI.
            * Processamento: Contagem absoluta e conversão em percentual relativo ao volume total do recorte filtrado.
            """)
            
        df_genero = df_filtrado['Gênero'].value_counts().reset_index()
        df_genero.columns = ['Gênero', 'Quantidade']
        
        # Gráfico de pizza com buraco no meio (donut) para um visual mais moderno
        fig_pizza = px.pie(
            df_genero, 
            names='Gênero', 
            values='Quantidade',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pizza.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_pizza, use_container_width=True)
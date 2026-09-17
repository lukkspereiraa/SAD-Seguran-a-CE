import streamlit as st
import plotly.express as px

def render(df_filtrado):
    st.subheader(":material/calendar_month: Mapa de Calor: Risco Operacional por Dia e Hora")
    with st.popover(":material/help: Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        Matriz bidimensional onde as linhas são os dias da semana e as colunas são as horas do dia (00h às 23h). A intensidade da cor indica a densidade de crimes: zonas amarelas são pacíficas, enquanto zonas vermelhas indicam picos de violência (Hotspots Temporais).
        
        **Regras de Negócio e Tratamento:**
        * Fonte de Dados: Colunas `Dia da Semana` e `Hora` da aba CVLI.
        * Processamento: A hora exata do crime sofre um "split" programático para extrair apenas a hora cheia. Os dias da semana são convertidos em dados categóricos ordenados (Segunda a Domingo) para garantir a ordem cronológica no eixo Y.
        """)
        
    heatmap_data = df_filtrado.groupby(['Dia da Semana', 'Hora_Pico']).size().reset_index(name='Casos')
    fig_heat = px.density_heatmap(heatmap_data, x='Hora_Pico', y='Dia da Semana', z='Casos', color_continuous_scale='YlOrRd', labels={'Hora_Pico': 'Hora do Dia (00h - 23h)'})
    st.plotly_chart(fig_heat, use_container_width=True)
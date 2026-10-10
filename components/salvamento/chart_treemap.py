import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'AIS' not in df.columns or 'Município' not in df.columns: 
        return
        
    with st.popover(":material/help: Metodologia e Leitura (Mapa de Árvore)"):
        st.markdown("""
        **Navegação Hierárquica (Treemap):**
        Este gráfico permite uma imersão profunda (Drill-down) na distribuição espacial dos chamados de resgate e salvamento.
        
        * **Níveis da Árvore:** Ceará (Estado) > AIS (Batalhão/Área) > Município.
        * **Tamanho e Cor do Bloco:** Quanto maior e mais escuro o retângulo, maior o **Volume de Chamados** recebidos naquela região.
        * **Como interagir:** Clique em cima de uma AIS (ex: 'AIS 02') para dar um "zoom" e isolar a visão apenas nos municípios que compõem aquela AIS. Clique no título superior (barra cinza) para voltar.
        """)
    
    # 1. Tratamento de Dados: Evita que valores nulos quebrem a hierarquia
    df_tree = df.copy()
    df_tree['AIS'] = df_tree['AIS'].fillna('AIS Não Informada').astype(str)
    df_tree['Município'] = df_tree['Município'].fillna('Município Não Informado')
    
    # 2. Agrupa a CONTAGEM de ocorrências (tamanho) seguindo o caminho da hierarquia
    # Como não temos coluna 'Quantidade', usamos .size() para contar as linhas
    df_agrupado = df_tree.groupby(['AIS', 'Município']).size().reset_index(name='Chamados')
    
    # Filtra apenas os que têm chamados maiores que zero
    df_agrupado = df_agrupado[df_agrupado['Chamados'] > 0]

    # 3. Renderização do Treemap
    fig = px.treemap(
        df_agrupado,
        path=[px.Constant("Ceará (Total)"), 'AIS', 'Município'],
        values='Chamados',
        color='Chamados',
        color_continuous_scale='Blues',
        title="Estrutura Hierárquica de Chamados (Zoom Interativo)"
    )
    
    # Melhora a exibição dos textos dentro dos blocos (Rótulo + % do pai)
    fig.update_traces(
        textinfo="label+percent parent",
        hovertemplate="<b>%{label}</b><br>Total de Chamados: %{value}<br>Representa %{percentParent:.1%} da sua área maior<extra></extra>"
    )
    
    fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))

    st.plotly_chart(fig, use_container_width=True)
    
    st.info(":material/account_tree: **Interatividade:** O gráfico acima é clicável! Clique em uma caixa para mergulhar nos dados do Município ou AIS, e clique no título no topo do gráfico para voltar.")
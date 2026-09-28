import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty or 'AIS' not in df.columns or 'Município' not in df.columns: 
        return
        
    with st.popover(":material/help: Metodologia e Leitura (Mapa de Árvore)"):
        st.markdown("""
        **Navegação Hierárquica (Treemap):**
        Este gráfico permite uma imersão profunda (Drill-down) na cadeia de distribuição do tráfico.
        
        * **Níveis da Árvore:** Ceará (Estado) > AIS (Batalhão) > Município > Tipo de Droga.
        * **Tamanho do Bloco:** Quanto maior o retângulo, maior o **Volume em Kg** apreendido.
        * **Como interagir:** Clique em cima de uma AIS (ex: 'AIS 14') para dar um "zoom" e expandir apenas os municípios dela. Clique no título superior para voltar.
        
        **Valor Tático:** Permite ao comando identificar imediatamente o centro de gravidade do tráfico. Em uma única tela, fica óbvio qual AIS demanda mais atenção, qual cidade puxa essa métrica para cima e qual droga é o carro-chefe daquela região.
        """)
    
    # 1. Tratamento de Dados: Evita que valores nulos quebrem a hierarquia da árvore
    df_tree = df.copy()
    df_tree['AIS'] = df_tree['AIS'].fillna('AIS Não Informada').astype(str)
    df_tree['Município'] = df_tree['Município'].fillna('Município Não Informado')
    df_tree['Tipo de Entorpecente'] = df_tree['Tipo de Entorpecente'].fillna('Não Informado')
    
    # 2. Agrupa a soma de Volume (Kg) seguindo o caminho da hierarquia
    df_agrupado = df_tree.groupby(['AIS', 'Município', 'Tipo de Entorpecente'])['Quantidade (Kg)'].sum().reset_index()
    
    # Filtra apenas os que têm peso maior que zero para o gráfico ficar limpo
    df_agrupado = df_agrupado[df_agrupado['Quantidade (Kg)'] > 0]

    # 3. Renderização do Treemap
    fig = px.treemap(
        df_agrupado,
        path=[px.Constant("Ceará (Total)"), 'AIS', 'Município', 'Tipo de Entorpecente'],
        values='Quantidade (Kg)',
        color='Quantidade (Kg)',
        color_continuous_scale='Greens',
        title="Estrutura Hierárquica de Apreensões (Zoom Interativo)"
    )
    
    # Melhora a exibição dos textos dentro dos blocos (mostra o Rótulo e a % que ele representa do pai)
    fig.update_traces(
        textinfo="label+percent parent",
        hovertemplate="<b>%{label}</b><br>Volume: %{value:.2f} Kg<br>Representa %{percentParent:.1%} da área maior<extra></extra>"
    )
    
    fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))

    st.plotly_chart(fig, use_container_width=True)
    
    st.info(":material/account_tree: **Interatividade:** O gráfico acima é clicável! Clique em uma caixa para mergulhar nos dados do Município ou AIS, e clique no título no topo do gráfico para voltar.")
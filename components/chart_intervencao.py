import streamlit as st
import plotly.express as px
import pandas as pd

def render(df_ip):
    st.info(":material/info: Nota Metodológica: Os dados desta seção refletem o painel global de Intervenções Policiais. Filtros de CVLI não incidem sobre esta base.")
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader(":material/map: Ocorrências por Município (Top 10)")
        with st.popover(":material/help: Metodologia e Leitura"):
            st.markdown("""
            **Diretrizes de Leitura:**
            Exibe os 10 municípios com maior letalidade em ações com intervenção do Estado.
            
            **Regras de Negócio e Tratamento:**
            * Fonte de Dados: Planilha apartada `Intervenção Policial`.
            * Processamento: Esta base opera de forma independente (Stand-alone) em relação aos filtros de data, município e perfis aplicados na barra lateral para os CVLIs comuns. Representa a volumetria bruta.
            """)
            
        top_mun_ip = df_ip['Município'].value_counts().head(10).reset_index()
        top_mun_ip.columns = ['Município', 'Casos']
        fig_ip_mun = px.bar(top_mun_ip, x='Casos', y='Município', orientation='h', color_discrete_sequence=['#4a4e69'])
        fig_ip_mun.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_ip_mun, use_container_width=True)
        
    with col6:
        st.subheader(":material/candlestick_chart: Dispersão Etária nas Intervenções")
        with st.popover(":material/help: Metodologia e Leitura"):
            st.markdown("""
            **Diretrizes de Leitura (Diagrama de Caixa / Boxplot):**
            * A linha central dentro da caixa marca a **Mediana** (50% das vítimas têm até essa idade).
            * Os limites da caixa colorida representam o 1º e 3º Quartis.
            * As hastes (bigodes) mostram a amplitude, e os pontos isolados nas extremidades são os **Outliers** (casos fora da curva).
            
            **Regras de Negócio e Tratamento:**
            * Fonte de Dados: Coluna `Idade` da planilha `Intervenção Policial`.
            * Processamento: Conversão rigorosa de `String` para `Float/Numérico`, ignorando dados não preenchidos (`coerce`) para permitir o cálculo correto das medidas de dispersão estatística.
            """)
            
        df_ip['Idade Numérica'] = pd.to_numeric(df_ip['Idade'], errors='coerce')
        fig_ip_idade = px.box(df_ip, y='Idade Numérica', points="all", color_discrete_sequence=['#9a031e'])
        fig_ip_idade.update_layout(yaxis_title="Idade")
        st.plotly_chart(fig_ip_idade, use_container_width=True)
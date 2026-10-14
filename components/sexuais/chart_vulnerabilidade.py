import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    st.markdown("#### Matriz de Vulnerabilidade Socioeconómica")
    st.info("Inteligência Assistencial: Agressores sexuais tendem a vitimizar indivíduos em situação de vulnerabilidade sistémica. O mapeamento do nível de instrução e raça guia a alocação de recursos do CRAS, CREAS e campanhas de literacia de direitos.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'Escolaridade da Vítima' in df.columns:
            # Filtra os dados e remove nulos/não informados para ver a tendência real
            df_esc = df[~df['Escolaridade da Vítima'].isin(['Não Informada', 'Sem Informação', 'NÃO INFORMADA'])]
            df_esc_count = df_esc['Escolaridade da Vítima'].value_counts().reset_index()
            df_esc_count.columns = ['Escolaridade', 'Ocorrências']
            
            fig_esc = px.bar(
                df_esc_count, x='Ocorrências', y='Escolaridade', orientation='h',
                title="Vitimização por Nível de Instrução",
                color='Ocorrências', color_continuous_scale='PuRd'
            )
            fig_esc.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_esc, use_container_width=True)

    with col2:
        if 'Raça da Vítima' in df.columns:
            df_raca = df[~df['Raça da Vítima'].isin(['Não Informada', 'Sem Informação', 'NÃO INFORMADA'])]
            df_raca_count = df_raca['Raça da Vítima'].value_counts().reset_index()
            df_raca_count.columns = ['Raça/Cor', 'Total']
            
            fig_raca = px.pie(
                df_raca_count, values='Total', names='Raça/Cor', hole=0.4, 
                title="Vitimização por Raça/Cor Declarada", 
                color_discrete_sequence=['#CE1256', '#DF65B0', '#D7B5D8', '#F1EEF6']
            )
            fig_raca.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_raca, use_container_width=True)
            
    # Métrica de Subnotificação (Qualidade do Dado)
    if 'Raça da Vítima' in df.columns:
        total_casos = len(df)
        sem_info = df['Raça da Vítima'].isin(['Não Informada', 'Sem Informação', 'NÃO INFORMADA']).sum()
        if total_casos > 0 and (sem_info / total_casos) > 0.3:
            st.warning(f"**Alerta de Qualidade de Dados:** {int((sem_info/total_casos)*100)}% dos inquéritos/BOs não contêm a identificação racial ou de escolaridade da vítima. É recomendada uma auditoria processual nas delegacias para melhorar a recolha de dados sociais.")
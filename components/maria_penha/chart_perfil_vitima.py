import streamlit as st
import plotly.express as px

def render(df):
    if df.empty: return
    
    st.info(":material/fingerprint: **Mapeamento de Vulnerabilidade:** Analise quais grupos demográficos estão sendo mais vitimizados para direcionar campanhas de prevenção e acolhimento.")
    
    col1, col2 = st.columns(2)
    
    # 1. Perfil por Raça/Cor
    with col1:
        df_raca = df['Raça da Vítima'].value_counts().reset_index()
        df_raca.columns = ['Raça', 'Total']
        
        fig_raca = px.pie(
            df_raca, 
            values='Total', 
            names='Raça', 
            hole=0.45,
            title="Distribuição por Raça/Cor",
            color_discrete_sequence=px.colors.sequential.Purples_r
        )
        fig_raca.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_raca, use_container_width=True)

    # 2. Perfil Etário
    with col2:
        df_idade = df['Faixa Etária'].value_counts().reset_index()
        df_idade.columns = ['Faixa Etária', 'Total']
        
        fig_idade = px.bar(
            df_idade, 
            x='Faixa Etária', 
            y='Total', 
            title="Perfil Etário da Vítima",
            color='Total',
            color_continuous_scale='Purples'
        )
        st.plotly_chart(fig_idade, use_container_width=True)
        
    st.divider()

    # 3. Grau de Escolaridade
    df_esc = df['Escolaridade da Vítima'].value_counts().reset_index()
    df_esc.columns = ['Escolaridade', 'Total']
    
    fig_esc = px.bar(
        df_esc, 
        y='Escolaridade', 
        x='Total', 
        orientation='h',
        title="Grau de Instrução (Escolaridade)",
        color='Total',
        color_continuous_scale='Purples'
    )
    fig_esc.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_esc, use_container_width=True)
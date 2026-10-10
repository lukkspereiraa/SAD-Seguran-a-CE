import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### :material/wc: Identidade de Género")
        df_gen = df['Identidade de Gênero'].value_counts().reset_index()
        df_gen.columns = ['Identidade', 'Total']
        
        fig_gen = px.pie(
            df_gen, 
            values='Total', 
            names='Identidade', 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_gen.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gen, use_container_width=True)

    with col2:
        st.markdown("#### :material/favorite: Orientação Sexual")
        df_ori = df['Orientação Sexual'].value_counts().reset_index()
        df_ori.columns = ['Orientação', 'Total']
        
        fig_ori = px.bar(
            df_ori, 
            x='Orientação', 
            y='Total', 
            color='Total',
            color_continuous_scale='Purples' # Paleta mais suave para barras
        )
        st.plotly_chart(fig_ori, use_container_width=True)
        
    st.divider()
    
    # NOVA ANÁLISE: Pirâmide Etária por Tipificação
    st.markdown("#### :material/filter_alt: Perfil Etário da Vítima")
    st.info("Analise qual faixa etária está mais vulnerável. Crimes de transfobia tendem a afetar vítimas mais jovens devido à alta taxa de expulsão precoce de casa e evasão escolar.")
    
    # Criamos um Funil Cruzado
    df_idade = df.groupby(['Faixa Etária', 'Natureza']).size().reset_index(name='Casos')
    
    # Ordenar a faixa etária logicamente
    ordem_idades = ['0 a 17 anos', '18 a 29 anos', '30 a 59 anos', '60+ anos (Idosos)', 'Não Informada']
    df_idade['Faixa Etária'] = pd.Categorical(df_idade['Faixa Etária'], categories=ordem_idades, ordered=True)
    df_idade = df_idade.sort_values('Faixa Etária')
    
    fig_idade = px.bar(
        df_idade, 
        y='Faixa Etária', 
        x='Casos',
        color='Natureza',
        orientation='h',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Distribuição de Vítimas por Idade e Tipo de Crime"
    )
    fig_idade.update_layout(yaxis={'categoryorder':'array', 'categoryarray': ordem_idades})
    
    st.plotly_chart(fig_idade, use_container_width=True)
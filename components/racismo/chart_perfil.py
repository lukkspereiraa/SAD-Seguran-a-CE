import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### :material/wc: Género da Vítima")
        df_gen = df['Gênero'].value_counts().reset_index()
        df_gen.columns = ['Género', 'Total']
        
        fig_gen = px.pie(df_gen, values='Total', names='Género', hole=0.45, color_discrete_sequence=px.colors.sequential.Oranges_r)
        fig_gen.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gen, use_container_width=True)

    with col2:
        st.markdown("#### :material/groups: Interseção (Raça vs Género)")
        st.info("Nota: Excluímos os dados 'Não Informados' neste gráfico para revelar o perfil demográfico real das vítimas identificadas.")
        
        # Filtra os dados com Raça válida para o cruzamento
        df_valido = df[~df['Raça da Vítima'].isin(['Não Informada', 'Não Informado', 'Nao Informada'])].copy()
        
        if not df_valido.empty:
            df_cross = df_valido.groupby(['Raça da Vítima', 'Gênero']).size().reset_index(name='Casos')
            fig_cross = px.bar(
                df_cross, x='Raça da Vítima', y='Casos', color='Gênero', barmode='group',
                color_discrete_sequence=['#FD8D3C', '#A63603', '#FDD0A2']
            )
            st.plotly_chart(fig_cross, use_container_width=True)
        else:
            st.warning("Sem dados suficientes de raça identificada para este cruzamento.")
            
    st.divider()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### :material/school: Grau de Instrução")
        df_esc = df['Escolaridade da Vítima'].value_counts().reset_index()
        df_esc.columns = ['Escolaridade', 'Total']
        
        fig_esc = px.bar(df_esc, y='Escolaridade', x='Total', orientation='h', color='Total', color_continuous_scale='Oranges')
        fig_esc.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_esc, use_container_width=True)
        
    with col4:
        st.markdown("#### :material/badge: Faixa Etária")
        if 'Faixa Etária' in df.columns:
            df_idade = df['Faixa Etária'].value_counts().reset_index()
            df_idade.columns = ['Faixa Etária', 'Total']
            
            # Ordenar logicamente
            ordem_idades = ['0 a 17 anos', '18 a 29 anos', '30 a 59 anos', '60+ anos (Idosos)', 'Não Informada']
            df_idade['Faixa Etária'] = pd.Categorical(df_idade['Faixa Etária'], categories=ordem_idades, ordered=True)
            df_idade = df_idade.sort_values('Faixa Etária')
            
            fig_idade = px.bar(
                df_idade, x='Faixa Etária', y='Total', color='Total', color_continuous_scale='Oranges'
            )
            st.plotly_chart(fig_idade, use_container_width=True)
import streamlit as st
import plotly.express as px
import pandas as pd

def classificar_faixa_etaria(idade):
    try:
        i = int(idade)
        if i <= 11: return '1. Criança (0-11)'
        elif i <= 17: return '2. Adolescente (12-17)'
        elif i <= 29: return '3. Jovem (18-29)'
        elif i <= 59: return '4. Adulto (30-59)'
        else: return '5. Idoso (60+)'
    except:
        return '6. Não Informada'

def render(df):
    if df.empty: return
    
    st.markdown("#### Análise de Vulnerabilidade e Perfil da Vítima")
    st.info("Inteligência Social: A identificação da faixa etária e perfil demográfico permite o direcionamento de campanhas de prevenção e atuação de assistentes sociais/psicólogos.")
    
    df_demo = df.copy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico 1: Faixa Etária (A grande descoberta tática)
        if 'Idade da Vítima' in df_demo.columns:
            df_demo['Faixa Etária'] = df_demo['Idade da Vítima'].apply(classificar_faixa_etaria)
            df_idade = df_demo['Faixa Etária'].value_counts().reset_index()
            df_idade.columns = ['Faixa Etária', 'Ocorrências']
            df_idade = df_idade.sort_values('Faixa Etária')
            
            fig_idade = px.bar(
                df_idade, x='Ocorrências', y='Faixa Etária', orientation='h',
                title="Vítimas por Faixa Etária (Estatuto da Criança e Adolescente)",
                color='Ocorrências', color_continuous_scale='PuRd'
            )
            fig_idade.update_layout(yaxis={'categoryorder':'category descending'})
            st.plotly_chart(fig_idade, use_container_width=True)
            
            # Alerta Automático se houver muita criança
            criancas_adolescentes = df_demo[df_demo['Faixa Etária'].isin(['1. Criança (0-11)', '2. Adolescente (12-17)'])].shape[0]
            if criancas_adolescentes > 0:
                percentual = (criancas_adolescentes / len(df_demo)) * 100
                st.error(f"**Alerta ECA:** {percentual:.1f}% das vítimas registadas neste filtro são Crianças ou Adolescentes (menores de 18 anos), configurando presunção de vulnerabilidade absoluta.")

    with col2:
        # Gráfico 2: Género e Raça
        if 'Gênero' in df_demo.columns:
            df_gen = df_demo['Gênero'].value_counts().reset_index()
            df_gen.columns = ['Gênero', 'Total']
            
            fig_gen = px.pie(
                df_gen, values='Total', names='Gênero', hole=0.4, 
                title="Distribuição por Género", 
                color_discrete_sequence=['#980043', '#DD1C77', '#DF65B0', '#C994C7']
            )
            fig_gen.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_gen, use_container_width=True)
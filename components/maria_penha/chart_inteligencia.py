import streamlit as st
import plotly.express as px
import pandas as pd

def render(df):
    if df.empty: return
    
    with st.popover(":material/help: Metodologia de Inteligência Socioterritorial"):
        st.markdown("""
        **1. Funil de Risco Etário:** Ilustra o volume de vitimização por faixa etária, permitindo identificar onde a vulnerabilidade afunila ou expande.
        **2. Padrão Temporal por Escolaridade:** Gráfico de dispersão cruzando o horário do crime com o grau de instrução, revelando se a rotina de diferentes classes sociais altera a dinâmica da violência.
        **3. Vulnerabilidade Territorial:** Cruza a localização (AIS) com o grau de instrução, permitindo direcionar campanhas de prevenção com a linguagem e abordagem adequadas para cada região.
        """)

    col1, col2 = st.columns(2)

    # ==========================================
    # 1. FUNIL DE RISCO ETÁRIO
    # ==========================================
    with col1:
        st.markdown("#### :material/filter_alt: Funil de Risco Etário")
        
        df_idade = df['Faixa Etária'].value_counts().reset_index()
        df_idade.columns = ['Faixa Etária', 'Casos']
        
        # Ordenar para o funil fazer sentido (do mais novo ao mais velho, ou por volume)
        ordem_idades = ['0 a 17 anos', '18 a 29 anos', '30 a 59 anos', '60+ anos (Idosas)', 'Não Informada']
        df_idade['Faixa Etária'] = pd.Categorical(df_idade['Faixa Etária'], categories=ordem_idades, ordered=True)
        df_idade = df_idade.sort_values('Faixa Etária')
        
        fig_funil = px.funnel(
            df_idade, 
            y='Faixa Etária', 
            x='Casos',
            title="Distribuição de Vitimização (Ciclo de Vida)",
            color_discrete_sequence=['#6A0DAD']
        )
        st.plotly_chart(fig_funil, use_container_width=True)

    # ==========================================
    # 2. DISPERSÃO: HORA VS ESCOLARIDADE
    # ==========================================
    with col2:
        st.markdown("#### :material/scatter_plot: Padrão Temporal Sociológico")
        
        if 'Hora_Pico' in df.columns:
            df_disp = df.copy()
            df_disp['Hora_Pico'] = pd.to_numeric(df_disp['Hora_Pico'], errors='coerce')
            df_disp = df_disp.dropna(subset=['Hora_Pico'])
            df_disp['Hora_Pico'] = df_disp['Hora_Pico'].astype(int).astype(str).str.zfill(2) + 'h'
            
            df_bolhas = df_disp.groupby(['Hora_Pico', 'Escolaridade da Vítima']).size().reset_index(name='Casos')
            
            fig_bolhas = px.scatter(
                df_bolhas, 
                x='Hora_Pico', 
                y='Escolaridade da Vítima', 
                size='Casos', 
                color='Casos',
                color_continuous_scale='Purples',
                title="Horário da Agressão x Grau de Instrução"
            )
            # Organiza as horas da esquerda para a direita
            fig_bolhas.update_xaxes(categoryorder='category ascending')
            fig_bolhas.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
            st.plotly_chart(fig_bolhas, use_container_width=True)
        else:
            st.warning("Dados de hora indisponíveis para este gráfico.")

    st.divider()

    # ==========================================
    # 3. HEATMAP: AIS VS ESCOLARIDADE
    # ==========================================
    st.markdown("#### :material/grid_on: Matriz Territorial de Vulnerabilidade")
    
    df_territorio = df.groupby(['AIS', 'Escolaridade da Vítima']).size().reset_index(name='Casos')
    
    fig_heat_ter = px.density_heatmap(
        df_territorio, 
        x='Escolaridade da Vítima', 
        y='AIS', 
        z='Casos',
        color_continuous_scale='Purples',
        title='Concentração Socioterritorial (Área de Segurança x Instrução)'
    )
    
    fig_heat_ter.update_layout(height=600)
    st.plotly_chart(fig_heat_ter, use_container_width=True)
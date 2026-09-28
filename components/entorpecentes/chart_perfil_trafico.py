import streamlit as st
import plotly.express as px

def render(df):
    if df.empty: return
    
    with st.popover(":material/help: Metodologia de Classificação de Porte"):
        st.markdown("""
        **Critérios e Regras de Negócio:**
        Para entender o impacto real na logística financeira do crime organizado, as apreensões foram divididas em três categorias baseadas no peso (Kg):
        
        * **1. Varejo / Consumo:** Apreensões de até 100g. Geralmente associadas a usuários ou "aviõezinhos".
        * **2. Médio Porte:** De 100g a 2Kg. Associado ao abastecimento local de "bocas de fumo".
        * **3. Atacado / Grande Carga:** Acima de 2Kg. Interceptação de logística interestadual e atacadistas de drogas.
        """)
    
    def classificar_porte(kg):
        if kg <= 0.100:
            return '1. Varejo / Consumo (Até 100g)'
        elif kg <= 2.0:
            return '2. Médio Porte (100g a 2Kg)'
        else:
            return '3. Atacado / Grande Carga (Acima de 2Kg)'
            
    df_perfil = df.copy()
    df_perfil['Escala do Tráfico'] = df_perfil['Quantidade (Kg)'].apply(classificar_porte)
    
    col1, col2 = st.columns(2)
    
    with col1:
        df_freq_porte = df_perfil['Escala do Tráfico'].value_counts().reset_index()
        df_freq_porte.columns = ['Escala do Tráfico', 'Frequência Policial']
        df_freq_porte = df_freq_porte.sort_values('Escala do Tráfico')
        
        fig_freq = px.bar(
            df_freq_porte,
            x='Escala do Tráfico',
            y='Frequência Policial',
            title="Qtd. de Ocorrências por Escala",
            text_auto=True,
            color='Escala do Tráfico',
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig_freq.update_layout(showlegend=False)
        st.plotly_chart(fig_freq, use_container_width=True)
        
    with col2:
        df_vol_porte = df_perfil.groupby('Escala do Tráfico')['Quantidade (Kg)'].sum().reset_index()
        df_vol_porte = df_vol_porte.sort_values('Escala do Tráfico')
        
        fig_vol = px.bar(
            df_vol_porte,
            x='Escala do Tráfico',
            y='Quantidade (Kg)',
            title="Impacto Real: Volume (Kg) por Escala",
            text_auto='.2f',
            color='Escala do Tráfico',
            color_discrete_sequence=px.colors.sequential.Teal
        )
        fig_vol.update_layout(showlegend=False)
        st.plotly_chart(fig_vol, use_container_width=True)
        
    st.info(":material/lightbulb: **Leitura Tática:** A polícia realiza milhares de pequenas apreensões de Varejo (alta frequência), mas o grande golpe no narcotráfico é o Atacado (onde os quilos realmente se concentram e descapitalizam o crime).")
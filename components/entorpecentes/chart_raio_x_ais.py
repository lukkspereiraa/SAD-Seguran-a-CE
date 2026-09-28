import streamlit as st
import plotly.express as px

def render(df):
    if df.empty or 'AIS' not in df.columns: 
        return
        
    with st.popover(":material/help: Metodologia e Leitura (Raio-X por AIS)"):
        st.markdown("""
        **Vocação Criminal do Território:**
        Este gráfico exibe a proporção (em %) dos tipos de drogas apreendidas dentro de cada Área Integrada de Segurança (AIS).
        
        * **Eixo X:** As Áreas Integradas de Segurança (AIS).
        * **Eixo Y:** Percentual (0 a 100%) do Volume (Kg) apreendido.
        * **Como ler:** Cada barra totaliza 100%. Se a parte vermelha (ex: Crack) ocupa 80% da barra da AIS 03, isso significa que a imensa maioria do volume apreendido naquele território é Crack.
        
        **Valor Tático:** Permite identificar corredores logísticos específicos e orientar o direcionamento de delegacias especializadas (como a DENARC) para as AIS que apresentam vocação atacadista de uma droga específica.
        """)
    
    # Prepara os dados (Agrupa por AIS e Tipo)
    df_ais = df.groupby(['AIS', 'Tipo de Entorpecente'])['Quantidade (Kg)'].sum().reset_index()
    
    # Remove as linhas onde a AIS não foi preenchida
    df_ais = df_ais.dropna(subset=['AIS'])
    
    # Garante que a AIS seja tratada como texto para ficar bonita no eixo do gráfico
    df_ais['AIS'] = df_ais['AIS'].astype(str)
    
    # Ordena alfabeticamente/numericamente
    df_ais = df_ais.sort_values(by='AIS')

    # Plota o gráfico
    fig = px.bar(
        df_ais,
        x='AIS',
        y='Quantidade (Kg)',
        color='Tipo de Entorpecente',
        title="Raio-X de Vocação Criminal (Proporção do Volume por AIS)",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        labels={'Quantidade (Kg)': 'Proporção do Volume'}
    )
    
    # O SEGREDO MÁGICO: Transforma as barras absolutas em percentuais 100% empilhados
    fig.update_layout(barmode='stack', barnorm='percent')
    fig.update_yaxes(ticksuffix="%")

    st.plotly_chart(fig, use_container_width=True)
    
    st.info(":material/my_location: **Gestão de Efetivo:** Municípios são divisões políticas, mas o policiamento atua em blocos de AIS. Este gráfico traduz a realidade do que cada Batalhão está enfrentando, isolando o ruído das cidades.")
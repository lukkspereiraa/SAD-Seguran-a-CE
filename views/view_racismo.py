import streamlit as st
import pandas as pd # <-- CORREÇÃO AQUI: Importação do pandas
from services.data_handler import filtrar_dados_racismo

# Importar os componentes isolados
import components.racismo.chart_mapa as chart_mapa
import components.racismo.chart_perfil as chart_perfil
import components.racismo.chart_matriz as chart_matriz
import components.racismo.chart_auditoria as chart_auditoria

def render(df_racismo, datas, municipios, ais):
    st.subheader(":material/balance: Preconceito de Raça ou Cor (Racismo / Injúria)")
    
    with st.popover(":material/help: Metodologia e Leitura"):
        st.markdown("""
        **Diretrizes de Leitura:**
        Análise de crimes tipificados na lei de racismo e injúria racial.
        
        **Foco Tático:**
        * **Interseccionalidade:** Avaliar a sobreposição de vulnerabilidades (ex: racismo associado ao machismo).
        * **Auditoria de Dados:** O crime de racismo exige a identificação da raça da vítima. A ausência deste dado configura uma falha grave de governação policial.
        """)
        
    if df_racismo.empty:
        st.warning(":material/warning: Base de dados não encontrada ou vazia.")
        return df_racismo

    # Filtros Demográficos
    st.markdown("#### :material/tune: Filtros de Perfil Demográfico")
    col1, col2, col3 = st.columns(3)
    with col1:
        generos = st.multiselect("Género:", sorted(df_racismo['Gênero'].dropna().unique()))
    with col2:
        racas = st.multiselect("Raça/Cor:", sorted(df_racismo['Raça da Vítima'].dropna().unique()))
    with col3:
        escolaridades = st.multiselect("Escolaridade:", sorted(df_racismo['Escolaridade da Vítima'].dropna().unique()))
        
    # Processamento
    df_filtrado = filtrar_dados_racismo(df_racismo, datas, municipios, ais, generos, racas, escolaridades)
    
    if df_filtrado.empty:
        st.warning(":material/search_off: Nenhum registo encontrado com estes filtros.")
        return df_filtrado

    # KPIs Principais
    st.divider()
    kpi1, kpi2, kpi3 = st.columns(3)
    
    total_casos = df_filtrado.shape[0]
    kpi1.metric(label=":material/report: Ocorrências Registadas", value=f"{total_casos:,}".replace(',', '.'))
    
    if total_casos > 0:
        mulheres = df_filtrado[df_filtrado['Gênero'] == 'Feminino'].shape[0]
        tx_mulheres = (mulheres / total_casos) * 100
        kpi2.metric(label=":material/female: Vítimas do Sexo Feminino", value=f"{tx_mulheres:.1f}%")
        
        raca_nula = df_filtrado['Raça da Vítima'].apply(lambda x: 1 if pd.isna(x) or str(x).strip() in ['Não Informada', 'Não Informado'] else 0).sum()
        tx_nula = (raca_nula / total_casos) * 100
        kpi3.metric(label=":material/warning: Raça Não Informada", value=f"{tx_nula:.1f}%")
    
    st.divider()
    
    # Renderização do Mapa
    chart_mapa.render(df_filtrado)
    
    st.divider()
    st.markdown("### :material/monitoring: Dinâmica Socioterritorial e Operacional")
    
    # Agora com 5 abas!
    aba1, aba2, aba3, aba4, aba5 = st.tabs([
        ":material/group: Perfil da Vítima", 
        ":material/calendar_clock: Matriz Temporal",
        ":material/trending_up: Evolução Mensal", 
        ":material/local_police: Inteligência Operacional", # <-- A NOVA ABA
        ":material/policy: Auditoria de Dados" 
    ])
    
    with aba1:
        chart_perfil.render(df_filtrado)
    with aba2:
        chart_matriz.render(df_filtrado)
    with aba3:
        import components.racismo.chart_evolucao as chart_evolucao 
        chart_evolucao.render(df_filtrado)
    with aba4:
        # Importação do novo componente
        import components.racismo.chart_operacional as chart_operacional
        chart_operacional.render(df_filtrado)
    with aba5:
        chart_auditoria.render(df_filtrado)
    
    return df_filtrado


    

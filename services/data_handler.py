import pandas as pd
import streamlit as st
import os
from services.config import CONFIG_BASES
from services.data_pipeline import aplicar_pipeline_transformacao

# =====================================================================
# 1. CARREGADOR DE DADOS
# =====================================================================
@st.cache_data
def carregar_dados():
    dfs = {}
    for nome_base, caminho in CONFIG_BASES.items():
        if os.path.exists(caminho):
            df_bruto = pd.read_excel(caminho, sheet_name=0)
            dfs[nome_base] = aplicar_pipeline_transformacao(df_bruto)
        else:
            if nome_base == 'CVLI': # Regra de Negócio: CVLI é a base mestra obrigatória
                st.error(f"🚨 Erro Crítico: Banco '{caminho}' não encontrado.")
                st.stop()
            dfs[nome_base] = pd.DataFrame()
            
    # Retorna as variáveis na ordem exata para consumo no app.py
    return dfs['CVLI'], dfs['Entorpecentes'], dfs['Armas'], dfs['Salvamento'], dfs['Maria da Penha'], dfs['LGBTfobia'], dfs['Racismo'], dfs['Furto'], dfs['CVP'], dfs['Crimes Sexuais'], dfs['Indigenas'], dfs['Animais'], dfs['Incendios']
# =====================================================================
# 2. MOTOR DE FILTRAGEM UNIVERSAL (Polimorfismo com **kwargs)
# =====================================================================
def filtrar_dataframe(df, datas, **filtros):
    """
    Motor central que recebe qualquer tipo de filtro dinamicamente.
    """
    if df.empty: return df
    
    # Filtro Temporal Obrigatório
    mask = (df['Data'].dt.date >= datas[0]) & (df['Data'].dt.date <= datas[1])
    
    # Filtros Flexíveis baseados nos Kwargs
    for coluna, valores in filtros.items():
        if valores and coluna in df.columns:
            mask &= df[coluna].isin(valores)
            
    return df[mask]

# =====================================================================
# 3. ADAPTERS DOS MÓDULOS (Consumidos pelas Views)
# =====================================================================
def filtrar_dados_cvli(df, datas, municipios, ais, meios, faixas, escolaridades, generos, naturezas):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais, **{'Meio Empregado': meios, 'Faixa Etária': faixas, 'Escolaridade da Vítima': escolaridades, 'Gênero': generos, 'Natureza': naturezas})

def filtrar_dados_entorpecentes(df, datas, municipios, ais, tipos_droga):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais, **{'Tipo de Entorpecente': tipos_droga})

def filtrar_dados_armas(df, datas, municipios, ais):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais)

def filtrar_dados_salvamento(df, datas, municipios, ais):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais)

def filtrar_dados_maria_penha(df, datas, municipios, ais, faixas_etarias, racas, escolaridades):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais, **{'Faixa Etária': faixas_etarias, 'Raça da Vítima': racas, 'Escolaridade da Vítima': escolaridades})

def filtrar_dados_lgbt(df, datas, municipios, ais, naturezas, identidades, orientacoes):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais, **{'Natureza': naturezas, 'Identidade de Gênero': identidades, 'Orientação Sexual': orientacoes})

def filtrar_dados_racismo(df, datas, municipios, ais, generos, racas, escolaridades):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais, **{'Gênero': generos, 'Raça da Vítima': racas, 'Escolaridade da Vítima': escolaridades})

def filtrar_dados_furto(df, datas, municipios, ais):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais)

def filtrar_dados_cvp(df, datas, municipios, ais):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais)

def filtrar_dados_crimes_sexuais(df, datas, municipios, ais):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais)

def filtrar_dados_indigenas(df, datas, municipios, ais):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais)

def filtrar_dados_animais(df, datas, municipios, ais):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais)

def filtrar_dados_incendios(df, datas, municipios, ais):
    return filtrar_dataframe(df, datas, Município=municipios, AIS=ais)
import pandas as pd
import streamlit as st
import os

# Função auxiliar para não repetir o tratamento de datas nas duas planilhas
def tratar_datas_comuns(df):
    if df.empty: return df
    df['Data'] = pd.to_datetime(df['Data'])
    df['Hora'] = df['Hora'].astype(str)
    df['Hora_Pico'] = df['Hora'].str.split(':').str[0]
    ordem_dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    df['Dia da Semana'] = pd.Categorical(df['Dia da Semana'], categories=ordem_dias, ordered=True)
    return df

@st.cache_data
def carregar_dados(caminho_cvli='dataSett/CVLI_Agosto.xlsx', caminho_ent='dataSett/Entorpecentes.xlsx'):
    if not os.path.exists(caminho_cvli):
        st.error(f"🚨 Erro Crítico: Banco '{caminho_cvli}' não encontrado.")
        st.stop()

    # Processamento CVLI
    df_cvli = tratar_datas_comuns(pd.read_excel(caminho_cvli, sheet_name=0))
    df_cvli['Idade Numérica'] = pd.to_numeric(df_cvli['Idade da Vítima'], errors='coerce')
    df_cvli['Faixa Etária'] = pd.cut(
        df_cvli['Idade Numérica'], bins=[0, 17, 29, 59, 150], 
        labels=['0 a 17 anos', '18 a 29 anos', '30 a 59 anos', '60+ anos (Idosos)'], right=True
    ).cat.add_categories('Não Informada').fillna('Não Informada')

    # Processamento Entorpecentes
    df_ent = tratar_datas_comuns(pd.read_excel(caminho_ent, sheet_name=0)) if os.path.exists(caminho_ent) else pd.DataFrame()

    return df_cvli, df_ent

def filtrar_dados_cvli(df, datas, municipios, ais, meios, faixas, escolaridades, generos, naturezas):
    if df.empty: return df
    
    # Cria uma máscara booleana única para desempenho muito mais rápido
    mask = (df['Data'].dt.date >= datas[0]) & (df['Data'].dt.date <= datas[1])
    
    # Dicionário mapeando as colunas às variáveis de filtro
    filtros = {
        'Município': municipios, 'AIS': ais, 'Meio Empregado': meios,
        'Faixa Etária': faixas, 'Escolaridade da Vítima': escolaridades,
        'Gênero': generos, 'Natureza': naturezas
    }
    
    # Aplica todos os filtros em 3 linhas
    for coluna, valores in filtros.items():
        if valores:
            mask &= df[coluna].isin(valores)
            
    return df[mask]

# --- NOVA FUNÇÃO DE FILTRO: ENTORPECENTES ---
def filtrar_dados_entorpecentes(df, datas, municipios, ais, tipos_droga):
    if df.empty: return df
    
    mask = (df['Data'].dt.date >= datas[0]) & (df['Data'].dt.date <= datas[1])
    
    if municipios: mask &= df['Município'].isin(municipios)
    if ais: mask &= df['AIS'].isin(ais)
    if tipos_droga: mask &= df['Tipo de Entorpecente'].isin(tipos_droga)
        
    return df[mask]
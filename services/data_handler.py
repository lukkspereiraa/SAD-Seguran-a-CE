import pandas as pd
import streamlit as st
import os

def tratar_datas_comuns(df):
    if df.empty: return df
    df['Data'] = pd.to_datetime(df['Data'])
    
    if 'Hora' in df.columns:
        df['Hora'] = df['Hora'].astype(str)
        df['Hora_Pico'] = df['Hora'].str.split(':').str[0]
        
    ordem_dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    if 'Dia da Semana' in df.columns:
        df['Dia da Semana'] = pd.Categorical(df['Dia da Semana'], categories=ordem_dias, ordered=True)
    return df

@st.cache_data
def carregar_dados(caminho_cvli='dataSett/CVLI_Agosto.xlsx', 
                   caminho_ent='dataSett/Entorpecentes.xlsx',
                   caminho_armas='dataSett/Arma-de-Fogo.xlsx',
                   caminho_salvamento='dataSett/Salvamento_Agosto.xlsx'): # <-- 4ª BASE AQUI
    
    if not os.path.exists(caminho_cvli):
        st.error(f"🚨 Erro Crítico: Banco '{caminho_cvli}' não encontrado.")
        st.stop()

    df_cvli = tratar_datas_comuns(pd.read_excel(caminho_cvli, sheet_name=0))
    df_cvli['Idade Numérica'] = pd.to_numeric(df_cvli['Idade da Vítima'], errors='coerce')
    df_cvli['Faixa Etária'] = pd.cut(
        df_cvli['Idade Numérica'], bins=[0, 17, 29, 59, 150], 
        labels=['0 a 17 anos', '18 a 29 anos', '30 a 59 anos', '60+ anos (Idosos)'], right=True
    ).cat.add_categories('Não Informada').fillna('Não Informada')

    df_ent = tratar_datas_comuns(pd.read_excel(caminho_ent, sheet_name=0)) if os.path.exists(caminho_ent) else pd.DataFrame()

    df_armas = tratar_datas_comuns(pd.read_excel(caminho_armas, sheet_name=0)) if os.path.exists(caminho_armas) else pd.DataFrame()
    if not df_armas.empty:
        df_armas['Quantidade'] = pd.to_numeric(df_armas['Quantidade'], errors='coerce').fillna(0)

    # NOVO: Processamento de Salvamento
    df_salvamento = tratar_datas_comuns(pd.read_excel(caminho_salvamento, sheet_name=0)) if os.path.exists(caminho_salvamento) else pd.DataFrame()

    # Agora a função retorna 4 bases!
    return df_cvli, df_ent, df_armas, df_salvamento

def filtrar_dados_cvli(df, datas, municipios, ais, meios, faixas, escolaridades, generos, naturezas):
    if df.empty: return df
    mask = (df['Data'].dt.date >= datas[0]) & (df['Data'].dt.date <= datas[1])
    filtros = {'Município': municipios, 'AIS': ais, 'Meio Empregado': meios, 'Faixa Etária': faixas, 'Escolaridade da Vítima': escolaridades, 'Gênero': generos, 'Natureza': naturezas}
    for coluna, valores in filtros.items():
        if valores: mask &= df[coluna].isin(valores)
    return df[mask]

def filtrar_dados_entorpecentes(df, datas, municipios, ais, tipos_droga):
    if df.empty: return df
    mask = (df['Data'].dt.date >= datas[0]) & (df['Data'].dt.date <= datas[1])
    if municipios: mask &= df['Município'].isin(municipios)
    if ais: mask &= df['AIS'].isin(ais)
    if tipos_droga: mask &= df['Tipo de Entorpecente'].isin(tipos_droga)
    return df[mask]

def filtrar_dados_armas(df, datas, municipios, ais):
    if df.empty: return df
    mask = (df['Data'].dt.date >= datas[0]) & (df['Data'].dt.date <= datas[1])
    if municipios: mask &= df['Município'].isin(municipios)
    if ais: mask &= df['AIS'].isin(ais)
    return df[mask]

# --- NOVA FUNÇÃO DE FILTRO: SALVAMENTO ---
def filtrar_dados_salvamento(df, datas, municipios, ais):
    if df.empty: return df
    mask = (df['Data'].dt.date >= datas[0]) & (df['Data'].dt.date <= datas[1])
    if municipios: mask &= df['Município'].isin(municipios)
    if ais: mask &= df['AIS'].isin(ais)
    return df[mask]
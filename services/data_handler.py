import pandas as pd
import streamlit as st
import os

@st.cache_data
def carregar_dados(caminho_arquivo='dataSett/CVLI_Agosto.xlsx'):
    try:
        # Verifica se o arquivo existe antes de tentar abrir
        if not os.path.exists(caminho_arquivo):
            st.error(f"🚨 Erro Crítico: O banco de dados '{caminho_arquivo}' não foi encontrado no servidor.")
            st.info("Verifique se a pasta 'dataSett' existe e contém a planilha correta.")
            st.stop() # Interrompe o painel graciosamente sem mostrar erros de código

        df_cvli = pd.read_excel(caminho_arquivo, sheet_name='CVLI')
        df_ip = pd.read_excel(caminho_arquivo, sheet_name='Intervenção Policial')
        df_up = pd.read_excel(caminho_arquivo, sheet_name='Unidade Prisional')
        
        # Tratamento de Datas e Idades
        df_cvli['Data'] = pd.to_datetime(df_cvli['Data'])
        df_cvli['Idade Numérica'] = pd.to_numeric(df_cvli['Idade da Vítima'], errors='coerce')
        
        # Criando Faixas Etárias
        bins = [0, 17, 29, 59, 150]
        labels = ['0 a 17 anos', '18 a 29 anos', '30 a 59 anos', '60+ anos (Idosos)']
        df_cvli['Faixa Etária'] = pd.cut(df_cvli['Idade Numérica'], bins=bins, labels=labels, right=True)
        df_cvli['Faixa Etária'] = df_cvli['Faixa Etária'].cat.add_categories('Não Informada').fillna('Não Informada')

        # Tratamento de Hora
        df_cvli['Hora'] = df_cvli['Hora'].astype(str)
        df_cvli['Hora_Pico'] = df_cvli['Hora'].str.split(':').str[0]
        
        ordem_dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        df_cvli['Dia da Semana'] = pd.Categorical(df_cvli['Dia da Semana'], categories=ordem_dias, ordered=True)
        
        return df_cvli, df_ip, df_up
        
    except Exception as e:
        st.error(f"🚨 Falha na leitura dos dados. Detalhes técnicos: {e}")
        st.stop()

# --- Função atualizada com o 9º argumento: "naturezas" ---
def filtrar_dados_cvli(df, datas, municipios, ais, meios, faixas, escolaridades, generos, naturezas):
    df_filtrado = df.copy()
    
    # Filtro de Data
    if len(datas) == 2:
        df_filtrado = df_filtrado[(df_filtrado['Data'].dt.date >= datas[0]) & (df_filtrado['Data'].dt.date <= datas[1])]
    
    # Filtros Categóricos
    if municipios:
        df_filtrado = df_filtrado[df_filtrado['Município'].isin(municipios)]
    if ais:
        df_filtrado = df_filtrado[df_filtrado['AIS'].isin(ais)]
    if meios:
        df_filtrado = df_filtrado[df_filtrado['Meio Empregado'].isin(meios)]
    if faixas:
        df_filtrado = df_filtrado[df_filtrado['Faixa Etária'].isin(faixas)]
    if escolaridades:
        df_filtrado = df_filtrado[df_filtrado['Escolaridade da Vítima'].isin(escolaridades)]
    if generos:
        df_filtrado = df_filtrado[df_filtrado['Gênero'].isin(generos)]
        
    # --- NOVO FILTRO DE NATUREZA AQUI ---
    if naturezas:
        df_filtrado = df_filtrado[df_filtrado['Natureza'].isin(naturezas)]
        
    return df_filtrado
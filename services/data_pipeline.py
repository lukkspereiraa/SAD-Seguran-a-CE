import pandas as pd

"""
Motor de transformação de dados (Pipeline ETL).
Aplica regras universais de formatação a qualquer Dataframe injetado.
"""

def aplicar_pipeline_transformacao(df):
    if df.empty: return df
    
    # A. Tratamento Universal de Tempo
    if 'Data' in df.columns:
        df['Data'] = pd.to_datetime(df['Data'])
        
    if 'Hora' in df.columns:
        df['Hora'] = df['Hora'].astype(str)
        df['Hora_Pico'] = df['Hora'].str.split(':').str[0]
        
    if 'Dia da Semana' in df.columns:
        ordem_dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        df['Dia da Semana'] = pd.Categorical(df['Dia da Semana'], categories=ordem_dias, ordered=True)
        
    # B. Tratamento Dinâmico de Demografia (Injeta colunas se 'Idade da Vítima' existir)
    if 'Idade da Vítima' in df.columns:
        df['Idade Numérica'] = pd.to_numeric(df['Idade da Vítima'], errors='coerce')
        df['Faixa Etária'] = pd.cut(
            df['Idade Numérica'], bins=[0, 17, 29, 59, 150], 
            labels=['0 a 17 anos', '18 a 29 anos', '30 a 59 anos', '60+ anos (Idosos)'], right=True
        ).cat.add_categories('Não Informada').fillna('Não Informada')
        
    # C. Tratamentos Específicos (Armas)
    if 'Quantidade' in df.columns:
        df['Quantidade'] = pd.to_numeric(df['Quantidade'], errors='coerce').fillna(0)
        
    return df
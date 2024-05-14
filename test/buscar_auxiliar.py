import pandas as pd
from collections import defaultdict, Counter

global resultado_formatado

import pandas as pd

def ler_planilha(caminho_arquivo, planilha_nome):
    df = pd.read_excel(caminho_arquivo, sheet_name=planilha_nome)
    df = df.drop(df.index[:7])
    return df

def extrair_colunas_interesse(df):
    atividade = df.iloc[:, 8]
    auxiliar = df.iloc[:, 16]
    return auxiliar, atividade

def criar_lista_tuplas(auxiliar, atividade):
    return [(a, b) for a, b in zip(auxiliar, atividade) if isinstance(a, str) and a.strip() != ""]

def get_auxiliar(caminho_arquivo):
    df = ler_planilha(caminho_arquivo, "Ordens de Serviço")
    auxiliar, atividade = extrair_colunas_interesse(df)
    return criar_lista_tuplas(auxiliar, atividade)




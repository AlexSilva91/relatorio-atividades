import pandas as pd
from collections import Counter, OrderedDict
from textwrap import wrap

def ler_planilha(caminho_arquivo, planilha_nome):
    df = pd.read_excel(caminho_arquivo, sheet_name=planilha_nome)
    df = df.drop(df.index[:7])
    return df

def extrair_colunas_interesse(df):
    atividade = df.iloc[:, 8]
    tecnico = df.iloc[:, 15]
    auxiliar = df.iloc[:, 16]
    return tecnico, auxiliar, atividade

def criar_lista_tuplas(tecnico, auxiliar, atividade):
    return list(zip(tecnico, auxiliar, atividade))

def contar_atividades_repetidas(lista):
    return Counter(lista)

def processar_tecnicos_auxiliar(lista_tuplas):
    tecnicos_auxiliar = {}

    for tecnico, auxiliar, atividade in lista_tuplas:
        if not isinstance(tecnico, str) or tecnico.strip() == "":
            continue

        # Adiciona o auxiliar associado a cada técnico
        if tecnico not in tecnicos_auxiliar:
            tecnicos_auxiliar[tecnico] = {"auxiliares": set(), "atividades": set()}

        if pd.notna(auxiliar):  # Verifica se o valor não é NaN
            tecnicos_auxiliar[tecnico]["auxiliares"].add(str(auxiliar))
            tecnicos_auxiliar[tecnico]["atividades"].add(str(atividade))

    return tecnicos_auxiliar

def processar_planilha(caminho, tecnicos_a_evitar):
    caminho_arquivo = caminho
    planilha_nome = "Ordens de Serviço"

    df = ler_planilha(caminho_arquivo, planilha_nome)
    tecnico, auxiliar, atividade = extrair_colunas_interesse(df)
    list_tuplas = criar_lista_tuplas(tecnico, auxiliar, atividade)

    tecnicos_auxiliar = processar_tecnicos_auxiliar(list_tuplas)

    for tecnico, info in tecnicos_auxiliar.items():
        if tecnico not in tecnicos_a_evitar:
            auxiliares_str = ', '.join(info["auxiliares"])
            atividades_str = ', '.join(info["atividades"])
            print(f"Técnico: {tecnico}, Auxiliares: {auxiliares_str}, Atividades: {atividades_str}")

# Lista de técnicos a evitar
lista_tecnicos_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]

# Uso da função com a lista de técnicos a evitar
processar_planilha("/home/alex/Downloads/ordemservico-2024-03-04-194647.xlsx", lista_tecnicos_a_evitar)

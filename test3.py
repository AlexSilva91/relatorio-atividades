import pandas as pd
from collections import Counter, defaultdict
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

def contar_atividades_por_auxiliar(lista_tuplas, tecnicos_a_evitar, auxiliares_a_evitar):
    contagem_por_auxiliar = defaultdict(Counter)
    contagem_total_por_tecnico = Counter()

    for tecnico, auxiliar, atividade in lista_tuplas:
        if not isinstance(tecnico, str) or tecnico.strip() == "":
            continue

        if tecnico in tecnicos_a_evitar or auxiliar in auxiliares_a_evitar:
            continue

        if pd.notna(auxiliar):  # Verifica se o valor não é NaN
            contagem_por_auxiliar[(tecnico, auxiliar)][atividade] += 1
            contagem_total_por_tecnico[tecnico] += 1

    return contagem_por_auxiliar, contagem_total_por_tecnico

def processar_planilha(caminho, tecnicos_a_evitar, auxiliares_a_evitar):
    caminho_arquivo = caminho
    planilha_nome = "Ordens de Serviço"

    df = ler_planilha(caminho_arquivo, planilha_nome)
    tecnico, auxiliar, atividade = extrair_colunas_interesse(df)
    list_tuplas = criar_lista_tuplas(tecnico, auxiliar, atividade)

    contagem_por_auxiliar, contagem_total_por_tecnico = contar_atividades_por_auxiliar(list_tuplas, tecnicos_a_evitar, auxiliares_a_evitar)

    for (tecnico, auxiliar), contagem_por_categoria in contagem_por_auxiliar.items():
        print(f"\nTécnico: {tecnico}, Auxiliar: {auxiliar}")
        for categoria, quantidade in contagem_por_categoria.items():
            print(f"  Categoria: {categoria}, Quantidade de Ajuda: {quantidade}")

        print(f"  Total de Serviços para {tecnico}: {contagem_total_por_tecnico[tecnico]}")

# Lista de técnicos a evitar
lista_tecnicos_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]

# Lista de auxiliares a evitar
lista_auxiliares_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]

# Uso das funções
caminho_arquivo = "/home/alex/Downloads/ordemservico-2024-03-04-194647.xlsx"
processar_planilha(caminho_arquivo, lista_tecnicos_a_evitar, lista_auxiliares_a_evitar)

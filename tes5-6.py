import pandas as pd
from collections import defaultdict, Counter

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
    vinculo_tecnico_auxiliares = defaultdict(set)
    contagem_por_auxiliar = defaultdict(Counter)

    for tecnico, auxiliar, atividade in lista_tuplas:
        if not isinstance(tecnico, str) or tecnico.strip() == "":
            continue

        if tecnico in tecnicos_a_evitar or auxiliar in auxiliares_a_evitar:
            continue

        if pd.notna(auxiliar):  # Verifica se o valor não é NaN
            vinculo_tecnico_auxiliares[tecnico].add(auxiliar)
            contagem_por_auxiliar[(tecnico, auxiliar)][atividade] += 1

    return dict(vinculo_tecnico_auxiliares), dict(contagem_por_auxiliar)

def gerar_dicionario(caminho_arquivo, tecnicos_a_evitar, auxiliares_a_evitar):
    planilha_nome = "Ordens de Serviço"
    df = ler_planilha(caminho_arquivo, planilha_nome)
    tecnico, auxiliar, atividade = extrair_colunas_interesse(df)
    list_tuplas = criar_lista_tuplas(tecnico, auxiliar, atividade)
    
    vinculo_tecnico_auxiliares, contagem_por_auxiliar = contar_atividades_por_auxiliar(list_tuplas, tecnicos_a_evitar, auxiliares_a_evitar)

    return {
        'vinculo_tecnico_auxiliares': vinculo_tecnico_auxiliares,
        'contagem_por_auxiliar': contagem_por_auxiliar
    }

# Lista de técnicos a evitar
lista_tecnicos_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]

# Lista de auxiliares a evitar
lista_auxiliares_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]

# Caminho para o arquivo de entrada
caminho_arquivo = "/home/alex/Downloads/ordemservico-2024-03-04-194647.xlsx"

# Uso da função para obter o dicionário
resultado_dict = gerar_dicionario(caminho_arquivo, lista_tecnicos_a_evitar, lista_auxiliares_a_evitar)

# Exibindo o dicionário
print(resultado_dict)

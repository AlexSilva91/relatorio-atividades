import pandas as pd
from collections import defaultdict, Counter
from datetime import datetime

def ler_planilha(caminho_arquivo, planilha_nome):
    df = pd.read_excel(caminho_arquivo, sheet_name=planilha_nome)
    df = df.drop(df.index[:7])
    return df

def extrair_colunas_interesse(df):
    atividade = df.iloc[:, 8]
    tecnico = df.iloc[:, 15]
    auxiliar = df.iloc[:, 16]
    data = pd.to_datetime(df.iloc[:, 14], errors='coerce').dt.date
    return tecnico, auxiliar, atividade, data

def criar_lista_tuplas(tecnico, auxiliar, atividade, data):
    return list(zip(tecnico, auxiliar, atividade, data))

def filtrar_por_datas(lista_tuplas, data_inicial, data_final):
    return [(tecnico, auxiliar, atividade, data) for tecnico, auxiliar, atividade, data in lista_tuplas if data_inicial <= data <= data_final]

def contar_atividades_por_auxiliar(lista_tuplas, tecnicos_a_evitar, auxiliares_a_evitar):
    vinculo_tecnico_auxiliares = defaultdict(set)
    contagem_por_auxiliar = defaultdict(Counter)

    for tecnico, auxiliar, atividade, _ in lista_tuplas:
        if not isinstance(tecnico, str) or tecnico.strip() == "":
            continue

        if tecnico in tecnicos_a_evitar or auxiliar in auxiliares_a_evitar:
            continue

        if pd.notna(auxiliar):  # Verifica se o valor não é NaN
            vinculo_tecnico_auxiliares[tecnico].add(auxiliar)
            contagem_por_auxiliar[(tecnico, auxiliar)][atividade] += 1

    return dict(vinculo_tecnico_auxiliares), dict(contagem_por_auxiliar)

def gerar_dicionario_formatado(caminho_arquivo, tecnicos_a_evitar, auxiliares_a_evitar, data_inicial=None, data_final=None):
    planilha_nome = "Ordens de Serviço"
    df = ler_planilha(caminho_arquivo, planilha_nome)
    tecnico, auxiliar, atividade, data = extrair_colunas_interesse(df)
    list_tuplas = criar_lista_tuplas(tecnico, auxiliar, atividade, data)
    
    if data_inicial and data_final:
        list_tuplas = filtrar_por_datas(list_tuplas, data_inicial, data_final)

    vinculo_tecnico_auxiliares, contagem_por_auxiliar = contar_atividades_por_auxiliar(list_tuplas, tecnicos_a_evitar, auxiliares_a_evitar)

    total_servicos = 0  # Inicializa o total de serviços

    resultado_formatado = ""
    for tecnico, auxiliares in vinculo_tecnico_auxiliares.items():
        resultado_formatado += f"Técnico: {tecnico}\n"
        for auxiliar in auxiliares:
            resultado_formatado += f"  Auxiliar: {auxiliar}\n"
            for atividade, quantidade in contagem_por_auxiliar.get((tecnico, auxiliar), {}).items():
                resultado_formatado += f"    Serviço: {atividade}, Quantidade: {quantidade}\n"
                total_servicos += quantidade  # Adiciona a quantidade ao total
        resultado_formatado += "\n"

    resultado_formatado += f"Total de serviços: {total_servicos}\n"  # Adiciona o total de serviços ao final do relatório

    return resultado_formatado, total_servicos, vinculo_tecnico_auxiliares, contagem_por_auxiliar


def get_resultado_formatado(caminho, data_inicial=None, data_final=None):
    # Lista de técnicos a evitar
    lista_tecnicos_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves", "NOC", "leandro.lacerda", "jonatas.thiago"]

    # Lista de auxiliares a evitar
    lista_auxiliares_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves", "NOC", "leandro.lacerda", "jonatas.thiago"]

    data_init = datetime.strptime(data_inicial, '%Y-%m-%d').date() if data_inicial else None
    data_end = datetime.strptime(data_final, '%Y-%m-%d').date() if data_final else None

    # Uso da função para obter a string formatada
    resultado_formatado, total_servicos, vinculo_tecnico_auxiliares, contagem_por_auxiliar = gerar_dicionario_formatado(caminho, lista_tecnicos_a_evitar, lista_auxiliares_a_evitar, data_init, data_end)
    
    return resultado_formatado, total_servicos, vinculo_tecnico_auxiliares, contagem_por_auxiliar
    

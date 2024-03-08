import pandas as pd
from collections import Counter, OrderedDict
from textwrap import wrap
from auxiliar_por_atividade import get_resultado_formatado
from buscar_auxiliar import get_auxiliar


def ler_planilha(caminho_arquivo, planilha_nome):
    df = pd.read_excel(caminho_arquivo, sheet_name=planilha_nome)
    df = df.drop(df.index[:7])
    return df

def extrair_colunas_interesse(df):
    tecnico = df.iloc[:, 15]
    atividade = df.iloc[:, 8]
    return tecnico, atividade

def criar_lista_tuplas(tecnico, atividade):
    return list(zip(tecnico, atividade))

def contar_atividades_repetidas(lista):
    return Counter(lista)

def processar_tecnicos_atividades(contagem_atividades, tecnicos_a_evitar):
    tecnicos_atividades = {}

    for (tecnico, atividade), contagem in contagem_atividades.items():
        if not isinstance(tecnico, str) or tecnico.strip() == "":
            continue

        if tecnico not in tecnicos_a_evitar:
            if tecnico not in tecnicos_atividades:
                tecnicos_atividades[tecnico] = {}

            tecnicos_atividades[tecnico][atividade] = contagem

    return OrderedDict(sorted(tecnicos_atividades.items()))

def remover_repeticao_auxiliar(lista_auxiliar, lista_auxiliar_proibido):
    # Filtra as atividades associadas aos técnicos que queremos evitar
    atividades_filtradas = [atividade for tecnico, atividade in lista_auxiliar if tecnico not in lista_auxiliar_proibido]

    # Obtém a quantidade total de atividades filtradas  
    total_atividades = len(atividades_filtradas)
    return total_atividades

def salvar_resultado_em_arquivo(tecnicos_atividades, total, total_ajuda , resultado_formatado):
    with open("resultado4.txt", "w") as arquivo:
        arquivo.write("-------------------------------------------------\n")
        arquivo.write("-----> Relatório de Atividades por Técnico <-----\n")
        arquivo.write("-------------------------------------------------")

        for tecnico, atividades in tecnicos_atividades.items():
            arquivo.write(f"\n********************************\nTécnico: {tecnico}\n********************************\n")

            total_por_tecnico = 0
            atividades = OrderedDict(sorted(atividades.items()))

            for atividade, contagem in atividades.items():
                texto_formatado = wrap(f"  {atividade}: {contagem}\n", width=70)
                arquivo.write("\n".join(texto_formatado) + "\n")

                total_por_tecnico += contagem
                total[0] += contagem

            contagem_str = f"{total_por_tecnico}"
            linhas = sorted([f"\n-----> Total: {contagem_str} <-----"], reverse=True)

            arquivo.write("\n".join(linhas) + "\n")
        total[0] -= total_ajuda
        arquivo.write(f"\n++++++++++++++++++++++++++++++++\n Total geral de atividade: {total[0]}\n++++++++++++++++++++++++++++++++\n")
        arquivo.write("\n-------------------------------------------------\n")
        arquivo.write(" ---> Relatório de Atividades por Auxiliar <----\n")
        arquivo.write("-------------------------------------------------\n")
        arquivo.write('\n'+resultado_formatado)

def processar_dados_planilha(caminho):
    # Uso das funções
    caminho_arquivo = caminho
    planilha_nome = "Ordens de Serviço"
    lista_tecnicos_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]

    df = ler_planilha(caminho_arquivo, planilha_nome)
    tecnico, atividade = extrair_colunas_interesse(df)
    lista_tuplas = criar_lista_tuplas(tecnico, atividade)
    
    # Adicionando as tuplas obtidas de get_auxiliar à lista_tuplas
    lista_auxiliar = get_auxiliar(caminho)
    lista_tuplas += lista_auxiliar
    total_ajuda = remover_repeticao_auxiliar(lista_auxiliar, lista_tecnicos_a_evitar)

    print(total_ajuda)
    contagem_atividades = contar_atividades_repetidas(lista_tuplas)
    total = [0]  # Usando uma lista para contornar a limitação do escopo

    tecnicos_atividades = processar_tecnicos_atividades(contagem_atividades, lista_tecnicos_a_evitar)

    salvar_resultado_em_arquivo(tecnicos_atividades, total, total_ajuda, get_resultado_formatado(caminho))


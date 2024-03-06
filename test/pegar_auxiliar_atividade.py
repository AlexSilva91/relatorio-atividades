import pandas as pd
from collections import Counter, OrderedDict
from textwrap import wrap
from test7 import gerar_dicionario

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

from collections import OrderedDict
from textwrap import wrap

def salvar_resultado_em_arquivo(tecnicos_atividades, vinculo_tecnico_auxiliares, contagem_por_auxiliar, total):
    with open("resultado.txt", "w") as arquivo:
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

            # Adiciona informações sobre auxiliares e atividades
            if tecnico in vinculo_tecnico_auxiliares:
                arquivo.write("\nAuxiliares:\n")
                for auxiliar in vinculo_tecnico_auxiliares[tecnico]:
                    arquivo.write(f"  {auxiliar}\n")

                    # Se o auxiliar for igual ao técnico, soma a quantidade de serviço
                    if auxiliar == tecnico and (tecnico, tecnico) in contagem_por_auxiliar:
                        aux_total = sum(contagem_por_auxiliar[(tecnico, tecnico)].values())
                        total[0] += aux_total
                        arquivo.write(f"    Serviço: {tecnico}, Quantidade: {aux_total}\n")
                    elif (tecnico, auxiliar) in contagem_por_auxiliar:
                        aux_total = sum(contagem_por_auxiliar[(tecnico, auxiliar)].values())
                        total[0] += aux_total
                        arquivo.write(f"    Serviço: {auxiliar}, Quantidade: {aux_total}\n")

        arquivo.write(f"++++++++++++++++++++++++++++++++\n Total geral de atividade: {total[0]}\n++++++++++++++++++++++++++++++++\n")

def processar_dados_planilha(caminho):
  # Uso das funções
  caminho_arquivo = caminho
  planilha_nome = "Ordens de Serviço"
  lista_tecnicos_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]
  lista_auxiliares_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]

  vinculo_tecnico_auxiliares, contagem_por_auxiliar = gerar_dicionario(caminho_arquivo, lista_tecnicos_a_evitar, lista_auxiliares_a_evitar)
  df = ler_planilha(caminho_arquivo, planilha_nome)
  tecnico, atividade = extrair_colunas_interesse(df)
  lista_tuplas = criar_lista_tuplas(tecnico, atividade)
  contagem_atividades = contar_atividades_repetidas(lista_tuplas)
  total = [0]  # Usando uma lista para contornar a limitação do escopo

  tecnicos_atividades = processar_tecnicos_atividades(contagem_atividades, lista_tecnicos_a_evitar)
  salvar_resultado_em_arquivo(tecnicos_atividades, vinculo_tecnico_auxiliares, contagem_por_auxiliar, total)

processar_dados_planilha("/home/alex/Downloads/ordemservico-2024-03-04-194647.xlsx")


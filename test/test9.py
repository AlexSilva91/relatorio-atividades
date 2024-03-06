import pandas as pd
from collections import Counter, OrderedDict, defaultdict
from textwrap import wrap
from test7 import gerar_dicionario
from auxiliar_por_atividade import get_resultado_formatado

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

def processar_tecnicos_atividades(contagem_atividades, tecnicos_a_evitar, vinculo_tecnico_auxiliares, contagem_por_auxiliar):
    tecnicos_atividades = defaultdict(lambda: {'atividades': Counter(), 'auxiliares': defaultdict(Counter)})

    for (tecnico, atividade), contagem in contagem_atividades.items():
        if not isinstance(tecnico, str) or tecnico.strip() == "":
            continue

        if tecnico not in tecnicos_a_evitar:
            tecnicos_atividades[tecnico]['atividades'][atividade] += contagem

            if tecnico in vinculo_tecnico_auxiliares:
                for auxiliar in vinculo_tecnico_auxiliares[tecnico]:
                    instancia = (tecnico, auxiliar)
                    if instancia in contagem_por_auxiliar:
                        dados_auxiliar = contagem_por_auxiliar[instancia]
                        tecnicos_atividades[tecnico]['auxiliares'][auxiliar] += dados_auxiliar

    return tecnicos_atividades

def salvar_resultado_em_arquivo(tecnicos_atividades, total, resultado_formatado):
    with open("resultado3.txt", "w") as arquivo:
        arquivo.write("-------------------------------------------------\n")
        arquivo.write("-----> Relatório de Atividades por Técnico <-----\n")
        arquivo.write("-------------------------------------------------")

        arquivo.write(resultado_formatado)

        for tecnico, dados_tecnico in tecnicos_atividades.items():
            arquivo.write(f"\n********************************\nTécnico: {tecnico}\n********************************\n")

            # Adiciona informações sobre as atividades do técnico principal
            total_por_tecnico = 0
            atividades = OrderedDict(sorted(dados_tecnico['atividades'].items()))

            for atividade, contagem in atividades.items():
                texto_formatado = wrap(f"  {atividade}: {contagem}\n", width=70)
                arquivo.write("\n".join(texto_formatado) + "\n")

                total_por_tecnico += contagem
                total[0] += contagem

            # Adiciona informações sobre auxiliares e atividades
            if tecnico in dados_tecnico['auxiliares']:
                arquivo.write("\nAuxiliares:\n")
                for auxiliar, dados_auxiliar in dados_tecnico['auxiliares'].items():
                    arquivo.write(f"  {auxiliar}\n")

                    aux_total = sum(dados_auxiliar.values())
                    total[0] += aux_total
                    arquivo.write(f"    Serviço: {auxiliar}, Categorias:\n")
                    for categoria, quantidade in dados_auxiliar.items():
                        arquivo.write(f"      {categoria}: {quantidade}\n")

            contagem_str = f"{total_por_tecnico}"
            linhas = sorted([f"\n-----> Total: {contagem_str} <-----"], reverse=True)

            arquivo.write("\n".join(linhas) + "\n")

        arquivo.write(f"++++++++++++++++++++++++++++++++\n Total geral de atividade: {total[0]}\n++++++++++++++++++++++++++++++++\n")
        arquivo.write("-------------------------------------------------\n")
        arquivo.write(" ---> Relatório de Atividades por Auxiliar <----\n")
        arquivo.write("-------------------------------------------------")
        arquivo.write(resultado_formatado)

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

    tecnicos_atividades = processar_tecnicos_atividades(contagem_atividades, lista_tecnicos_a_evitar, vinculo_tecnico_auxiliares, contagem_por_auxiliar)

    # Obter a string formatada
    resultado_formatado = get_resultado_formatado(caminho)
    salvar_resultado_em_arquivo(tecnicos_atividades, total, resultado_formatado)


processar_dados_planilha("/home/alex/Downloads/ordemservico-2024-03-04-194647.xlsx")


import pandas as pd
from datetime import datetime
from collections import Counter, OrderedDict
from auxiliar_por_atividade import get_resultado_formatado

def ler_planilha(caminho_arquivo, planilha_nome):
    df = pd.read_excel(caminho_arquivo, sheet_name=planilha_nome)
    df = df.drop(df.index[:7])
    return df

def extrair_colunas_interesse(df):
    atividade = df.iloc[:, 8]
    data = pd.to_datetime(df.iloc[:, 14], errors='coerce').dt.date
    tecnico = df.iloc[:, 15]
    return tecnico, atividade, data

def criar_lista_tuplas(tecnico, atividade, data):
    return list(zip(tecnico, atividade, data))

def filtrar_atividades_por_data(data_inicial, data_final, lista_tuplas):
    data_inicial_com_horario = datetime.combine(data_inicial, datetime.min.time())
    data_final_com_horario = datetime.combine(data_final, datetime.max.time())

    atividades_filtradas = []
    for tupla in lista_tuplas:
        # Convertendo tupla[2] para datetime.datetime
        data_tupla = datetime.combine(tupla[2], datetime.min.time())

        if data_inicial_com_horario <= data_tupla <= data_final_com_horario:
            # Extrair nome do técnico e atividade
            nome_tecnico, atividade, _ = tupla
            atividades_filtradas.append((nome_tecnico, atividade))
    return atividades_filtradas

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

def atualizar_tecnico_atividades(contagem_por_auxiliar, tecnico_atividades):
    for auxiliar, atividades in contagem_por_auxiliar.items():
        tecnico = auxiliar[-1]  # Obtém o último elemento (nome do técnico)
        if tecnico in tecnico_atividades:
            for atividade, quantidade in atividades.items():
                if atividade in tecnico_atividades[tecnico]:
                    # Atualiza a quantidade da atividade existente
                    tecnico_atividades[tecnico][atividade] += quantidade
                else:
                    # Adiciona uma nova atividade
                    tecnico_atividades[tecnico][atividade] = quantidade
        else:
            # Adiciona um novo registro para o técnico
            tecnico_atividades[tecnico] = atividades

    return tecnico_atividades


def salvar_em_txt(tecnicos_atividades, data_inicial, data_final, resultado_formatado, total_servicos):
    data_init_str = data_inicial.strftime('%Y-%m-%d')
    data_end_str = data_final.strftime('%Y-%m-%d')

    with open(f"Relatório_{data_init_str}_{data_end_str}.txt", "w") as arquivo_saida:
        total_geral = 0
        arquivo_saida.write("-------------------------------------------------\n")
        arquivo_saida.write("-----> Relatório de Atividades por Técnico <-----\n")
        arquivo_saida.write("-------------------------------------------------\n")
        for tecnico, atividades in tecnicos_atividades.items():
            arquivo_saida.write(f"\n********************************\nTécnico: {tecnico}\n********************************\n")
            total_atividades_tecnico = sum(atividades.values())
            total_geral += total_atividades_tecnico  # Adiciona o total do técnico ao total geral
            arquivo_saida.write(f"\n++++++++++++++++++++++++\nTotal de atividades: {total_atividades_tecnico}\n++++++++++++++++++++++++\n")
            for atividade, contagem in atividades.items():
                arquivo_saida.write(f"- Atividade: {atividade} = {contagem}\n")
            arquivo_saida.write("\n")  # Adicione uma linha em branco entre cada técnico
        
        arquivo_saida.write(f"********************************\nTotal geral de atividades: {total_geral-total_servicos}\n********************************\n")
        arquivo_saida.write("--------------------------------------------\n")
        arquivo_saida.write("-----> Relatório de ajuda por Técnico <-----\n")
        arquivo_saida.write("--------------------------------------------\n")
        arquivo_saida.write(f"{resultado_formatado}\n")

def processar_dados_planilha(caminho, data_init, data_end):

    data_inicial = data_init
    data_final = data_end

    data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d')
    data_final = datetime.strptime(data_final, '%Y-%m-%d')
    #chama Acess
    resultado_formatado, total_servicos, vinculo_tecnico_auxiliares, contagem_por_auxiliar = get_resultado_formatado(caminho, data_init, data_end)


    lista_tecnicos_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves", "NOC", "leandro.lacerda", "jonatas.thiago"]

    df = ler_planilha(caminho, "Ordens de Serviço")
    tecnico, atividade, data = extrair_colunas_interesse(df)
    lista_tuplas = criar_lista_tuplas(tecnico, atividade, data)
    
    # Aqui, passamos diretamente os objetos datetime para a função filtrar_atividades_por_data
    tupla_result = filtrar_atividades_por_data(data_inicial, data_final, lista_tuplas)
    
    contagem_atividades = contar_atividades_repetidas(tupla_result)

    tecnicos_atividades = processar_tecnicos_atividades(contagem_atividades, lista_tecnicos_a_evitar)

    tecnico_atividades_atualizado = atualizar_tecnico_atividades(contagem_por_auxiliar, tecnicos_atividades)

    # Salvar os dados no arquivo de texto
    salvar_em_txt(tecnico_atividades_atualizado, data_inicial, data_final, resultado_formatado, total_servicos)


#caminho_arquivo = "/home/alex/Downloads/ordemservico-2024-05-07-202826.xlsx"
#processar_dados_planilha(caminho_arquivo, data_inicial, data_final)

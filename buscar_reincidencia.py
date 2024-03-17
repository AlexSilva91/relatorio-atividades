import pandas as pd
from datetime import datetime


def ler_planhilha(caminho_arquivo, planilha_nome):
  try:
    df = pd.read_excel(caminho_arquivo, sheet_name=planilha_nome)
    df = df.drop(df.index[:7])
    return df
  except FileNotFoundError:
    print("O arquivo especificado não pôde ser encontrado.")
    return None
    
def extrair_colunas_interesse(df):
  contrato = df.iloc[:, 2]
  atividade = df.iloc[:, 8].str.lower()
  data = pd.to_datetime(df.iloc[:, 14], errors='coerce')
  tecnico = df.iloc[:, 15]
  return tecnico, contrato, atividade, data

def gerar_dicionario(tecnico, contrato, atividade, data):
    # Criando o dicionário
    dados_contratos = {}
    for cont, atv, dt, tec in zip(contrato, atividade, data, tecnico):
        if isinstance(tec, str) and tec.strip() != '':  
            # Verifica se o técnico é uma string não vazia e diferente de 'nam'
            if cont not in dados_contratos:
                dados_contratos[cont] = []
            dados_contratos[cont].append({'atividade': atv, 'data': dt, 'tecnico': tec})
    return dados_contratos

def filtrar_atividades(dados_contratos, atividades_a_exibir):
    # Dicionário para armazenar os contratos com as atividades filtradas
    dados_filtrados = {}
    # Iterar sobre cada contrato no dicionário
    for contrato, atividades in dados_contratos.items():
        # Lista para armazenar as atividades filtradas para este contrato
        atividades_filtradas = []
        # Iterar sobre as atividades deste contrato
        for atividade in atividades:
            if atividade['atividade'].lower() in atividades_a_exibir:
                # Se a atividade estiver na lista de atividades a serem exibidas, adicioná-la à lista de atividades filtradas
                atividades_filtradas.append(atividade)
        # Se houver atividades filtradas para este contrato, adicionar ao dicionário de dados filtrados
        if atividades_filtradas:
            dados_filtrados[contrato] = atividades_filtradas
    return dados_filtrados

def consolidar_contratos(dados_filtrados):
    # Dicionário para armazenar os contratos consolidados
    contratos_consolidados = {}
    # Iterar sobre cada contrato no dicionário filtrado
    for contrato, atividades in dados_filtrados.items():
        # Se o contrato já estiver no dicionário consolidado, apenas adicione as atividades a ele
        if contrato in contratos_consolidados:
            contratos_consolidados[contrato]['atividades'].extend(atividades)
        else:
            # Caso contrário, crie uma nova entrada no dicionário consolidado
            contratos_consolidados[contrato] = {'atividades': atividades}

    return contratos_consolidados

def filtrar_contratos(contratos_consolidados, atividades_a_exibir):
    # Dicionário para armazenar os contratos filtrados
    contratos_filtrados = {}

    # Iterar sobre cada contrato no dicionário consolidado
    for contrato, info in contratos_consolidados.items():
        # Verificar se o contrato possui mais de uma atividade
        if len(info['atividades']) > 1:
            # Lista para armazenar as atividades filtradas para este contrato
            atividades_filtradas = []
            # Iterar sobre as atividades deste contrato
            for atividade in info['atividades']:
                # Verificar se a atividade está na lista de atividades a serem exibidas
                if atividade['atividade'].lower() in atividades_a_exibir:
                    atividades_filtradas.append(atividade)
            # Se houver atividades filtradas para este contrato, adicionar ao dicionário de contratos filtrados
            if atividades_filtradas:
                contratos_filtrados[contrato] = {'atividades': atividades_filtradas}
    return contratos_filtrados

def salvar_contratos_em_txt(contratos_filtrados, nome_arquivo):
    try:
        # Abrir o arquivo de texto para escrita
        with open(nome_arquivo, 'w') as arquivo:
            # Variável para contar o número de contratos impressos
            num_contratos_impressos = 0
            # Iterar sobre os contratos filtrados
            for contrato, info in contratos_filtrados.items():
                # Verificar se o contrato possui mais de uma atividade
                if len(info['atividades']) > 1:
                    arquivo.write(f"Contrato: {contrato}\n")
                    arquivo.write("Atividades:\n")
                    # Iterar sobre as atividades do contrato
                    for atividade in info['atividades']:
                        arquivo.write(f"Atividade: {atividade['atividade']}, Data: {atividade['data']}, Técnico: {atividade['tecnico']}\n")
                    arquivo.write("\n")  # Adicionar uma linha em branco entre os contratos
                    num_contratos_impressos += 1
            
            # Escrever a quantidade total de contratos impressos no arquivo
            arquivo.write(f"-----------------------------------------------\nTotal de contratos impressos: {num_contratos_impressos}\n-----------------------------------------------")
    except Exception as e:
        print(f"Ocorreu um erro ao salvar as informações dos contratos no arquivo: {e}")


caminho_arquivo = "/home/alex/Downloads/ordemservico-2024-03-07-230029.xlsx"
planilha_nome = "Ordens de Serviço"
atividades_a_exibir = ["suporte externo", "corretiva"]

df = ler_planhilha(caminho_arquivo, planilha_nome)
tecnico, contrato, atividade, data = extrair_colunas_interesse(df)
dados_contratos = gerar_dicionario(tecnico, contrato, atividade, data)
dados_filtrados = filtrar_atividades(dados_contratos, atividades_a_exibir)
consolidar_contratos = consolidar_contratos(dados_contratos)
contratos_filtrados = filtrar_contratos(consolidar_contratos, atividades_a_exibir)

salvar_contratos_em_txt(contratos_filtrados, 'contratos.txt')


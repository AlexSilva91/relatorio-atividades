import pandas as pd
import logging

global PLANILHA_NOME
PLANILHA_NOME = "Ordens de Serviço"

def contar_colunas(caminho_arquivo, planilha_nome):
    """
    Conta o número total de colunas em uma planilha Excel.

    Args:
        caminho_arquivo (str): Caminho do arquivo Excel.
        planilha_nome (str): Nome da planilha a ser lida.

    Returns:
        int: Número total de colunas na planilha.
    """
    logging.info(f"Lendo a planilha: {caminho_arquivo}, Planilha: {planilha_nome}")
    df = pd.read_excel(caminho_arquivo, sheet_name=planilha_nome)
    numero_colunas = df.shape[1]
    logging.info(f"Total de colunas: {numero_colunas}")
    return numero_colunas

def validation_legth_sheet(caminho):
    global PLANILHA_NOME
    number = contar_colunas(caminho, PLANILHA_NOME)
    if number == 22:
        return True
    else:
        return False


#print(validation_legth_sheet("/home/alex/Downloads/ordemservico-2024-12-21-153345.xlsx"))
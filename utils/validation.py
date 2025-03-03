import pandas as pd
import logging
<<<<<<< HEAD
from utils.log import get_log_file_path
=======
>>>>>>> c2f76c2a2615472f5536ca8879bbf1e85308fe2c

global PLANILHA_NOME
PLANILHA_NOME = "Ordens de Serviço"

<<<<<<< HEAD
log_file = get_log_file_path()

=======
# Criação de um logger centralizado
logger = logging.getLogger(__name__)

# Configuração do logging para salvar em arquivo e exibir no console
>>>>>>> c2f76c2a2615472f5536ca8879bbf1e85308fe2c
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    handlers=[
<<<<<<< HEAD
        logging.FileHandler(log_file),
        logging.StreamHandler()
=======
        logging.FileHandler(".logs.log"),  # Salva logs em 'api_logs.log'
        logging.StreamHandler()  # Exibe logs no console também
>>>>>>> c2f76c2a2615472f5536ca8879bbf1e85308fe2c
    ]
)

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
<<<<<<< HEAD
    if number <= 26:
=======
    if number == 22:
>>>>>>> c2f76c2a2615472f5536ca8879bbf1e85308fe2c
        return True
    else:
        return False
    
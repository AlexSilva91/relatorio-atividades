import pandas as pd

# Definir o nome do arquivo Excel
nome_arquivo = 'relatorio.xlsx'

# Definir o nome da planilha que você deseja acessar
nome_planilha = 'Relatorio'

# Leitura da planilha específica
df = pd.read_excel(nome_arquivo, sheet_name=nome_planilha)

# Selecionar a coluna que você deseja analisar
coluna_analise = df['Tecnico']

# Criar um conjunto para armazenar os nomes sem repetições
nomes_unicos = set(coluna_analise.str.upper())

# Ordenar os nomes em ordem alfabética
nomes_unicos = sorted(nomes_unicos)

# Salvar os nomes em um arquivo TXT
with open('nomes_unicos.txt', 'w') as arquivo:
    for nome in nomes_unicos:
        arquivo.write(nome + '\n')


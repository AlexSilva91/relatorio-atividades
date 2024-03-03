import pandas as pd

# Definindo o nome do arquivo Excel
nome_arquivo = "relatorio.xlsx"
nome_planilha = 'Relatorio'

# Lendo a planilha
df = pd.read_excel(nome_arquivo, sheet_name=nome_planilha)

# Criando um dicionário para armazenar os resultados
tecnicos_atividades = {}
for tecnico in df["Tecnico"].unique():
    tecnicos_atividades[tecnico] = {}

# Percorrendo cada linha da planilha
for i in range(df.shape[0]):
    # Acessando o nome do técnico e a atividade
    tecnico = df.loc[i, "Tecnico"]
    atividade = df.loc[i, "Atividade"]
    
    # Contando a repetição de cada atividade para cada técnico
    if atividade not in tecnicos_atividades[tecnico]:
        tecnicos_atividades[tecnico][atividade] = 0
    tecnicos_atividades[tecnico][atividade] += 1

# Imprimindo os resultados
for tecnico, atividades in tecnicos_atividades.items():
    print(f"Técnico: {tecnico}")
    for atividade, contagem in atividades.items():
        print(f"    {atividade}: {contagem}")
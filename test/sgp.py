import pandas as pd

# Definindo o nome do arquivo Excel
nome_arquivo = "ordemservico-2024-03-01-232651.xlsx"
planilha = "Ordens de Serviço"

# Lendo a planilha
df = pd.read_excel(nome_arquivo, sheet_name=planilha)
df = df.drop(df.index[:])

# Criando um dicionário para armazenar os resultados
tecnicos_atividades = {}
for tecnico in df["Responsavel"].unique():
    tecnicos_atividades[tecnico] = {}

# Percorrendo cada linha da planilha
for i in range(df.shape[0]):
    # Acessando o nome do técnico e a atividade
    tecnico = df.loc[i, "Responsavel"]
    atividade = df.loc[i, "Motivo"]
    
    # Contando a repetição de cada atividade para cada técnico
    if atividade not in tecnicos_atividades[tecnico]:
        tecnicos_atividades[tecnico][atividade] = 0
    tecnicos_atividades[tecnico][atividade] += 1

# Imprimindo os resultados
for tecnico, atividades in tecnicos_atividades.items():
    print(f"Técnico: {tecnico}")
    for atividade, contagem in atividades.items():
        print(f"    {atividade}: {contagem}")

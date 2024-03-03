import pandas as pd
from collections import Counter
from textwrap import wrap

# Definindo o nome do arquivo Excel
nome_arquivo = "ordemservico-2024-03-01-232651.xlsx"
planilha = "Ordens de Serviço"

# Lendo a planilha
df = pd.read_excel(nome_arquivo, sheet_name=planilha)
df = df.drop(df.index[:7])

# Extraindo as colunas de interesse
tecnico = df.iloc[:, 15]
atividade = df.iloc[:, 8]

# Criando uma lista de tuplas (técnico, atividade)
lista = list(zip(tecnico, atividade))

# Lista de técnicos a evitar
lista_de_tecnicos_a_evitar = ["nan", "tiago.peres", "eguinailson.nunes"]

# Criando um dicionário para armazenar os resultados
tecnicos_atividades = {}

# Criando um objeto Counter para contar as repetições em "lista"
contagem_atividades = Counter(lista)

# Percorrendo as contagens de atividades
for (tecnico, atividade), contagem in contagem_atividades.items():
    # Ignora valores que não são nomes de técnicos
    if not isinstance(tecnico, str) or tecnico.strip() == "":
        continue

    # Ignora técnicos na lista "lista_de_tecnicos_a_evitar"
    if tecnico not in lista_de_tecnicos_a_evitar:
        # Adicionando o técnico ao dicionário se não existir
        if tecnico not in tecnicos_atividades:
            tecnicos_atividades[tecnico] = {}

        # Armazenando a contagem da atividade para o técnico
        tecnicos_atividades[tecnico][atividade] = contagem

# Salvando a saída em um arquivo TXT
with open("resultado.txt", "w") as arquivo:

    # Imprima o título do relatório
    arquivo.write("Relatório de Atividades por Técnico\n")
    arquivo.write("-------------------------------------------------\n")

    # Percorra os técnicos e suas atividades
    for tecnico, atividades in tecnicos_atividades.items():
        arquivo.write(f"\nTécnico: {tecnico}\n")
        for atividade, contagem in atividades.items():
            texto_formatado = wrap(f"  {atividade}: {contagem}\n", width=70)
            arquivo.write("\n".join(texto_formatado) + "\n")
        arquivo.write("-------------------------------------------------")

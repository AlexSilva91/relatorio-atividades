
# Suas listas
tecnico = ["Tecnico1", "Tecnico2", "Tecnico3"]
atividade = ["Atividade1", "Atividade2", "Atividade3"]

# Lista resultante do zip
lista_inicial = list(zip(tecnico, atividade))

# Adicionando mais dados a cada tupla
lista_modificada = []

for tupla in lista_inicial:
    tecnico, atividade = tupla  # Desempacotando a tupla

    # Adicionando mais dados, por exemplo, uma descrição
    descricao = f"Descrição para a atividade {atividade} realizada por {tecnico}"

    # Criando uma nova tupla com os dados adicionados
    tupla_modificada = (tecnico, atividade, descricao)

    # Adicionando a nova tupla à lista modificada
    lista_modificada.append(tupla_modificada)

# Exemplo de saída da lista modificada
for tupla in lista_modificada:
    print(tupla)


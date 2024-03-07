import pandas as pd
from collections import Counter, OrderedDict
from textwrap import wrap
from auxiliar_por_atividade import get_resultado_formatado
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

def salvar_resultado_em_arquivo(tecnicos_atividades, total, resultado_formatado, txt_filename="resultado4.txt"):
    with open(txt_filename, "w") as arquivo:
        arquivo.write("-------------------------------------------------\n")
        arquivo.write("-----> Relatório de Atividades por Técnico <-----\n")
        arquivo.write("-------------------------------------------------")

        for tecnico, atividades in tecnicos_atividades.items():
            arquivo.write(f"\n********************************\nTécnico: {tecnico}\n********************************\n")

            total_por_tecnico = 0
            atividades = OrderedDict(sorted(atividades.items()))

            for atividade, contagem in atividades.items():
                texto_formatado = wrap(f"  {atividade}: {contagem}\n", width=70)
                arquivo.write("\n".join(texto_formatado) + "\n")

                total_por_tecnico += contagem
                total[0] += contagem

                # Adicione uma nova linha para evitar quebras de linha no PDF
                arquivo.write("\n")

            contagem_str = f"{total_por_tecnico}"
            linhas = sorted([f"\n-----> Total: {contagem_str} <-----"], reverse=True)

            arquivo.write("\n".join(linhas) + "\n")

        arquivo.write(f"\n++++++++++++++++++++++++++++++++\n Total geral de atividade: {total[0]}\n++++++++++++++++++++++++++++++++\n")
        arquivo.write("\n-------------------------------------------------\n")
        arquivo.write(" ---> Relatório de Atividades por Auxiliar <----\n")
        arquivo.write("-------------------------------------------------\n")
        arquivo.write('\n'+resultado_formatado)

def salvar_resultado_em_arquivo_PDF(tecnicos_atividades, pdf_filename="resultado4.pdf"):
    pdf_canvas = canvas.Canvas(pdf_filename, pagesize=letter)

    pdf_canvas.drawString(100, 790, "Relatório de Atividades por Técnico")
    pdf_canvas.drawString(100, 785, "----------------------------------")

    y_position = 760
    for tecnico, atividades in tecnicos_atividades.items():
        pdf_canvas.drawString(100, y_position, f"Técnico: {tecnico}")
        pdf_canvas.drawString(100, y_position+1, f"----------------------------------")
        y_position -= 15

        total_por_tecnico = 0
        atividades = OrderedDict(sorted(atividades.items()))

        for atividade, contagem in atividades.items():
            texto_formatado = wrap(f"  {atividade}: {contagem}", width=70)
            for line in texto_formatado:
                pdf_canvas.drawString(120, y_position, line)
                y_position -= 15

            total_por_tecnico += contagem

            # Verifica se precisa mudar para a próxima coluna ou adicionar uma nova página
            if y_position <= 30:
                pdf_canvas.showPage()  # Adiciona uma nova página
                y_position = 780

        pdf_canvas.drawString(120, y_position, f"-----> Total: {total_por_tecnico} <-----")
        y_position -= 15

    pdf_canvas.save()

def processar_dados_planilha(caminho):
    caminho_arquivo = caminho
    planilha_nome = "Ordens de Serviço"
    lista_tecnicos_a_evitar = ["tiago.peres", "eguinailson.nunes", "evandro.zuza", "geimerson.alves"]

    df = ler_planilha(caminho_arquivo, planilha_nome)
    tecnico, atividade = extrair_colunas_interesse(df)
    lista_tuplas = criar_lista_tuplas(tecnico, atividade)
    contagem_atividades = contar_atividades_repetidas(lista_tuplas)
    total = [0]

    tecnicos_atividades = processar_tecnicos_atividades(contagem_atividades, lista_tecnicos_a_evitar)
    resultado_formatado = get_resultado_formatado(caminho)

    salvar_resultado_em_arquivo(tecnicos_atividades, total, resultado_formatado)
    salvar_resultado_em_arquivo_PDF(tecnicos_atividades)

# Exemplo de uso
processar_dados_planilha("/home/alex/Downloads/ordemservico-2024-03-06-105404.xlsx")

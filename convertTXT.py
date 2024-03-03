import PyPDF2
from PyPDF2 import Page, Font  # Importar classes Page e Font do PyPDF2
from textwrap import wrap

def converter_txt_para_pdf(caminho_arquivo_txt, caminho_arquivo_pdf, 
                          tamanho_fonte=12, nome_fonte="Helvetica", 
                          margem_esquerda=20, margem_superior=20):
  """
  Converte um arquivo TXT para PDF, preservando a formatação original do texto.

  Args:
      caminho_arquivo_txt (str): Caminho para o arquivo TXT.
      caminho_arquivo_pdf (str): Caminho para o arquivo PDF de saída.
      tamanho_fonte (int): Tamanho da fonte a ser utilizada no PDF (opcional).
      nome_fonte (str): Nome da fonte a ser utilizada no PDF (opcional).
      margem_esquerda (int): Margem esquerda da página em pixels (opcional).
      margem_superior (int): Margem superior da página em pixels (opcional).
  """

  # Abrindo o arquivo TXT em modo leitura
  with open(caminho_arquivo_txt, "r") as arquivo_txt:
    texto = arquivo_txt.read()

  # Criando um objeto PDFWriter
  pdf_writer = PyPDF2.PdfWriter()

  # Criando um objeto Page
  pdf_page = Page()

  # Adicionando a página ao PDFWriter
  pdf_writer.addPage(pdf_page)

  # Definindo a fonte e o tamanho da letra
  pdf_font = Font(nome_fonte, size=tamanho_fonte)

  # Definindo as margens da página
  pdf_page.setMargins(left=margem_esquerda, top=margem_superior)

  # Coordenadas para escrever o texto na página
  x = margem_esquerda
  y = pdf_page.getPageSize()[1] - margem_superior

  # Percorrendo o texto e escrevendo no PDF
  for linha in texto.splitlines():
    # Quebrando a linha em várias linhas se necessário
    linhas_formatadas = wrap(linha, width=70)

    for linha_formatada in linhas_formatadas:
      # Escrevendo a linha no PDF
      pdf_page.drawString(x, y, linha_formatada, font=pdf_font)

      # Ajustando a posição vertical para a próxima linha
      y -= pdf_font.size

  # Salvando o PDF
  with open(caminho_arquivo_pdf, "wb") as arquivo_pdf:
    pdf_writer.write(arquivo_pdf)

# Exemplo de uso
caminho_arquivo_txt = "resultado1.txt"
caminho_arquivo_pdf = "caminho_do_arquivo.pdf"

converter_txt_para_pdf(caminho_arquivo_txt, caminho_arquivo_pdf)

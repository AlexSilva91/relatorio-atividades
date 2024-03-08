from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def salvar_relatorio_em_pdf(texto_completo, caminho_pdf):
    # Configuração da página
    largura, altura = letter
    margem = 30
    altura_linha = 12

    pdf = canvas.Canvas(caminho_pdf, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    # Quebra o texto por linhas
    linhas = texto_completo.split('\n')

    # Configurações de posição inicial
    x, y = margem, altura - margem

    for linha in linhas:
        if y < margem + altura_linha:
            pdf.showPage()  # Adiciona uma nova página se não houver espaço suficiente
            y = altura - margem

        pdf.drawString(x, y, linha)
        y -= altura_linha  # Desce 12 unidades para a próxima linha

    pdf.save()

# Texto completo
texto_completo = """
-------------------------------------------------
Relatório de Atividades por Técnico 
-------------------------------------------------
********************************
Técnico: adriano.teodoro
********************************
  ATIVAÇÃO: 11
  CANCELAMENTO: 13
  Mudança Endereço: 1
  OURINETV: 3
  REATIVAÇÃO: 1
  RETIRADA: 20
  SUPORTE EXTERNO: 52
  SUPORTE INTERNO: 2
  TRANSFERÊNCIA: 7
  UPGRADE: 1

-----> Total: 111 <-----

********************************
Técnico: gracione.cavalcanti
********************************
  ATIVAÇÃO: 17
  CANCELAMENTO: 8
  Corretiva: 1
  FINANCEIRO: 2
  INFRAESTRUTURA: 1
  MIGRAÇÃO: 1
  REATIVAÇÃO: 2
  RETIRADA: 5
  SUPORTE EXTERNO: 63
  SUPORTE INTERNO: 1
  TRANSFERÊNCIA: 8
  UPGRADE: 1

-----> Total: 110 <-----

********************************
Técnico: jackson.mendes
********************************
  ATIVAÇÃO: 6
  CANCELAMENTO: 1
  INFRAESTRUTURA: 1
  Mudança Endereço: 1
  RETIRADA: 8
  SUPORTE EXTERNO: 59
  SUPORTE INTERNO: 2
  TRANSFERÊNCIA: 5

-----> Total: 83 <-----

********************************
Técnico: joao.neto
********************************
  ATIVAÇÃO: 5
  Financeiro: 2
  INFRAESTRUTURA: 4
  Instalação de KIT: 1
  RETIRADA: 8
  SUPORTE EXTERNO: 57
  SUPORTE INTERNO: 3
  TRANSFERÊNCIA: 1
  UPGRADE: 1

-----> Total: 82 <-----

********************************
Técnico: joel.pedro
********************************
  ATIVAÇÃO: 20
  CANCELAMENTO: 8
  Corretiva: 1
  FINANCEIRO: 1
  MIGRAÇÃO: 1
  Mudança Endereço: 1
  OURINETV: 1
  RETIRADA: 10
  SUPORTE EXTERNO: 62
  TRANSFERÊNCIA: 10
  UPGRADE: 5

-----> Total: 120 <-----

********************************
Técnico: jose.welder
********************************
  ATIVAÇÃO: 9
  CANCELAMENTO: 4
  FINANCEIRO: 1
  OURINETV: 2
  REATIVAÇÃO: 1
  RETIRADA: 11
  SUPORTE EXTERNO: 65
  TRANSFERÊNCIA: 10
  UPGRADE: 3

-----> Total: 106 <-----

********************************
Técnico: luiz.carlos
********************************
  ATIVAÇÃO: 10
  CANCELAMENTO: 8
  OURINETV: 1
  REATIVAÇÃO: 1
  RETIRADA: 19
  SUPORTE EXTERNO: 28
  TRANSFERÊNCIA: 7
  UPGRADE: 5

-----> Total: 79 <-----

********************************
Técnico: rogerio.sobreira
********************************
  ATIVAÇÃO: 8
  CANCELAMENTO: 15
  FINANCEIRO: 1
  Mudança Endereço: 1
  OURINETV: 1
  RETIRADA: 9
  SUPORTE EXTERNO: 42
  SUPORTE INTERNO: 1
  TRANSFERÊNCIA: 6
  UPGRADE: 4

-----> Total: 88 <-----

++++++++++++++++++++++++++++++++
 Total geral de atividade: 765
++++++++++++++++++++++++++++++++

-------------------------------------------------
Relatório de Atividades por Auxiliar 
-------------------------------------------------

Técnico: joel.pedro
  Auxiliar: gracione.cavalcanti
    Serviço: Corretiva, Quantidade: 1
    Serviço: TRANSFERÊNCIA, Quantidade: 1
    Serviço: SUPORTE EXTERNO, Quantidade: 1
    Serviço: ATIVAÇÃO, Quantidade: 1
    Serviço: MIGRAÇÃO, Quantidade: 1

Técnico: gracione.cavalcanti
  Auxiliar: jackson.mendes
    Serviço: ATIVAÇÃO, Quantidade: 1
  Auxiliar: joel.pedro
    Serviço: TRANSFERÊNCIA, Quantidade: 2
    Serviço: ATIVAÇÃO, Quantidade: 1

Técnico: jose.welder
  Auxiliar: adriano.teodoro
    Serviço: SUPORTE EXTERNO, Quantidade: 1

Técnico: rogerio.sobreira
  Auxiliar: adriano.teodoro
    Serviço: SUPORTE INTERNO, Quantidade: 1
    Serviço: SUPORTE EXTERNO, Quantidade: 1

Técnico: joao.neto
  Auxiliar: jose.welder
    Serviço: TRANSFERÊNCIA, Quantidade: 1

Técnico: adriano.teodoro
  Auxiliar: jackson.mendes
    Serviço: Mudança Endereço, Quantidade: 1


+++++++++++++++++++++++++++++++
Total geral de ajudas: 14
+++++++++++++++++++++++++++++++
"""

# Caminho do arquivo PDF
caminho_pdf = "relatorio.pdf"

# Chamada da função para salvar o relatório em PDF
salvar_relatorio_em_pdf(texto_completo, caminho_pdf)

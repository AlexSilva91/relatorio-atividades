import pandas as pd
from PyQt5.QtWidgets import QApplication, QDateEdit, QVBoxLayout, QMainWindow, QFileDialog, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
#from acessar_planilha import processar_dados_planilha
from buscar_reincidencia import buscar_reinicidencia
from acess import processar_dados_planilha

caminho_arquivo = None
data_inicial = None
data_final = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Selecionar Arquivo")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QIcon('report.ico'))

        # Definindo o background da janela principal com uma cor acinzentada
        #self.setStyleSheet("background-color: #f0f0f0;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Alinhando o layout vertical ao centro
        self.central_widget.setLayout(self.layout)

        self.button_open = QPushButton("Abrir Arquivo")
        self.button_open.setFixedSize(200, 30)
        self.button_open.setStyleSheet("background-color: #007bff; color: white; border: none;")  # Estilo do Bootstrap para botão primário
        self.button_open.clicked.connect(self.open_file)
        self.layout.addWidget(self.button_open)

        self.title_label1 = QLabel("Data Inicial:")
        self.date_edit1 = QDateEdit()
        self.date_edit1.setFixedSize(200, 30)  # Definindo o tamanho do campo de data
        self.date_edit1.setCalendarPopup(True)
        self.date_edit1.setDate(QDate.currentDate())
        self.date_edit1.dateChanged.connect(self.check_date1)  # Conectando o sinal dateChanged ao slot check_date1

        self.title_label2 = QLabel("Data Final:")
        self.date_edit2 = QDateEdit()
        self.date_edit2.setFixedSize(200, 30)  # Definindo o tamanho do campo de data
        self.date_edit2.setCalendarPopup(True)
        self.date_edit2.setDate(QDate.currentDate())
        self.date_edit2.dateChanged.connect(self.check_date2)  # Conectando o sinal dateChanged ao slot check_date2

        self.layout.addWidget(self.title_label1)
        self.layout.addWidget(self.date_edit1)
        self.layout.addWidget(self.title_label2)
        self.layout.addWidget(self.date_edit2)

        self.button_new_function = QPushButton("Gerar relatório")
        self.button_new_function.setFixedSize(200, 30)
        self.button_new_function.setStyleSheet("background-color: #28a745; color: white; border: none;")  # Estilo do Bootstrap para botão de sucesso
        self.button_new_function.clicked.connect(self.my_function)
        self.layout.addWidget(self.button_new_function)

        self.button_new_function2 = QPushButton("Gerar relatório de reincidência")
        self.button_new_function2.setFixedSize(200, 30)
        self.button_new_function2.setStyleSheet("background-color: #dc3545; color: white; border: none;")  # Estilo do Bootstrap para botão de perigo
        self.button_new_function2.clicked.connect(self.gerar_reincidecia)
        self.layout.addWidget(self.button_new_function2)

        self.label_file = QLabel()
        self.layout.addWidget(self.label_file)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo")
        if filename:
            if filename.endswith('.xlsx'):
                global caminho_arquivo
                caminho_arquivo = filename
                self.label_file.setText(f"Arquivo: {filename}")
            else:
                self.label_file.setText("Por favor, selecione um arquivo .xlsx.")
                caminho_arquivo = None

    def my_function(self):
        global caminho_arquivo, data_inicial, data_final
        if not caminho_arquivo:
            self.label_file.setText("Por favor, selecione um arquivo.")
            return
        if data_inicial is None or data_final is None:
            self.label_file.setText("Por favor, selecione as datas inicial e final.")
            return
        processar_dados_planilha(caminho_arquivo, data_inicial, data_final)
        self.label_file.setText("Relatório de serviços gerado!")

    def gerar_reincidecia(self):
        global caminho_arquivo, data_inicial, data_final
        if not caminho_arquivo:
            self.label_file.setText("Por favor, selecione um arquivo.")
            return
        if not data_inicial or not data_final:
            self.label_file.setText("Por favor, selecione as datas inicial e final.")
            return
        buscar_reinicidencia(caminho_arquivo)
        self.label_file.setText("Relatório de reincidência gerado!")
        
    def check_date1(self, new_date):
        global data_inicial
        # Garante que a data inicial não seja posterior à data atual
        if new_date > QDate.currentDate():
            self.date_edit1.setDate(QDate.currentDate())
        else:
            data_inicial = new_date.toString("yyyy-MM-dd")

    def check_date2(self, new_date):
        global data_final
        # Garante que a data final não seja posterior à data atual
        if new_date > QDate.currentDate():
            self.date_edit2.setDate(QDate.currentDate())
        else:
            data_final = new_date.toString("yyyy-MM-dd")

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

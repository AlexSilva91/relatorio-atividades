from PyQt5.QtWidgets import QApplication, QDateEdit, QVBoxLayout, QMainWindow, QFileDialog, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from acessar_planilha import processar_dados_planilha
from buscar_reincidencia import buscar_reinicidencia
#from acess import get_resultado_formatado
#from buscar_auxiliar import processar_dados_planilha

caminho_arquivo = None
data_inicial = None
data_final = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Selecionar Arquivo")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QIcon('report.ico'))

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
        self.date_edit1.setDate(QDate.currentDate())  # Definindo a data atual
        self.date_edit1.dateChanged.connect(self.check_date1)  # Conectando o sinal dateChanged ao slot check_date1

        self.title_label2 = QLabel("Data Final:")
        self.date_edit2 = QDateEdit()
        self.date_edit2.setFixedSize(200, 30)  # Definindo o tamanho do campo de data
        self.date_edit2.setCalendarPopup(True)
        self.date_edit2.setDate(QDate.currentDate())  # Definindo a data atual
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


    def valida_data(self):
        global data_inicial, data_final
        if not data_inicial or not data_final:
            data_inicial = QDate.currentDate().toString(Qt.ISODate)
            data_final = QDate.currentDate().toString(Qt.ISODate)
            return

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo")
        if filename:
            if filename.endswith('.xlsx'):
                global caminho_arquivo
                caminho_arquivo = filename
                self.label_file.setText(f"Arquivo: {filename}")
                self.valida_data()
            else:
                self.label_file.setText("Por favor, selecione um arquivo .xlsx.")
                caminho_arquivo = None

    def my_function(self):
        global caminho_arquivo, data_inicial, data_final
        if not caminho_arquivo:
            self.label_file.setText("Por favor, selecione um arquivo.")
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
        current_date = QDate.currentDate()
        if new_date.isNull():  # Verifica se a data selecionada é nula
            data_inicial = current_date.toString(Qt.ISODate)  # Atribui a data atual se nenhuma data for selecionada
        elif new_date <= current_date:  # Verifica se a data selecionada é igual ou anterior à data atual
            data_inicial = new_date.toString(Qt.ISODate)
        else:
            self.date_edit1.setDate(current_date)  # Define a data atual se a data selecionada for posterior à data atual

    def check_date2(self, new_date):
        global data_final
        current_date = QDate.currentDate()
        if new_date.isNull():  # Verifica se a data selecionada é nula
            data_final = current_date.toString(Qt.ISODate)  # Atribui a data atual se nenhuma data for selecionada
        elif new_date <= current_date:  # Verifica se a data selecionada é igual ou anterior à data atual
            data_final = new_date.toString(Qt.ISODate)
        else:
            self.date_edit2.setDate(current_date)  # Define a data atual se a data selecionada for posterior à data atual


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

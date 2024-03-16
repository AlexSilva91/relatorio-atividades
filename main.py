from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtWidgets import QWidget
from acessar_planilha import processar_dados_planilha
from buscar_reincidencia import gerar_relatorio

caminho_arquivo = None  # Inicializa a variável caminho_arquivo como None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Selecionar Arquivo")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.button_open = QPushButton("Abrir Arquivo")
        self.button_open.clicked.connect(self.open_file)
        self.layout.addWidget(self.button_open)

        self.button_new_function = QPushButton("Gerar relatório")
        self.button_new_function.clicked.connect(self.my_function)
        self.layout.addWidget(self.button_new_function)

        self.button_new_function = QPushButton("Gerar relatório de reincidência")
        self.button_new_function.clicked.connect(self.gerar_reincidecia)
        self.layout.addWidget(self.button_new_function)

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
        global caminho_arquivo
        if not caminho_arquivo:
            self.label_file.setText("Por favor, selecione um arquivo.")
            return
        processar_dados_planilha(caminho_arquivo)
        self.label_file.setText("Relatório de serviços gerado!")

    def gerar_reincidecia(self):
        global caminho_arquivo
        if not caminho_arquivo:
            self.label_file.setText("Por favor, selecione um arquivo.")
            return
        gerar_relatorio(caminho_arquivo)
        self.label_file.setText("Relatório de reincidência gerado!")

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

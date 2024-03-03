from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtWidgets import QWidget
#from acessar_planilha import processar_dados_planilha
from teste_planilha import processar_dados_planilha

global caminho_arquivo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Selecionar Arquivo")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Botão para abrir o arquivo
        self.button_open = QPushButton("Abrir Arquivo")
        self.button_open.clicked.connect(self.open_file)
        self.layout.addWidget(self.button_open)

        # Botão para executar a função
        self.button_new_function = QPushButton("Gerar relatório")
        self.button_new_function.clicked.connect(self.my_function)
        self.layout.addWidget(self.button_new_function)

        # Label para exibir o caminho do arquivo
        self.label_file = QLabel()
        self.layout.addWidget(self.label_file)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo")

        if filename:
            global caminho_arquivo
            caminho_arquivo = filename
            self.label_file.setText(f"Arquivo: {filename}")

    def my_function(self):
        global caminho_arquivo
        processar_dados_planilha(caminho_arquivo)
        self.label_file.setText("Relatório gerado!")

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()

import os
import logging
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QDateEdit, QDesktopWidget
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QIcon
from gui.worker_thread import WorkerThread
from process.acessar_planilha import processar_dados_planilha
from process.buscar_reincidencia import buscar_reinicidencia
from bot_module.bot_module import get_status, start_bot, parar_bot
from utils.validation import validation_legth_sheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Inicialização dos atributos
        self.data_inicial = None
        self.data_final = None
        self.caminho_arquivo = None
        self.status_anterior = None

        self.init_ui()
        self.init_bot()
        self.init_status_check()

    def init_ui(self):
        self.setWindowTitle("OuriNet - Meta Técnicos")
        self.setFixedSize(400, 350)
        self.setWindowIcon(QIcon('resources/report.ico'))
        self.center()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QHBoxLayout()
        self.central_layout.setAlignment(Qt.AlignCenter)
        self.central_widget.setLayout(self.central_layout)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.central_layout.addLayout(self.layout)

        self.init_file_button()
        self.init_date_pickers()
        self.init_report_buttons()
        self.init_status_label()

    def init_file_button(self):
        self.button_open = QPushButton("Abrir Arquivo")
        self.button_open.setFixedSize(200, 40)
        self.button_open.setStyleSheet("background-color: #007bff;color: white; border: 2px solid white; border-radius: 10px;")
        self.button_open.clicked.connect(self.open_file)
        self.layout.addWidget(self.button_open)

    def init_date_pickers(self):
        self.title_label1 = QLabel("Data Inicial:")
        self.title_label1.setStyleSheet("color: #4F4F4F; font-size: 15px; font-weight: bold;")
        self.date_edit1 = QDateEdit()
        self.date_edit1.setStyleSheet("color: #4F4F4F; border: 2px solid white; border-radius: 10px;")
        self.date_edit1.setFixedSize(200, 30)
        self.date_edit1.setCalendarPopup(True)
        self.date_edit1.setDate(QDate.currentDate())
        self.date_edit1.dateChanged.connect(self.check_date1)

        self.title_label2 = QLabel("Data Final:")
        self.title_label2.setStyleSheet("color: #4F4F4F; font-size: 15px; font-weight: bold;")
        self.date_edit2 = QDateEdit()
        self.date_edit2.setFixedSize(200, 30)
        self.date_edit2.setStyleSheet("color:  #4F4F4F; border: 2px solid white; border-radius: 10px;")
        self.date_edit2.setCalendarPopup(True)
        self.date_edit2.setDate(QDate.currentDate())
        self.date_edit2.dateChanged.connect(self.check_date2)

        self.layout.addWidget(self.title_label1)
        self.layout.addWidget(self.date_edit1)
        self.layout.addWidget(self.title_label2)
        self.layout.addWidget(self.date_edit2)

    def init_report_buttons(self):
        self.button_new_function = QPushButton("Gerar relatório")
        self.button_new_function.setFixedSize(200, 40)
        self.button_new_function.setStyleSheet("background-color: #28a745; color: white; border: 2px solid white; border-radius: 10px;")
        self.button_new_function.clicked.connect(self.start_processar_dados)
        self.layout.addWidget(self.button_new_function)

        self.button_new_function2 = QPushButton("Relatório de\n reincidência")
        self.button_new_function2.setFixedSize(200, 40)
        self.button_new_function2.setStyleSheet("background-color: #dc3545; color: white; border: 2px solid white; border-radius: 10px;")
        self.button_new_function2.clicked.connect(self.start_buscar_reincidencia)
        self.layout.addWidget(self.button_new_function2)

    def init_status_label(self):
        self.label_file = QLabel()
        self.layout.addWidget(self.label_file)

    def init_bot(self):
        import threading
        self.bot_thread = threading.Thread(target=start_bot)
        self.bot_thread.daemon = True
        self.bot_thread.start()

    def init_status_check(self):
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.check_status)
        self.status_timer.start(1000)
        self.status_anterior = None

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

    def closeEvent(self, event):
        parar_bot()
        logging.info("Bot interrompido ao fechar a janela.")
        event.accept()

    def check_status(self):
        status = get_status()
        if status != self.status_anterior:
            logging.info(f"Status do sistema: {status}")
            self.status_anterior = status

            if status == "desbloqueado":
                self.show_status_message("Acesso liberado!")
                self.label_file.setStyleSheet("color: green;")
                self.label_file.setAlignment(Qt.AlignCenter)

        if status == "bloqueado":
            self.date_edit1.setDisabled(True)
            self.date_edit2.setDisabled(True)
            self.button_open.setDisabled(True)
            self.button_new_function.setDisabled(True)
            self.button_new_function2.setDisabled(True)
            self.label_file.setText("Acesso bloqueado!")
            self.label_file.setStyleSheet("color: red;")
            self.label_file.setAlignment(Qt.AlignCenter)
        else:
            self.date_edit1.setEnabled(True)
            self.date_edit2.setEnabled(True)
            self.button_open.setEnabled(True)
            self.button_new_function.setEnabled(True)
            self.button_new_function2.setEnabled(True)

    def show_status_message(self, message):
        self.label_file.setText(message)

    def check_date1(self, new_date):
        if new_date.isNull():
            self.data_inicial = QDate.currentDate().toString(Qt.ISODate)
            self.date_edit1.setDate(QDate.currentDate())
        else:
            if new_date > QDate.currentDate():
                self.date_edit1.setDate(QDate.currentDate())
                self.data_inicial = QDate.currentDate().toString(Qt.ISODate)
                logging.warning("Data inicial não pode ser maior que a data atual. Data alterada para hoje.")
            else:
                self.data_inicial = new_date.toString(Qt.ISODate)
                logging.info(f"Data inicial atualizada para: {self.data_inicial}")

        if hasattr(self, 'data_final') and self.data_final and QDate.fromString(self.data_final, Qt.ISODate) < new_date:
            self.date_edit2.setDate(new_date)
            self.data_final = new_date.toString(Qt.ISODate)
            logging.warning("Data final não pode ser anterior à data inicial. Data final ajustada para a data inicial.")

    def check_date2(self, new_date):
        if new_date.isNull():
            self.data_final = QDate.currentDate().toString(Qt.ISODate)
            self.date_edit2.setDate(QDate.currentDate())
        else:
            if new_date > QDate.currentDate():
                self.date_edit2.setDate(QDate.currentDate())
                self.data_final = QDate.currentDate().toString(Qt.ISODate)
                logging.warning("Data final não pode ser maior que a data atual. Data alterada para hoje.")
            else:
                self.data_final = new_date.toString(Qt.ISODate)
                logging.info(f"Data final atualizada para: {self.data_final}")

        if hasattr(self, 'data_inicial') and self.data_inicial and QDate.fromString(self.data_final, Qt.ISODate) < QDate.fromString(self.data_inicial, Qt.ISODate):
            self.date_edit1.setDate(QDate.fromString(self.data_final, Qt.ISODate))
            self.data_inicial = self.data_final
            logging.warning("Data inicial não pode ser maior que a data final. Data inicial ajustada para a data final.")

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo")
        if filename:
            if filename.endswith('.xlsx') and validation_legth_sheet(filename):
                self.caminho_arquivo = filename
                file_name = os.path.basename(filename)
                self.label_file.setText(f"{file_name[:23]}...")
                self.label_file.setStyleSheet("color: green;")
                self.label_file.setAlignment(Qt.AlignCenter)
                logging.info(f"Arquivo selecionado: {file_name}")
            else:
                self.label_file.setText("Arquivo inválido!")
                self.label_file.setStyleSheet("color: red;")
                self.caminho_arquivo = None
                logging.warning("Arquivo selecionado não é um .xlsx. ou o número de colunas é superior a 22")

    def start_processar_dados(self):
        if not self.caminho_arquivo:
            self.label_file.setText("Por favor, selecione um arquivo.")
            self.label_file.setStyleSheet("color: red;")
            logging.error("Nenhum arquivo foi selecionado.")
            return
        
        self.label_file.setText("Gerando...")
        self.label_file.setStyleSheet("color: orange;")
        logging.info("Iniciando o processamento de dados...")

        self.thread = WorkerThread(processar_dados_planilha, self.caminho_arquivo, self.data_inicial, self.data_final)
        self.thread.finished.connect(self.on_process_finished)
        self.thread.start()

    def start_buscar_reincidencia(self):
        if not self.caminho_arquivo:
            self.label_file.setText("Por favor, selecione um arquivo.")
            self.label_file.setStyleSheet("color: red;")
            logging.error("Nenhum arquivo foi selecionado.")
            return

        self.label_file.setText("Buscando reincidências...")
        self.label_file.setStyleSheet("color: orange;")
        logging.info("Iniciando a busca por reincidências...")

        self.thread2 = WorkerThread(buscar_reinicidencia, self.caminho_arquivo, self.data_inicial, self.data_final)
        self.thread2.finished.connect(self.on_process_finished)
        self.thread2.start()

    def on_process_finished(self):
        self.label_file.setText("Processamento Concluído!")
        self.label_file.setStyleSheet("color: green;")
        logging.info("Processamento concluído com sucesso.")
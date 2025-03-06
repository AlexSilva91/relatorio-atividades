from PyQt5.QtCore import QThread, pyqtSignal
import logging

class WorkerThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        total_steps = 100
        for i in range(total_steps):
            if i == 97:
                logging.info(f"Executando tarefa com {self.func.__name__} com argumentos {self.args}")
                self.func(*self.args)
            self.progress.emit(i + 1)
            self.msleep(10)

        self.finished.emit()
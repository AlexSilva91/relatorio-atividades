import sys
from PyQt5.QtWidgets import QApplication
import qt_material
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    # Aplicando o tema
    qt_material.apply_stylesheet(app, theme='light_blue.xml')
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
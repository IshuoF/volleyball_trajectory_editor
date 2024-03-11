from PyQt5.QtWidgets import QApplication
from GUI import MyWindow

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    app.exec_()

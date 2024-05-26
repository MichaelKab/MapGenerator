import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QMenuBar, QStatusBar,
                             QApplication, QLabel)
from dotenv import load_dotenv

from uifiles.UiMapGen import Ui_Mapgenerator


class Ui_Main_Window(QMainWindow):
    def __init__(self):
        super(Ui_Main_Window, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(501, 436)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.to_generate = QPushButton(self.centralwidget)
        self.to_generate.setGeometry(QtCore.QRect(110, 120, 301, 81))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        self.to_generate.setFont(font)
        self.to_generate.setObjectName("pushButton")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 500, 91))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.to_history = QPushButton(self.centralwidget)
        self.to_history.setGeometry(QtCore.QRect(110, 220, 301, 81))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(20)
        self.to_history.setFont(font)
        self.to_history.setObjectName("pushButton_2")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 501, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.add_functions()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Главное меню"))
        self.to_generate.setText(_translate("MainWindow", "Перейти к генерации"))
        self.label.setText(_translate("MainWindow", "Главное меню"))
        self.to_history.setText(_translate("MainWindow", "История генераций"))

    def add_functions(self):
        self.to_generate.clicked.connect(self.open_generate)

    def open_generate(self):
        self.hide()
        self.window_gen = Ui_Mapgenerator(self.show)
        self.window_gen.show()

def main():
    app = QApplication(sys.argv)
    window = Ui_Main_Window()
    window.show()
    sys.exit(app.exec_())


StyleSheet = '''
QCheckBox {
    spacing: 5px;
    font-size:25px;     
}

QCheckBox::indicator {
    width:  33px;
    height: 33px;
}
'''

if __name__ == '__main__':
    load_dotenv()
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    app.setStyleSheet(StyleSheet)
    main()
    sys.exit(app.exec_())

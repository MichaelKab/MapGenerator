import os
import shutil

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QFrame, QMainWindow, QWidget, QPushButton, QMenuBar, QStatusBar,
                             QFileDialog, QLabel, QLineEdit)

from uifiles.UiSelectionWindow import Ui_selection_window
from uifiles.Ui_generator_window import Ui_generator_window


class Ui_Mapgenerator(QMainWindow):
    def __init__(self, return_back):
        super(Ui_Mapgenerator, self).__init__()
        self.glob_font = self.set_font_and_color()
        self.glob_font.setPointSize(15)
        self.return_back = return_back
        self.setObjectName("MainWindow")
        self.resize(700, 350)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(210, 10, 71, 41))
        self.lineEdit.setFont(self.glob_font)
        self.lineEdit.setObjectName("lineEdit")
        self.label_1 = QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 20, 170, 24))
        self.label_1.setFont(self.glob_font)
        self.label_1.setObjectName("label")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 171, 24))
        self.label_2.setFont(self.glob_font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 120, 191, 24))
        self.label_3.setFont(self.glob_font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 160, 301, 51))
        self.pushButton.setFont(self.glob_font)
        self.pushButton.setObjectName("pushButton")
        self.line = QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(300, 10, 31, 201))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.choice_button = QPushButton(self.centralwidget)
        self.choice_button.setGeometry(QtCore.QRect(350, 160, 341, 51))
        self.choice_button.setFont(self.glob_font)
        self.choice_button.setObjectName("pushButton_2")
        self.generate_map_button = QPushButton(self.centralwidget)
        self.generate_map_button.setGeometry(QtCore.QRect(10, 240, 301, 51))
        self.generate_map_button.setFont(self.glob_font)
        self.generate_map_button.setObjectName("generate_map_button")
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 60, 71, 41))
        self.lineEdit_2.setFont(self.glob_font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(210, 110, 71, 41))
        self.lineEdit_3.setFont(self.glob_font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.load_cell = QPushButton(self.centralwidget)
        self.load_cell.setGeometry(QtCore.QRect(350, 90, 341, 51))
        rx = QtCore.QRegExp("[0-9]{100}")
        val = QtGui.QRegExpValidator(rx)
        self.lineEdit.setValidator(val)
        self.lineEdit_2.setValidator(val)
        self.lineEdit_3.setValidator(val)
        self.load_cell.setFont(self.glob_font)
        self.load_cell.setObjectName("load_cell")
        self.back = QPushButton(self.centralwidget)
        self.back.setGeometry(QtCore.QRect(420, 10, 221, 51))
        self.back.setFont(self.glob_font)
        self.back.setObjectName("back")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 825, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.add_functions()

    def add_functions(self):
        self.choice_button.clicked.connect(self.to_choice)
        self.load_cell.clicked.connect(self.openFileNameDialog)
        self.back.clicked.connect(self.to_main)
        self.generate_map_button.clicked.connect(self.generate)
        self.generate_map_button.clicked.connect(self.generate)

    def to_main(self):
        self.close()
        self.return_back()

    def to_choice(self):
        self.window_choice = Ui_selection_window()
        self.window_choice.show()

    def generate(self):
        n = int(self.lineEdit.text())
        m = int(self.lineEdit_2.text())
        size = int(self.lineEdit_3.text())
        self.gennerator = Ui_generator_window(n, m, size)
        self.gennerator.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        DIR_SAVE = os.getenv('CELLS_URL')
        name_file = fileName.split('/')[-1]
        shutil.copy2(fileName, DIR_SAVE + '/' + name_file)
        if fileName:
            print(fileName, DIR_SAVE + '/' + name_file)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Генерация"))
        self.lineEdit.setText(_translate("MainWindow", "10"))
        self.label_1.setText(_translate("MainWindow", "Высота в клетках"))
        self.label_2.setText(_translate("MainWindow", "Ширина в клетках"))
        self.label_3.setText(_translate("MainWindow", "Размер клетки (px)"))
        self.pushButton.setText(_translate("MainWindow", "Сохранить"))
        self.choice_button.setText(_translate("MainWindow", "Выбрать используемые клетки"))
        self.generate_map_button.setText(_translate("MainWindow", "Генерация карты"))
        self.lineEdit_2.setText(_translate("MainWindow", "10"))
        self.lineEdit_3.setText(_translate("MainWindow", "100"))
        self.load_cell.setText(_translate("MainWindow", "загрузить клетку (.png)"))
        self.back.setText(_translate("MainWindow", "Вернуться на главную"))

    def set_font_and_color(self):
        COLOR = os.getenv('COLOR')
        FONT = os.getenv('FONT')
        self.setStyleSheet(f"color: {COLOR};")
        font = QtGui.QFont()
        font.setFamily(FONT)
        return font

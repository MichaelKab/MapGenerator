import os
import shutil

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QFrame, QMainWindow, QWidget, QPushButton, QMenuBar, QStatusBar,
                             QFileDialog, QLabel, QLineEdit)

from generator import generate_map, open_cells
from uifiles.UiSelectionWindow import Ui_selection_window


class Ui_Mapgenerator(QMainWindow):
    def __init__(self):
        super(Ui_Mapgenerator, self).__init__()
        self.setObjectName("MainWindow")
        self.resize(825, 345)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(210, 10, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 161, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 171, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 120, 191, 24))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 160, 301, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(15)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.line = QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(300, 10, 31, 201))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.choice_button = QPushButton(self.centralwidget)
        self.choice_button.setGeometry(QtCore.QRect(350, 160, 341, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(15)
        self.choice_button.setFont(font)
        self.choice_button.setObjectName("pushButton_2")
        self.generate_map_button = QPushButton(self.centralwidget)
        self.generate_map_button.setGeometry(QtCore.QRect(10, 240, 301, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(15)
        self.generate_map_button.setFont(font)
        self.generate_map_button.setObjectName("generate_map_button")
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 60, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(210, 110, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.load_cell = QPushButton(self.centralwidget)
        self.load_cell.setGeometry(QtCore.QRect(350, 90, 341, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(15)
        self.load_cell.setFont(font)
        self.load_cell.setObjectName("load_cell")
        self.back = QPushButton(self.centralwidget)
        self.back.setGeometry(QtCore.QRect(590, 10, 221, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(15)
        self.back.setFont(font)
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
        self.window_gen = Ui_MainWindow()
        self.window_gen.show()

    def to_choice(self):
        self.window_choice = Ui_selection_window()
        self.window_choice.show()

    def generate(self):
        n = int(self.lineEdit.text())
        m = int(self.lineEdit_2.text())
        size = int(self.lineEdit_3.text())
        DIR = os.getenv('CELLS_URL')
        DIR_SAVE = os.getenv('SAVE_RESULT')
        cells = open_cells(DIR, size)
        map = generate_map(n, m, size, cells)
        map.save(DIR_SAVE)
        self.image_window = Image_window()
        self.image_window.load_image(DIR_SAVE)
        self.image_window.show()

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

    def load_image(self, file_name):
        pixmap = QPixmap(file_name)
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())
        self.resize(pixmap.width(), pixmap.height())

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Генерация"))
        self.lineEdit.setText(_translate("MainWindow", "10"))
        self.label.setText(_translate("MainWindow", "Высота в клетках"))
        self.label_2.setText(_translate("MainWindow", "Ширина в клетках"))
        self.label_3.setText(_translate("MainWindow", "Размер клетки (px)"))
        self.pushButton.setText(_translate("MainWindow", "Сохранить"))
        self.choice_button.setText(_translate("MainWindow", "Выбрать используемые клетки"))
        self.generate_map_button.setText(_translate("MainWindow", "Генерация карты"))
        self.lineEdit_2.setText(_translate("MainWindow", "10"))
        self.lineEdit_3.setText(_translate("MainWindow", "100"))
        self.load_cell.setText(_translate("MainWindow", "загрузить клетку (.png)"))
        self.back.setText(_translate("MainWindow", "Вернуться на главную"))

class Image_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Тест')
        self.setGeometry(200, 200, 300, 300)

    def load_image(self, file_name):
        pixmap = QPixmap(file_name)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())

        self.resize(pixmap.width(), pixmap.height())
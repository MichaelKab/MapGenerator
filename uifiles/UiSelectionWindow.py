import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QGridLayout, QCheckBox)


class Ui_selection_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор клеток")
        outerLayout = QVBoxLayout()
        topLayout = QFormLayout()
        label = QLabel(self)
        label.setGeometry(QtCore.QRect(150, 10, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(15)
        label.setFont(font)
        label.setObjectName("label")
        pushButton = QPushButton(self)
        pushButton.setGeometry(QtCore.QRect(20, 32, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        pushButton.setFont(font)
        pushButton.setObjectName("pushButton")
        pushButton.clicked.connect(self.save)
        label.setText("Выберите клетки")
        pushButton.setText("Сохранить")
        topLayout.addRow(label, pushButton)
        self.body = QGridLayout()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.generate_body()
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(self.body)
        self.setLayout(outerLayout)

    def save(self):
        save_data = []
        SAVE_CONFIG = os.getenv('SAVE_CONFIG')
        for i in range(self.body.rowCount()):
            now = self.body.itemAtPosition(i, 0).widget()
            save_data.append(str(now.checkState()))
        with open(SAVE_CONFIG, 'w') as file:
            file.write(" ".join(save_data))
        self.close()

    def generate_body(self):
        DB_DIR = os.getenv('CELLS_URL')
        SAVE_CONFIG = os.getenv('SAVE_CONFIG')
        try:
            with open(SAVE_CONFIG, 'r') as file:
                save_values = list(map(int, file.read().split()))
        except FileNotFoundError:
            save_values = [2 for i in range(100)]
        for ind, file_name in enumerate(os.listdir(DB_DIR)):
            self.body.setRowStretch(ind, 110)
            pixmap = QPixmap(f"{DB_DIR}/{file_name}")
            pixmap = pixmap.scaled(100, 100)
            label = QLabel()
            label.setPixmap(pixmap)
            label.resize(pixmap.width(), pixmap.height())
            checkBox = QCheckBox()
            checkBox.setChecked(save_values[ind] != 0)
            font = QtGui.QFont()
            font.setPointSize(10)
            checkBox.setGeometry(200, 150, 100, 80)
            checkBox.setText(str(ind + 1))
            self.body.addWidget(checkBox, ind, 0, alignment=QtCore.Qt.AlignHCenter)
            self.body.addWidget(label, ind, 1)


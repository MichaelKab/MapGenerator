import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QGridLayout, QCheckBox,
                             QMessageBox, QButtonGroup, QMainWindow)
from random import randint
from generator import generate_map, open_cells


class Change_picture(QWidget):
    def __init__(self, new_value):
        super().__init__()
        self.setWindowTitle("Изменить клетку")
        self.new_value = new_value
        self.group = QButtonGroup()
        outerLayout = QVBoxLayout()
        topLayout = QFormLayout()
        font = QtGui.QFont()
        font.setPointSize(15)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.body = QGridLayout()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.generate_body()
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(self.body)
        self.setLayout(outerLayout)
        self.group.idClicked.connect(self.save)

    def save(self, id):
        self.new_value = id
        DB_DIR = os.getenv('CELLS_URL')
        for ind, file_name in enumerate(os.listdir(DB_DIR)):
            if (ind == id):
                pixmap = QPixmap(f"{DB_DIR}/{file_name}")
                pixmap = pixmap.scaled(100, 100)
                self.new_value = pixmap
        self.close()
        print("!!!")

    def generate_body(self):
        DB_DIR = os.getenv('CELLS_URL')
        for ind, file_name in enumerate(os.listdir(DB_DIR)):
            self.body.setRowStretch(ind, 110)
            pixmap = QPixmap(f"{DB_DIR}/{file_name}")
            pixmap = pixmap.scaled(100, 100)
            label = QLabel()
            button_save = QPushButton(self)
            label.setPixmap(pixmap)
            label.resize(pixmap.width(), pixmap.height())
            font = QtGui.QFont()
            font.setPointSize(14)
            button_save.setFont(font)
            button_save.setText("Выбрать клетку")
            self.group.addButton(button_save, ind)
            self.body.addWidget(label, ind, 0)
            self.body.addWidget(button_save, ind, 1)


class MyLabel(QLabel):
    clicked = QtCore.pyqtSignal()  # новый сигнал под клик

    def __init__(self, *args):
        QLabel.__init__(self, *args)

    # обработчик мыши
    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()  # вызывает сигнал
        QLabel.mousePressEvent(self, QMouseEvent)


class Ui_generator_window(QWidget):
    def __init__(self, n, m, size):
        super().__init__()
        self.n = n
        self.m = m
        self.size = size
        self.pixmaps = []
        self.choices = []
        self.setWindowTitle("Выбор клеток")
        self.DB_DIR = os.getenv('CELLS_URL')
        self.file_names = os.listdir(self.DB_DIR)
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
        self.smap.mapped.connect(self.on_click)

    def integer_map(self):
        for name in self.file_names:
            self.pixmaps.append(QPixmap(f"{self.DB_DIR}/{name}"))
            self.pixmaps[-1] = self.pixmaps[-1].scaled(100, 100)

        self.choices = [[randint(0, len(self.file_names) - 1) for _ in range(self.m)] for j in range(self.n)]

    def save(self):
        DIR_SAVE = os.getenv('SAVE_RESULT')
        cells = open_cells(self.DB_DIR, self.size)
        map_for_gen = [[0 for _ in range(self.n)] for i in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                map_for_gen[j][i] = self.choices[i][j]
        map = generate_map(self.n, self.m, self.size, cells, map_for_gen)
        map.save(DIR_SAVE)
        self.image_window = Image_window()
        self.image_window.load_image(DIR_SAVE)
        self.image_window.show()
        save_data = []
        # SAVE_CONFIG = os.getenv('SAVE_CONFIG')
        # for i in range(self.body.rowCount()):
        #     now = self.body.itemAtPosition(i, 0).widget()
        #     save_data.append(str(now.checkState()))
        # with open(SAVE_CONFIG, 'w') as file:
        #     file.write(" ".join(save_data))
        self.close()

    def generate_body(self):
        self.integer_map()
        self.smap = QtCore.QSignalMapper(self)
        index = 0
        for i in range(self.n):
            for j in range(self.m):
                self.body.setRowStretch(i, 110)
                pixmap = self.pixmaps[self.choices[i][j]]
                pixmap = pixmap.scaled(100, 100)
                label = MyLabel()
                label.setPixmap(pixmap)
                label.resize(pixmap.width(), pixmap.height())
                font = QtGui.QFont()
                font.setPointSize(10)
                label.setObjectName(f"{i}, {j}")
                self.body.addWidget(label, i, j)
                label.clicked.connect(self.smap.map)  # соеденить
                self.smap.setMapping(label, index)  # задать индекс
                index += 1

    @QtCore.pyqtSlot(int)
    def on_click(self, index):
        ind_x = index // self.m
        ind_y = index % self.m
        self.choices[ind_x][ind_y] = (1 + self.choices[ind_x][ind_y]) % len(self.file_names)
        label = MyLabel()
        label.setPixmap(self.pixmaps[self.choices[ind_x][ind_y]])
        dells = self.body.itemAtPosition(ind_x, ind_y)
        label.clicked.connect(self.smap.map)  # соеденить
        self.smap.setMapping(label, index)  # задать индекс
        dells.widget().deleteLater()
        self.body.addWidget(label, ind_x, ind_y)
        # self.change_box = Change_picture(new_label)
        # self.change_box.show()
        # print(new_label)
        return index
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

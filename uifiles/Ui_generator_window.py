import os
import datetime
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QPushButton, QLabel, QGridLayout,
                             QButtonGroup, QMainWindow, QMessageBox)
from random import randint
from generator import generate_map, open_cells
from collections import defaultdict


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
        self.image_window = None
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
        font = QtGui.QFont()
        font.setPointSize(15)
        pushButton = QPushButton(self)
        pushButton.setGeometry(QtCore.QRect(20, 32, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        pushButton.setFont(font)
        pushButton.setObjectName("pushButton")
        pushButton.clicked.connect(self.save)
        pushButton.setText("Сохранить")
        topLayout.addRow(pushButton)
        self.body = QGridLayout()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.generate_body()
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(self.body)
        self.setLayout(outerLayout)
        self.smap.mapped.connect(self.on_click)

    def integer_map(self):
        SAVE_CONFIG = os.getenv('SAVE_CONFIG')
        SAVE_PERCENT = os.getenv('SAVE_PERCENT')
        percents = defaultdict(int)
        try:
            with open(SAVE_CONFIG, 'r') as file:
                save_values = defaultdict(int)
                for ind, el in enumerate(file.read().split()):
                    save_values[ind] = int(el)
        except FileNotFoundError:
            QMessageBox.about(self, "error", "Не выбраны клетки")
            save_values = [2 for i in range(100)]

        try:
            with open(SAVE_PERCENT, 'r') as file:
                percents = defaultdict(int)
                for ind, el in enumerate(file.read().split()):
                    percents[ind] = int(el)
        except FileNotFoundError:
            QMessageBox.about(self, "error", "Не выбраны клетки")
        clear_file_names = []
        self.clear_percents = []
        summ_percents = 0
        for ind, name in enumerate(self.file_names):
            if save_values[ind] == 2:
                clear_file_names.append(name)
                self.clear_percents.append([percents[ind], len(clear_file_names) - 1])
                summ_percents += percents[ind]
        for i in range(len(self.clear_percents)):
            self.clear_percents[i] = tuple([self.clear_percents[i][0] * 100 / summ_percents, self.clear_percents[i][1]])
        self.clear_percents.sort()
        self.file_names = clear_file_names
        for ind, name in enumerate(self.file_names):
            self.pixmaps.append(QPixmap(f"{self.DB_DIR}/{name}"))
            self.pixmaps[-1] = self.pixmaps[-1].scaled(60, 60)
        self.choices = [[0 for _ in range(self.m)] for j in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                now = randint(1, 100)
                for el, ind in self.clear_percents:
                    if now - el <= 0:
                        self.choices[i][j] = ind
                        break

    def save(self):
        now = datetime.datetime.now()
        date_time = now.strftime("%m-%d-%Y %H-%M-%S")
        DIR_SAVE = os.getenv('SAVE_RESULT_DIR') + f"/result {date_time}.png"
        cells = open_cells(self.DB_DIR, self.file_names, self.size)
        map_for_gen = [[0 for _ in range(self.n)] for i in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                map_for_gen[j][i] = self.choices[i][j]
        map = generate_map(self.n, self.m, self.size, cells, map_for_gen)
        map.save(DIR_SAVE)
        self.image_window = Image_window(DIR_SAVE)
        self.image_window.load_image(DIR_SAVE)
        self.image_window.show()
        self.close()

    def generate_body(self):
        self.integer_map()
        self.smap = QtCore.QSignalMapper(self)
        index = 0
        for i in range(self.n):
            for j in range(self.m):
                self.body.setRowStretch(i, 110)
                pixmap = self.pixmaps[self.choices[i][j]]
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
    def __init__(self, dir_save):
        super().__init__()

        self.setWindowTitle(dir_save)
        self.setGeometry(200, 200, 300, 300)

    def load_image(self, file_name):
        pixmap = QPixmap(file_name)

        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.width(), pixmap.height())

        self.resize(pixmap.width(), pixmap.height())

import sys

from PyQt5.QtWidgets import QApplication
from dotenv import load_dotenv

from uifiles.UIMainwindow import Ui_Main_Window


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

import sys
import os
import imghdr
from pathlib import Path
import random

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QComboBox,
    QLineEdit,
    QGridLayout,
    QFileDialog,
    QScrollArea,
)
from PyQt6.QtCore import QDate, Qt

default_font = "calibri"
app_width = 800
app_height = int(app_width*(9/16))

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(app_width, app_height)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("Meetn Bonus App")
        self.setStyleSheet("background-color: #333333")

        layout = QHBoxLayout()
        layout.addWidget(QLabel('Meetn Bonus App'))
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()

    #open qss file
    File = open("main.qss",'r')

    with File:
        qss = File.read()
        app.setStyleSheet(qss)
        now = QDate.currentDate()

        print(now.toString(Qt.DateFormat.ISODate))
        print(now.toString(Qt.DateFormat.RFC2822Date))
        
    window.show()
    sys.exit(app.exec())
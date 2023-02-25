import sys
import os

from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
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
)

from PyQt6.QtCore import QDate, QTime, QDateTime, Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meetn Bonus App")
        # Create a QHBoxLayout instance
        layout = QHBoxLayout()
        # Add widgets to the layout
        layout.addWidget(MainPane("str"), 1)
        layout.addWidget(NavigationPane("str"), 1)
        # Set the layout on the application's window
        self.setLayout(layout)
        # print(self.children())

class MainPane(QWidget):
    def __init__(self, arg):
        super(MainPane, self).__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select a Camera Source:"))
        layout.addWidget(AvaliableCameras('wshat'))
        layout.addWidget(CompositeScreen('path'))
        self.setLayout(layout)

class NavigationPane(QWidget):
    def __init__(self, arg):
        super(NavigationPane, self).__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select a Virtual Background:"))
        self.dir_name_edit = QLineEdit()
        layout.addWidget(self.dir_name_edit, 2)
        self.openFolderBtn = QPushButton("Select Folder", self)
        layout.addWidget(self.openFolderBtn, 2)
        self.openFolderBtn.clicked.connect(self.buttonClicked)
        self.setLayout(layout)

    def buttonClicked(self):
        self.openFileNamesDialog()

    def openFileNamesDialog(self):
        dialog = QFileDialog(self)
        options = dialog.Options()
        options |= dialog.DontUseNativeDialog
        bg_dir_path = str(dialog.getExistingDirectory(self, "Select Virtual Background Folder"))
        if bg_dir_path:
            self.dir_name_edit.setText(bg_dir_path)

class CompositeScreen(QWidget):
    def __init__(self, path):
        super(CompositeScreen, self).__init__()
        self.im = QPixmap("./JohnDoe.jpg")
        self.label = QLabel()
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)

class AvaliableCameras(QWidget):
    def __init__(self, wshat):
        super(AvaliableCameras, self).__init__()
        layout = QVBoxLayout()
        combo = QComboBox()
        combo.addItem("web camera 1")
        combo.addItem("web camera 2")
        combo.addItem("web camera 3")
        layout.addWidget(combo)
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
    sys.exit(app.exec_())
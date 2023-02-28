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

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1200, 700)

        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("Meetn Bonus App")
        self.setStyleSheet("background-color: #333333")
        layout = QHBoxLayout()
        layout.addWidget(MainPane("str"), 1)
        layout.addWidget(NavigationPane("str"), 1)
        self.setLayout(layout)

class MainPane(QWidget):
    def __init__(self, arg):
        super(MainPane, self).__init__()
        layout = QVBoxLayout()
        layout.addWidget(SubTitle("Select a Camera Source:"))
        layout.addWidget(AvaliableCameras('wshat'))
        layout.addWidget(CompositeScreen('path'))
        layout.addStretch()
        self.setLayout(layout)

class NavigationPane(QWidget):
    def __init__(self, arg):
        super(NavigationPane, self).__init__()
        self.background_image_path = ""
        self.layout = QVBoxLayout()
        self.layout.addWidget(SubTitle("Select a Virtual Background:"))
        self.dir_name_edit = QLineEdit()
        self.dir_name_edit.setStyleSheet(
            "margin-top: 9px;"
            "background-color: #444444;"
        )
        self.layout.addWidget(self.dir_name_edit, 2)
        self.openFolderBtn = QPushButton("Select Folder", self)
        self.layout.addWidget(self.openFolderBtn, 2)
        self.backgroundImageGallery = BackgroundImageGallery("", [])
        self.layout.addWidget(self.backgroundImageGallery, 2)
        self.setLayout(self.layout)
        self.setLayout(self.layout)
        self.openFolderBtn.clicked.connect(self.openFolderButtonClicked)

    def openFolderButtonClicked(self):
        self.openFileNamesDialog()

    def openFileNamesDialog(self):
        dialog = QFileDialog(self)
        background_image_directory_path = str(dialog.getExistingDirectory(self, "Select Virtual Background Folder"))
        if background_image_directory_path:
            self.dir_name_edit.setText(background_image_directory_path)

            background_image_list = os.listdir(Path(background_image_directory_path))
            background_image_list_new = []
            for background_image_path in background_image_list:
                my_path = f'{Path(background_image_directory_path)}\{background_image_path}'
                isFile = os.path.isfile(my_path)
                if (isFile):
                    if (imghdr.what(my_path) != None):
                        background_image_list_new.append(my_path)
            self.backgroundImageGallery.close()

            self.backgroundImageGallery = BackgroundImageGallery(background_image_directory_path, background_image_list_new)
            self.layout.addWidget(self.backgroundImageGallery, 2)

class SubTitle(QWidget):
    def __init__(self, title):
        super(SubTitle, self).__init__()
        layout = QVBoxLayout()
        label = QLabel(title)
        label.setStyleSheet(
            "color: #DEDEDE;"
            "font-family:{default_font};"
            "font-size: 18px;"
            "padding: 0px 0px;"
            "margin: 0px"
        )
        layout.addWidget(label)
        self.setLayout(layout)

class CompositeScreen(QWidget):
    def __init__(self, path):
        super(CompositeScreen, self).__init__()
        self.im = QPixmap(f"../basic_feature/human_img/2.jpg")
        self.im = self.im.scaled(720, 500)
        self.label = QLabel()
        self.label.addActions
        self.label.mousePressEvent = self.clickedMouse
        self.label.setPixmap(self.im)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label, 1, 1)
        self.setLayout(self.grid)

    def clickedMouse(self, event):
        i = random.randint(1, 4)
        self.im = QPixmap(f"../basic_feature/human_img/{i}.jpg")
        self.label.setPixmap(self.im)

class AvaliableCameras(QWidget):
    def __init__(self, wshat):
        super(AvaliableCameras, self).__init__()
        layout = QVBoxLayout()
        combo = QComboBox()
        combo.setStyleSheet(
            "background-color: #444444;"
        )
        combo.addItem("web camera 1")
        combo.addItem("web camera 2")
        combo.addItem("web camera 3")
        layout.addWidget(combo)
        self.setLayout(layout)

class BackgroundImageGallery(QWidget):
    def __init__(self, background_image_directory_path, background_image_list):
        super(BackgroundImageGallery, self).__init__()
        layout = QHBoxLayout()
        scrollArea = QScrollArea()
        scrollArea.setStyleSheet(
            "QScrollBar:vertical"
            "{"
                "border: none;"
                "width: 7px;"
                "margin: 0 0 0 0;"
            "}"
        )
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget()
        gridLayout = QGridLayout(scrollAreaWidgetContents)
        scrollArea.setWidget(scrollAreaWidgetContents)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        

        i = 0
        for background_image_path in background_image_list:
            isFile = os.path.isfile(background_image_path)
            if (isFile):
                if (imghdr.what(background_image_path) != None):
                    gridLayout.addWidget(GalleryImage(os.path.relpath(background_image_path)), int((i-i%2)/2), i%2)
                    i += 1
                    
        layout.addWidget(scrollArea)
        self.setLayout(layout)

class GalleryImage(QWidget):
    def __init__(self, background_image_path):
        super(GalleryImage, self).__init__()
        self.background_image_path = background_image_path
        self.layout = QHBoxLayout()
        self.label = QLabel()
        self.label.mousePressEvent = self.selectBackgroundImage
        self.pixmap = QPixmap(self.background_image_path)
        self.pixmap = self.pixmap.scaled(160, 120)
        self.label.setPixmap(self.pixmap)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        
    def selectBackgroundImage(self, event):
        print(self.background_image_path)

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
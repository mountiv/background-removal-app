import sys

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
        layout = QVBoxLayout()
        layout.addWidget(SubTitle("Select a Virtual Background:"))
        self.dir_name_edit = QLineEdit()
        self.dir_name_edit.setStyleSheet(
            "margin-top: 9px;"
            "background-color: #444444;"
        )
        layout.addWidget(self.dir_name_edit, 2)
        self.openFolderBtn = QPushButton("Select Folder", self)
        layout.addWidget(self.openFolderBtn, 2)
        layout.addWidget(BackgroundImageGallery(), 2)
        self.setLayout(layout)
        self.setLayout(layout)
        self.openFolderBtn.clicked.connect(self.openFolderButtonClicked)

    def openFolderButtonClicked(self):
        self.openFileNamesDialog()

    def openFileNamesDialog(self):
        dialog = QFileDialog(self)
        bg_dir_path = str(dialog.getExistingDirectory(self, "Select Virtual Background Folder"))
        if bg_dir_path:
            self.dir_name_edit.setText(bg_dir_path)

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
        self.im = QPixmap("../basic_feature/human_img/1.jpg")
        self.im = self.im.scaled(720, 500)
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
        combo.setStyleSheet(
            "background-color: #444444;"
        )
        combo.addItem("web camera 1")
        combo.addItem("web camera 2")
        combo.addItem("web camera 3")
        layout.addWidget(combo)
        self.setLayout(layout)

class BackgroundImageGallery(QWidget):
    def __init__(self):
        super(BackgroundImageGallery, self).__init__()
        layout = QHBoxLayout()
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget()
        gridLayout = QGridLayout(scrollAreaWidgetContents)
        scrollArea.setWidget(scrollAreaWidgetContents)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg1.jpg'), 0, 0)
        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg2.jpg'), 0, 1)
        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg3.jpg'), 1, 0)
        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg1.jpg'), 1, 1)
        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg2.jpg'), 2, 0)
        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg3.jpg'), 2, 1)
        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg1.jpg'), 3, 0)
        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg2.jpg'), 3, 1)
        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg3.jpg'), 4, 0)
        gridLayout.addWidget(GalleryImage('../basic_feature/background_img/new/bg1.jpg'), 4, 1)    
        
        layout.addWidget(scrollArea)
        self.setLayout(layout)

class GalleryImage(QWidget):
    def __init__(self, background_image_path):
        super(GalleryImage, self).__init__()
        layout = QHBoxLayout()
        label = QLabel()
        pixmap = QPixmap(background_image_path)
        pixmap = pixmap.scaled(140, 100)
        label.setPixmap(pixmap)
        layout.addWidget(label)
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
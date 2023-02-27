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

        #left_layout

        #left_layout subtitle
        subtitle1_layout = QLabel("Select a Camera Source:")
        subtitle1_layout.setStyleSheet(
                    "color: #DEDEDE;"
                    "font-family:{default_font};"
                    "font-size: 18px;"
                    "font-weight: 600;"
                )
        
        #available cameras
        camera_combo = QComboBox()
        camera_combo.setStyleSheet(
            "background-color: #444444;"
        )
        camera_combo.addItem("web camera 1")
        camera_combo.addItem("web camera 2")
        camera_combo.addItem("web camera 3")
        camera_combo.setFixedWidth(int(app_width*(3/5)-32))

        #camera screen area
        im = QPixmap(f"../basic_feature/human_img/2.jpg")
        im = im.scaled(720, int(720*(9/16)))
        composite_screen = QLabel()
        composite_screen.setPixmap(im)

        #left_layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(subtitle1_layout)
        left_layout.addWidget(camera_combo)
        left_layout.addWidget(composite_screen)
        left_layout.addStretch()
        
        w_left_layout = QWidget()
        w_left_layout.setLayout(left_layout)
        w_left_layout.setFixedWidth(int(app_width * (3/5)))
        


        #right_layout

        #right_layout subtitle
        subtitle2_layout = QLabel("Select a Virtual Background:")
        subtitle2_layout.setStyleSheet(
                    "color: #DEDEDE;"
                    "font-family:{default_font};"
                    "font-size: 18px;"
                    "font-weight: 600;"
                )

        #background image path
        self.background_image_path = ""
        self.dir_name_edit = QLineEdit()
        self.dir_name_edit.setStyleSheet(
            "background-color: #444444;"
        )

        #open folder button
        self.openFolderBtn = QPushButton("Select Folder", self)
        self.openFolderBtn.clicked.connect(self.openFolderButtonClicked)
      
        #background image gallery, self.scroll_area
        self.background_image_directory_path = ""
        self.background_image_list = ['E:\\background\\Nature (1).png', 'E:\\background\\Nature (10).png', 'E:\\background\\Nature (11).png', 'E:\\background\\Nature (2).png', 'E:\\background\\Nature (3).png', 'E:\\background\\Nature (4).png', 'E:\\background\\Nature (5).png', 'E:\\background\\Nature (6).png', 'E:\\background\\Nature (7).png', 'E:\\background\\Nature (8).png', 'E:\\background\\Nature (9).png']

        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedHeight(app_height-140)
        self.scroll_area.setStyleSheet(
            "QScrollBar:vertical"
            "{"
                "border: none;"
                "width: 7px;"
                "margin: 0 0 0 0;"
            "}"
        )
        self.scroll_area.setWidgetResizable(True)
        scrollAreaWidgetContents = QWidget()
        self.gridLayout = QGridLayout(scrollAreaWidgetContents)
        self.scroll_area.setWidget(scrollAreaWidgetContents)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        

        #right_layout
        right_layout = QVBoxLayout()
        right_layout.addWidget(subtitle2_layout)
        right_layout.addWidget(self.dir_name_edit)
        right_layout.addWidget(self.openFolderBtn)
        right_layout.addWidget(self.scroll_area)
        right_layout.addStretch()

        w_right_layout = QWidget()
        w_right_layout.setLayout(right_layout)
        w_right_layout.setFixedWidth(int(app_width * (2/5)))



        #main layout
        layout = QHBoxLayout()
        layout.addWidget(w_left_layout)
        layout.addWidget(w_right_layout)
        self.setLayout(layout)

    def openFolderButtonClicked(self):
        self.openFileNamesDialog()

    def openFileNamesDialog(self):
        dialog = QFileDialog(self)
        background_image_directory_path = str(dialog.getExistingDirectory(self, "Select Virtual Background Folder"))
        if background_image_directory_path:
            self.dir_name_edit.setText(background_image_directory_path)
            self.background_image_directory_path = background_image_directory_path
            background_image_list = os.listdir(Path(background_image_directory_path))
            self.background_image_list.clear()
            for background_image_path in background_image_list:
                my_path = f'{Path(background_image_directory_path)}\{background_image_path}'
                isFile = os.path.isfile(my_path)
                if (isFile):
                    if (imghdr.what(my_path) != None):
                        self.background_image_list.append(my_path)
        i = 0
        for background_image_path in self.background_image_list:
            isFile = os.path.isfile(background_image_path)
            if (isFile):
                if (imghdr.what(background_image_path) != None):
                    bg_width = int(app_width*(2/5)/2-30)
                    bg = QPixmap(os.path.relpath(background_image_path))
                    bg = bg.scaled(bg_width, int(bg_width*(9/16)))
                    single_background_image = QLabel()
                    single_background_image.setPixmap(bg)

                    self.gridLayout.addWidget(single_background_image, int((i-i%2)/2), i%2)
                    i += 1
                        


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
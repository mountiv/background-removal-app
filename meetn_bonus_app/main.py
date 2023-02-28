import sys
import os
import imghdr

from pathlib import Path
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
    QFileDialog,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import QDate, Qt, QSize
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

default_font = "calibri"
app_width = 800
app_height = int(app_width*(9/16))

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # getting available cameras
        self.available_cameras = QCameraInfo.availableCameras()

		# if no camera found
        if not self.available_cameras:
            # exit the code
            print('no camera')
            # sys.exit()
                        
        self.setFixedSize(app_width, app_height)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("Meetn Bonus App")
        self.setStyleSheet("background-color: #333333")

        # left_layout
        # left_layout subtitle
        subtitle1_layout = QLabel("Select a Camera Source:")
        subtitle1_layout.setStyleSheet(
            "color: #DEDEDE;"
            "font-family:{default_font};"
            "font-size: 22px;"
            "font-weight: 600;"
        )
        
        # available cameras
        camera_combo = QComboBox()
        camera_combo.setStyleSheet(
            "color: #DDDDDD;"
            "background-color: #444444;"
            "border: 1px solid;"
            "border-color: #AAAAAA;"
            "border-radius: 2px;"
            "padding: 3px;"
            "font-size: 15px;"
        )
        camera_combo.setFixedWidth(int(app_width*(3/5)-32))

        # adding status tip to it
        camera_combo.setStatusTip("Choose camera to take pictures")

		# adding tool tip to it
        camera_combo.setToolTip("Select Camera")
        camera_combo.setToolTipDuration(2500)

		# adding items to the combo box
        camera_combo.addItems([camera.description() for camera in self.available_cameras])

        # camera screen area
        self.selected_background_image_path = f"../basic_feature/human_img/2.jpg"
        self.im = QPixmap(self.selected_background_image_path)
        self.im = self.im.scaled(720, int(720*(9/16)))
        self.composite_screen = QLabel()
        self.composite_screen.setPixmap(self.im)
        
        # left_layout
        left_layout = QVBoxLayout()
        left_layout.addWidget(subtitle1_layout)
        left_layout.addWidget(camera_combo)
        left_layout.addWidget(self.composite_screen)
        left_layout.addStretch()
        
        w_left_layout = QWidget()
        w_left_layout.setLayout(left_layout)
        w_left_layout.setFixedWidth(int(app_width * (3/5)))
        

        # right_layout
        # right_layout subtitle
        subtitle2_layout = QLabel("Select a Virtual Background:")
        subtitle2_layout.setStyleSheet(
            "color: #DEDEDE;"
            "font-family:{default_font};"
            "font-size: 22px;"
            "font-weight: 600;"
        )

        # background image path
        self.background_image_path = ""
        self.dir_name_edit = QLineEdit()
        self.dir_name_edit.setStyleSheet(
            "color: #DDDDDD;"
            "background-color: #444444;"
            "border: 1px solid;"
            "border-color: #AAAAAA;"
            "border-radius: 2px;"
            "padding: 3px;"
            "font-size: 15px;"
        )

        # open folder button
        self.openFolderBtn = QPushButton("Select Folder", self)
        self.openFolderBtn.setStyleSheet(
            "color: #DDDDDD;"
            "border: 1px solid;"
            "border-color: #AAAAAA;"
            "border-radius: 2px;"
            "padding: 5px;"
        )
        self.openFolderBtn.clicked.connect(self.openFolderButtonClicked)

        # backgrouned image list, listItem Widget
        self.background_image_list = []
        self.listwidget = QListWidget()
        self.listwidget.setFixedHeight(app_height-140)
        self.listwidget.setStyleSheet(
            "QScrollBar:vertical"
            "{"
                "border: none;"
                "width: 7px;"
                "margin: 0 0 0 0;"
            "}"
        )
        self.listwidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.listwidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listwidget.clicked.connect(self.selectBackgroundImage)

        # right_layout
        right_layout = QVBoxLayout()
        right_layout.addWidget(subtitle2_layout)
        right_layout.addWidget(self.dir_name_edit)
        right_layout.addWidget(self.openFolderBtn)
        right_layout.addWidget(self.listwidget)
        right_layout.addStretch()

        w_right_layout = QWidget()
        w_right_layout.setLayout(right_layout)
        w_right_layout.setFixedWidth(int(app_width * (2/5)))


        # main layout
        layout = QHBoxLayout()
        layout.addWidget(w_left_layout)
        layout.addWidget(w_right_layout)
        self.setLayout(layout)

    def openFolderButtonClicked(self):
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
                    item = QListWidgetItem()
                    icon = QIcon()
                    icon.addFile(os.path.relpath(background_image_path), QSize(10,10))
                    item.setIcon(icon)
                    item.setText(background_image_path)
                    self.listwidget.addItem(item)
                    i += 1

    def selectBackgroundImage(self, qmodelindex):
        item = self.listwidget.currentItem()
        self.selected_background_image_path = os.path.relpath(item.text())
        self.im = QPixmap(self.selected_background_image_path)
        self.im = self.im.scaled(720, int(720*(9/16)))
        self.composite_screen.setPixmap(self.im)
        print(item.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()

    now = QDate.currentDate()
    print(now.toString(Qt.DateFormat.ISODate))
    print(now.toString(Qt.DateFormat.RFC2822Date))
        
    window.show()
    sys.exit(app.exec())
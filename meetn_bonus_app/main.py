import sys
import os
import imghdr
import numpy as np
import mediapipe as mp
import cv2

from pathlib import Path
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PySide6.QtCore import QThread, Signal, Slot
from PyQt6.QtGui import QPixmap, QIcon, QImage, QColor
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QLabel,
    QMainWindow,
    QComboBox,
    QLineEdit,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
)

default_font = "calibri"
app_width = 800
app_height = int(app_width*(9/16))
# screen_width = int(app_width*(3/5))
# screen_height = int(screen_width*(9/16))
screen_width = 640
screen_height = 480
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

class Thread(QThread):
    updateFrame = Signal(QImage)


    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True
        self.cap = True
        self.bg_path = ""

    def set_file(self, fname):
        self.bg_path = fname

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.status:
            ret, frame = self.cap.read()
            if not ret:
                continue

            if self.bg_path == "":
                color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                h, w, ch = color_frame.shape
                img = QImage(color_frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
                scaled_img = img.scaled(screen_width, screen_height)
            else:
                color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                width = screen_width
                height = screen_height

                results = selfie_segmentation.process(color_frame)

                # extract segmented mask
                mask = results.segmentation_mask
                condition = np.stack((mask,) * 3, axis=-1) > 0.5

                bg_img = cv2.imread(self.bg_path)

                # resizing background Image
                bg_img = cv2.resize(bg_img, (width, height))

                output_image = np.where(condition, frame, bg_img)

                # Creating and scaling QImage
                h, w, ch = output_image.shape
                img = QImage(output_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
                scaled_img = img.scaled(screen_width, screen_height)

            # Emit signal
            self.updateFrame.emit(scaled_img)
        sys.exit(-1)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # getting available cameras
        self.available_cameras = QCameraInfo.availableCameras()

		# if no camera found
        if not self.available_cameras:
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
            "font-size: 20px;"
            "font-weight: 500;"
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
        if not self.available_cameras:
            self.composite_screen = QLabel("There are no cameras available.")
            self.composite_screen.setStyleSheet(
                "font-size: 20px;"
                "color: #777777;"
            )
            # sys.exit()
        else: 
            self.composite_screen = QLabel()
            self.composite_screen.setFixedSize(int(app_width*(3/5)-32), int((app_width*(3/5)-32)*9/16))

        self.th = Thread()
        self.th.updateFrame.connect(self.setImage)
        self.th.start()
        
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
            "font-size: 20px;"
            "font-weight: 500;"
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
                "width: 5px;"
                "margin: 0 0 0 0;"
                "background-color: #777777;"
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

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

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
                    item.setSizeHint(QSize(200,100))
                    icon = QIcon()
                    icon.addFile(os.path.relpath(background_image_path))
                    item.setIcon(icon)
                    item.setText(background_image_path)
                    item.setForeground(QColor("#777777"))
                    self.listwidget.addItem(item)
                    self.listwidget.setIconSize(QSize(160, 90))
                    i += 1
    @Slot()
    def selectBackgroundImage(self):
        item = self.listwidget.currentItem()
        self.th.set_file(os.path.relpath(item.text()))

    # method to select camera
    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()

    @Slot(QImage)
    def setImage(self, image):
        self.composite_screen.setPixmap(QPixmap.fromImage(image))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
        
    window.show()
    sys.exit(app.exec())
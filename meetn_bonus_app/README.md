# Meetn Bonus App

The goal of this project is to build the desktop application that remove natural background and replace in my local background image.
Todo this I used Python. Especially used libraries: open-cv, mediapipe, numpy, pyqt5, pyqt6, pyside6.

## Running the project

If you installed Python in your PC already, and installed libraries above. You can run the project using command `python main.py` in terminal in project directory.

## Build the project for Windows and MacOS

Generally, most Python application can be built via below command.

```pyinstaller.exe --onefile --windowed main.py```

But, in this project it courses error like below image.

Because of mediapipe library.
In this project, we use this library, but using above command, not include this labrary and courses error.
So, I used `auto-py-to-exe` command.


## Author

© me
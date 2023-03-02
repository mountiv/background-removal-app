# Meetn Bonus App

The goal of this project is to build the desktop application that remove natural background and replace in my local background image.
Todo this I used Python. Especially used libraries: open-cv, mediapipe, numpy, pyqt5, pyqt6, pyside6.

## Running the project

If you installed Python in your PC already, and installed libraries above. You can run the project using command `python main.py` in terminal in project directory.

## Build the project for Windows and MacOS

Generally, most Python application can be built via below command.

```pyinstaller.exe --onefile --windowed main.py```

But, in this project it courses error like below image.

<div align="center">

![Error](https://user-images.githubusercontent.com/121834775/222467525-fda23a12-c731-47f1-b877-a4fdd381841a.png)
</div>

Because of mediapipe library.
In this project, we use this library, but using above command, not include this labrary and courses error.
So, I used `auto-py-to-exe` command.

<div align="center">

![AutoPyToExe](https://user-images.githubusercontent.com/121834775/222467808-2c7f66b5-8d1a-46ac-a871-4a0b08956a27.png)
</div>

## Author

© me

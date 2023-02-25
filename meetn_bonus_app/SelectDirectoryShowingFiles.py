from PyQt5 import QtCore, QtWidgets

class DirProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, fsModel):
        super().__init__()
        self.fsModel = fsModel
        self.setSourceModel(fsModel)

    def lessThan(self, left, right):
        # QFileSystemModel populates its entries with some delay, which results 
        # in the proxy model not able to do the proper sorting (usually showing 
        # directories first) since the proxy does not always "catch up" with the 
        # source sorting; so, this has to be manually overridden by 
        # force-checking the entry type of the index.
        leftIsDir = self.fsModel.fileInfo(left).isDir()
        if leftIsDir != self.fsModel.fileInfo(right).isDir():
            return leftIsDir
        return super().lessThan(left, right)

    def flags(self, index):
        flags = super().flags(index)
        # map the index to the source and check if it's a directory or not
        if not self.fsModel.fileInfo(self.mapToSource(index)).isDir():
            # if it is a directory, remove the enabled flag
            flags &= ~QtCore.Qt.ItemIsEnabled
        return flags


class Test(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        self.lineEdit = QtWidgets.QLineEdit()
        layout.addWidget(self.lineEdit)
        self.selectBtn = QtWidgets.QToolButton(text='...')
        layout.addWidget(self.selectBtn)
        self.selectBtn.clicked.connect(self.selectDirectory)

    def selectDirectory(self):
        dialog = QtWidgets.QFileDialog(self, windowTitle='Select directory')
        dialog.setDirectory(self.lineEdit.text() or __file__)
        dialog.setFileMode(dialog.Directory)
        dialog.setOptions(dialog.DontUseNativeDialog)

        # find the underlying model and set our own proxy model for it
        for view in self.findChildren(QtWidgets.QAbstractItemView):
            if isinstance(view.model(), QtWidgets.QFileSystemModel):
                proxyModel = DirProxyModel(view.model())
                dialog.setProxyModel(proxyModel)
                break

        # try to hide the file filter combo
        fileTypeCombo = dialog.findChild(QtWidgets.QComboBox, 'fileTypeCombo')
        if fileTypeCombo:
            fileTypeCombo.setVisible(False)
            dialog.setLabelText(dialog.FileType, '')

        if dialog.exec_():
            self.lineEdit.setText(dialog.selectedFiles()[0])

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Test()
    w.show()
    sys.exit(app.exec_())
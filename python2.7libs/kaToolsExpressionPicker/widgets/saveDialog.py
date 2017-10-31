from PySide2 import QtWidgets, QtCore, QtGui

class saveDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(QtWidgets.QDialog).__init__(self, parent)
        self.finished.connect(self.onDialogFinished())


    def onDialogFinished(self, result):
        pass

from PySide2 import QtWidgets, QtCore, QtGui
from kaToolsExpressionPicker.widgets import snippet

reload(snippet)


class snippetDialog(QtWidgets.QDialog):

    def __init__(self, parent = None, f=0):
        super(snippetDialog, self).__init__(parent, f)
        

        layout = QtWidgets.QVBoxLayout()
        snippetTextArea = snippet.snippet()

        layout.addWidget(snippetTextArea)

        self.setLayout(layout)


        self.setFocus()
from PySide2 import QtWidgets, QtCore, QtGui
from kaToolsExpressionPicker.widgets import snippet
import hou

reload(snippet)


class snippetDialog(QtWidgets.QDialog):

    def __init__(self, parent = None, f=0, text = ""):
        super(snippetDialog, self).__init__(parent, f)
        
        layout = QtWidgets.QVBoxLayout()
        self.snippetTextArea = snippet.snippet()
        self.snippetTextArea.setText(text)

        buttonLayout = QtWidgets.QHBoxLayout()
        okButton = QtWidgets.QPushButton("OK")
        cancelButton = QtWidgets.QPushButton("Cancel")

        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        
        layout.addWidget(self.snippetTextArea)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.setFocus()
        self.snippetTextArea.setFocus()

        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)
        
        self.setStyleSheet(hou.qt.styleSheet())

    
    def getNewText(self):
        return self.snippetTextArea.toPlainText()
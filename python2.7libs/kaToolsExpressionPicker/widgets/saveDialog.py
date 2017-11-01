from PySide2 import QtWidgets, QtCore, QtGui


class saveDialog(QtWidgets.QDialog):

    def __init__(self, parent = None, f=0):
        super(saveDialog, self).__init__(parent, f)
        self.setFocus()

        layout = QtWidgets.QVBoxLayout()
        catLayout = QtWidgets.QHBoxLayout()
        nameLayout = QtWidgets.QHBoxLayout()
        buttonLayout = QtWidgets.QHBoxLayout()
        catLabel = QtWidgets.QLabel("Category: ")
        nameLabel = QtWidgets.QLabel("Name    : ")
        self.catTextLine = QtWidgets.QLineEdit()
        self.nameTextLine = QtWidgets.QLineEdit()
        okButton = QtWidgets.QPushButton("OK")
        cancelButton = QtWidgets.QPushButton("Cancel")

        catLayout.addWidget(catLabel)
        catLayout.addWidget(self.catTextLine)
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameTextLine)
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        layout.addLayout(catLayout)
        layout.addLayout(nameLayout)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.catTextLine.setFocus()
        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)


    def getCatandName(self):
        return self.catTextLine.text(), self.nameTextLine.text()
        



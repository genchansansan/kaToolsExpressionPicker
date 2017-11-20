from PySide2 import QtWidgets, QtCore, QtGui


###  char formats
varTypeFormat = QtGui.QTextCharFormat()
#varTypeFormat.setFontWeight(QtGui.QFont.Bold)
varTypeFormat.setForeground(QtCore.Qt.magenta)



### patterns
__varTypePatterns = ["int", "float", "string", "vector"
    , "matrix", "matrix3", "vector4", "vector2", "matrix2"]
__varTypePatterns = ["\\b" + pattern + "\\b" for pattern in __varTypePatterns]







# ("pattern", format)
vexRules = []

[vexRules.append((pattern, varTypeFormat)) for pattern in __varTypePatterns]


from PySide2 import QtWidgets, QtCore, QtGui


###  char formats
__varTypeFormat = QtGui.QTextCharFormat()
#__varTypeFormat.setFontWeight(QtGui.QFont.Bold)
__varTypeFormat.setForeground(QtCore.Qt.magenta)

__varCommentFormat = QtGui.QTextCharFormat()
__varCommentFormat.setForeground(QtCore.Qt.yellow)



### patterns
__varTypePatterns = ["int", "float", "string", "vector"
    , "matrix", "matrix3", "vector4", "vector2", "matrix2"]
__varTypePatterns = ["\\b" + pattern + "\\b" for pattern in __varTypePatterns]

__singleLinePattern = ["//"]
__singleLinePattern = [pattern + "*" for pattern in __varTypePatterns]

__multilinePatternsStart = ["/\\*"]
__multilinePatternsEnd = ["\\*/"]

# ("pattern", format)
vexRules = []
[vexRules.append((pattern, __varTypeFormat)) for pattern in __varTypePatterns]

multiLineRules = []
[multiLineRules.append((start, end, __varCommentFormat)) for (start, end) in zip(__multilinePatternsStart, __multilinePatternsEnd)]

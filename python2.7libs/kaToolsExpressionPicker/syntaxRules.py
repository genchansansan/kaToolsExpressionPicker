from PySide2 import QtWidgets, QtCore, QtGui


###  char formats
__varFormat = QtGui.QTextCharFormat()
#__varFormat.setFontWeight(QtGui.QFont.Bold)
__varFormat.setForeground(QtCore.Qt.magenta)


__commentFormat = QtGui.QTextCharFormat()
__commentFormat.setForeground(QtCore.Qt.yellow)



### patterns
__varTypePatterns = ["int", "float", "string", "vector"
    , "matrix", "matrix3", "vector4", "vector2", "matrix2"]
__varTypePatterns = ["\\b" + pattern + "\\b" for pattern in __varTypePatterns]



__singleLinePattern = ["//"]
#__singleLinePattern = [pattern + "" for pattern in __singleLinePattern]

__multilinePatternsStart = ["/\\*", "\"", "'"]
__multilinePatternsEnd = ["\\*/", "\"", "'"]

# ("pattern", format)
vexRules = []
[vexRules.append((pattern, __varFormat)) for pattern in __varTypePatterns]


singleLineRules = []
[singleLineRules.append((pattern, __commentFormat)) for pattern in __singleLinePattern]


multiLineRules = []
[multiLineRules.append((start, end, __commentFormat)) for (start, end) in zip(__multilinePatternsStart, __multilinePatternsEnd)]

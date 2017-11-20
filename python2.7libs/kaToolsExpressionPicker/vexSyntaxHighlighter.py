from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import syntaxRules

reload(syntaxRules)

class vexSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent = None):
        super(vexSyntaxHighlighter, self).__init__(parent)
    


    def highlightBlock(self, text):
        for pattern, format in syntaxRules.vexRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import syntaxRules

reload(syntaxRules)

class vexSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent = None):
        super(vexSyntaxHighlighter, self).__init__(parent)
    


    def highlightBlock(self, text):
        for pattern, charFormat in syntaxRules.vexRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, charFormat)
                index = expression.indexIn(text, index + length)

        for start, end, charFormat in syntaxRules.multiLineRules:
            print "start"
            startExp = QtCore.QRegExp(start)
            endExp = QtCore.QRegExp(end)
            startIndex = 0
            self.setCurrentBlockState(0)

            if self.previousBlockState() != 1:
                startIndex = startExp.indexIn(text)
            while startIndex >= 0:
                print "start index: ", startIndex
                #length = startExp.matchedLength()
                endIndex = endExp.indexIn(text, startIndex)
                print "end index: ", endIndex
                
                if endIndex == -1:
                    self.setCurrentBlockState(1)
                    commentLength = len(text) - startIndex
                else :# if endIndex >= startIndex:
                    commentLength = endIndex - startIndex + endExp.matchedLength()

                self.setFormat(startIndex, commentLength, charFormat)
                startIndex = startExp.indexIn(text, startIndex + commentLength)

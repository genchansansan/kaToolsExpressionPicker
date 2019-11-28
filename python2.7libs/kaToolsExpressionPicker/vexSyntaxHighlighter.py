from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import syntaxRules

reload(syntaxRules)

class vexSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent = None):
        super(vexSyntaxHighlighter, self).__init__(parent)
    


    def highlightBlock(self, text):
        print "text :", text
        for pattern, charFormat in syntaxRules.vexRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, charFormat)
                index = expression.indexIn(text, index + length)

        
        for pattern, charFormat in syntaxRules.singleLineRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = len(text)
                self.setFormat(index, length - index, charFormat)
                index = expression.indexIn(text, index + length)



        count = 0
        self.setCurrentBlockState(0)
        self.setCurrentBlockState(self.previousBlockState())
        if self.currentBlockState() == -1:
            self.setCurrentBlockState(0)
        print "current : ", self.currentBlockState()

        for start, end, charFormat in syntaxRules.multiLineRules:
            startExp = QtCore.QRegExp(start)
            endExp = QtCore.QRegExp(end)
            startIndex = 0
            existPrev = 0

            if self.currentBlockState() == 0:
                startIndex = startExp.indexIn(text)

            if self.currentBlockState() != 0:
                bi = "%04d" % int(format(self.currentBlockState(), 'b'))
                print "bi : ", bi, -1-count

                if bi[-1-count] != "1" :
                    startIndex = startExp.indexIn(text)
                else:
                    existPrev = 1
                
                
            while startIndex >= 0:
                print "existPrev", existPrev
                if existPrev == 0:
                    self.setCurrentBlockState(self.currentBlockState() + 2 ** count)
                    endIndex = endExp.indexIn(text, startIndex+1)
                    existPrev = 1
                else:
                    endIndex = endExp.indexIn(text, startIndex)
                    #self.setCurrentBlockState(self.currentBlockState() - 2 ** count)
                    if endIndex != -1:
                        existPrev = 0

                
                if endIndex == -1:
                    #self.setCurrentBlockState(self.currentBlockState() + 2 ** count)
                    commentLength = len(text) - startIndex
                else :
                    self.setCurrentBlockState(self.currentBlockState() - 2 ** count)

                    bi = "%04d" % int(format(self.currentBlockState(), 'b'))

                    if bi[-1-count] == "0" :
                        commentLength = endIndex - startIndex + endExp.matchedLength()
                    else:
                        commentLength = len(text) - startIndex

                self.setFormat(startIndex, commentLength, charFormat)
                print count, " start ", startIndex, endIndex
                print "current " , self.currentBlockState()
                startIndex = startExp.indexIn(text, startIndex + commentLength)
                

            count+=1

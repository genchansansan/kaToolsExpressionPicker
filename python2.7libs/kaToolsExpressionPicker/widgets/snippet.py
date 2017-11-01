import hou
from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import stylesheet

reload(stylesheet)



class snippet(QtWidgets.QTextEdit):
    def __init__(self, parent=None, pathLabel = None):
        super(snippet, self).__init__(parent)
        self.pathLabel = pathLabel

        self.setFontPointSize(12)


    def dragEnterEvent(self, event):
        print "enter to text area", event.mimeData().text()
        event.accept()
        #event.acceptProposedAction()
        pass


    def dropEvent(self, event):
        text = event.mimeData().text()
        print text, event.mimeData().formats()
        parm = hou.parm(text)
        if parm != None:
            mime = QtCore.QMimeData()
            mime.setText("")
            newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
            super(snippet, self).dropEvent(newEvent)
            self.pathLabel.setText(text)
            self.setText(parm.eval())
            self.pathLabel.setStyleSheet(stylesheet.styles["valid"])
        else:
            if hou.parm(self.pathLabel.text()) != None:
                if hou.node(text) == None:
                    super(snippet, self).dropEvent(event)
                    #self.pathLabel.setStyleSheet(stylesheet.styles["valid"])
                    if hou.parm(self.pathLabel.text()).name() == "snippet":
                        self.parmCreate(hou.parm(self.pathLabel.text()).node())
                else:
                    mime = QtCore.QMimeData()
                    mime.setText("")
                    newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
                    super(snippet, self).dropEvent(newEvent)
                    self.pathLabel.setText("Invalid. Drop a parameter:")
                    self.pathLabel.setStyleSheet(stylesheet.styles["invalid"])
            else:
                mime = QtCore.QMimeData()
                mime.setText("")
                newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
                super(snippet, self).dropEvent(newEvent)
                self.pathLabel.setText("Invalid. Drop a parameter first:")
                self.pathLabel.setStyleSheet(stylesheet.styles["invalid"])



    def parmCreate(self, node):
        try:
            import vexpressionmenu
            parmname = 'snippet'

            vexpressionmenu.createSpareParmsFromChCalls(node, parmname)
        except error:
            print "cannot create parms"
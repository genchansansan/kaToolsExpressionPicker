import hou
from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import stylesheet

reload(stylesheet)



class snippet(QtWidgets.QTextEdit):
    def __init__(self, parent=None, pathLabel = None):
        super(snippet, self).__init__(parent)
        self.pathLabel = pathLabel
        self.setFontPointSize(12)
        self.setAcceptRichText(True)


    def dragEnterEvent(self, event):
        super(snippet, self).dragEnterEvent(event)
        #print "enter to text area", event.type()
        #event.accept()
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        super(snippet, self).dragMoveEvent(event)
        #print "drag move", event.mimeData().formats()
        #event.accept()
        event.acceptProposedAction()


    def dropEvent(self, event):
        text = event.mimeData().text()
        print event.mimeData().formats()
        parm = hou.parm(text)
        if parm != None:
            mime = QtCore.QMimeData()
            mime.setText("")
            newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
            super(snippet, self).dropEvent(newEvent)
            self.pathLabel.setText(text)
            if parm.eval() != "":
                self.setText(parm.eval())
            else:
                pass
            self.pathLabel.setStyleSheet(stylesheet.styles["valid"])
        else:
            if hou.parm(self.pathLabel.text()) != None:
                if hou.node(text) == None:
                    if self.toPlainText() == "":
                        self.setText(" ")
                    super(snippet, self).dropEvent(event)
                    #self.insertFromMimeData(event.mimeData())
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

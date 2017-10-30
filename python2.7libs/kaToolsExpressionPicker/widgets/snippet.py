import hou
from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import stylesheet

reload(stylesheet)



class snippet(QtWidgets.QTextEdit):
    def __init__(self, parent=None, label = None):
        super(snippet, self).__init__(parent)
        self.label = label

        self.setFontPointSize(12)


    def dragEnterEvent(self, event):
        event.acceptProposedAction()


    def dropEvent(self, event):
        text = event.mimeData().text()
        parm = hou.parm(text)
        if parm != None:
            mime = QtCore.QMimeData()
            mime.setText("")
            newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
            super(snippet, self).dropEvent(newEvent)
            self.label.setText(text)
            self.setText(parm.eval())
            self.label.setStyleSheet(stylesheet.styles["valid"])
        elif text[0]!="/":
            super(snippet, self).dropEvent(event)
            self.label.setStyleSheet(stylesheet.styles["valid"])
            if hou.parm(self.label.text()).name() == "snippet":
                self.parmCreate(hou.parm(self.label.text()).node())
        else:
            mime = QtCore.QMimeData()
            mime.setText("")
            newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
            super(snippet, self).dropEvent(newEvent)
            self.label.setText("Invalid. Drop a parameter:")
            self.label.setStyleSheet(stylesheet.styles["invalid"])



    def parmCreate(self, node):
        try:
            import vexpressionmenu
            parmname = 'snippet'

            vexpressionmenu.createSpareParmsFromChCalls(node, parmname)
        except error:
            print "cannot create parms"
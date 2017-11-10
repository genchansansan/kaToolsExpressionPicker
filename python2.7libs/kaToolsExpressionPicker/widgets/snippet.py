import hou
from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import stylesheet

reload(stylesheet)



class snippet(QtWidgets.QTextEdit):
    def __init__(self, parent=None, pathLabel = None):
        super(snippet, self).__init__(parent)
        self.pathLabel = pathLabel
        #self.setFontPointSize(12)
        self.setTabStopWidth(20)
        self.setAcceptRichText(True)
        self.setMouseTracking(True)



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
        #print event.mimeData().formats()
        parm = hou.parm(text)
        if parm != None:
            mime = QtCore.QMimeData()
            mime.setText("")
            newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
            super(snippet, self).dropEvent(newEvent)
            self.pathLabel.setText(text)
            self.setText(parm.eval())

            self.pathLabel.setStyleSheet(stylesheet.styles["valid"])

            self.setUpCallback(parm.node())
        else:
            if hou.parm(self.pathLabel.text()) != None:
                if hou.node(text) == None:
                    currentSize = self.fontPointSize()
                    super(snippet, self).dropEvent(event)
                    cursor = self.textCursor()
                    self.selectAll()
                    self.setFontPointSize(currentSize)
                    self.setTextCursor(cursor)

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
                '''
                mime = QtCore.QMimeData()
                mime.setText("")
                newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
                super(snippet, self).dropEvent(newEvent)
                '''
                currentSize = self.fontPointSize()
                super(snippet, self).dropEvent(event)
                cursor = self.textCursor()
                self.selectAll()
                self.setFontPointSize(currentSize)
                self.setTextCursor(cursor)
                self.pathLabel.setText("Invalid. Drop a parameter first:")
                self.pathLabel.setStyleSheet(stylesheet.styles["invalid"])


    def mouseMoveEvent(self, event):
        #print "mouse move"
        super(snippet, self).mouseMoveEvent(event)
        self.setFocus()


    def keyPressEvent(self, event):
        super(snippet, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Plus:
            if event.modifiers() == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier:
                #print "press contol plus"
                cursor = self.textCursor()
                self.selectAll()
                self.setFontPointSize(self.fontPointSize()+2)
                self.setTextCursor(cursor)
        elif event.key() == QtCore.Qt.Key_Minus:
            if event.modifiers() == QtCore.Qt.ControlModifier :
                #print "press contol minus"
                cursor = self.textCursor()
                self.selectAll()
                self.setFontPointSize(self.fontPointSize()-2)
                self.setTextCursor(cursor)




    def parmCreate(self, node):
        try:
            import vexpressionmenu
            parmname = 'snippet'

            vexpressionmenu.createSpareParmsFromChCalls(node, parmname)
        except error:
            print "cannot create parms"



    def onParmChanged(self, **kwargs):
        linkedParm = hou.parm(self.pathLabel.text())
        parms = kwargs["parm_tuple"]
        print len(parms)
        for parm in parms:
            if linkedParm != None and parm !=None:
                if self.toPlainText() != parm.eval():
                    self.setText(parm.eval())
                    break
        pass



    def setUpCallback(self, node):
        self.removeCallBack(node)
        print "add"
        node.addEventCallback((hou.nodeEventType.ParmTupleChanged,), self.onParmChanged)

    def removeCallBack(self, node):
        node.removeAllEventCallbacks()

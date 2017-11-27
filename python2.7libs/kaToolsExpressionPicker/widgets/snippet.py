import hou
from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import stylesheet, vexSyntaxHighlighter

reload(stylesheet)
reload(vexSyntaxHighlighter)



class snippet(QtWidgets.QTextEdit):

    currentSize = 12

    def __init__(self, parent=None, pathLabel = None):
        super(snippet, self).__init__(parent)
        self.pathLabel = pathLabel
        #self.setFontPointSize(12)
        self.setTabStopWidth(20)
        self.setAcceptRichText(True)
        self.setMouseTracking(True)
        self.textChanged.connect(self.onSnippetTextEdited)
        vexSyntax = vexSyntaxHighlighter.vexSyntaxHighlighter(self.document())




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
            if hou.parm(self.pathLabel.text()) !=None:
                self.removeCallBack(hou.parm(self.pathLabel.text()).node())
            if isinstance(parm.eval(),str):
                mime = QtCore.QMimeData()
                mime.setText("")
                newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
                super(snippet, self).dropEvent(newEvent)

                self.pathLabel.setText(text)
                self.setText(parm.eval())
                self.pathLabel.setStyleSheet(stylesheet.styles["valid"])

                self.setUpCallback(parm.node())
            else:
                mime = QtCore.QMimeData()
                mime.setText("")
                newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
                super(snippet, self).dropEvent(newEvent)
                self.pathLabel.setText("Invalid. Only String Parameter is acceptable:")
                self.pathLabel.setStyleSheet(stylesheet.styles["invalid"])
        else:
            ###
            ### droped info is not path to parm
            ###
            if hou.parm(self.pathLabel.text()) != None:
                ###
                ### parm is already set
                ###
                if hou.node(text) == None:
                    ###
                    ### dropping a template
                    ###
                    self.dropTemplate(event)
                    if hou.parm(self.pathLabel.text()).name() == "snippet":
                        self.parmCreate(hou.parm(self.pathLabel.text()).node())
                else:
                    ###
                    ### dropping node or something
                    ###
                    if hou.parm(self.pathLabel.text()) !=None:
                        self.removeCallBack(hou.parm(self.pathLabel.text()).node())
                    mime = QtCore.QMimeData()
                    mime.setText("")
                    newEvent = QtGui.QDropEvent(event.pos(), event.dropAction(), mime, event.mouseButtons(), event.keyboardModifiers())
                    super(snippet, self).dropEvent(newEvent)
                    self.pathLabel.setText("Invalid. Drop a parameter:")
                    self.pathLabel.setStyleSheet(stylesheet.styles["invalid"])
            else:
                ###
                ### parm is not set
                ###
                self.dropTemplate(event)
                self.pathLabel.setText("Invalid. Drop a parameter first:")
                self.pathLabel.setStyleSheet(stylesheet.styles["invalid"])


    def dropTemplate(self, event):
        #print self.currentSize
        #currentSize = self.fontPointSize()
        super(snippet, self).dropEvent(event)
        cursor = self.textCursor()
        self.selectAll()
        self.setFontPointSize(self.currentSize)
        self.setTextCursor(cursor)


    def mouseMoveEvent(self, event):
        #print "mouse move"
        super(snippet, self).mouseMoveEvent(event)
        self.setFocus()


    def keyPressEvent(self, event):
        super(snippet, self).keyPressEvent(event)
        text = self.toPlainText()
        if "\t" in text:
            doc = self.document()
            cursor = doc.find("\t")
            cursor.deleteChar()
            cursor.insertText("    ")
        if event.key() == QtCore.Qt.Key_Plus:
            if event.modifiers() == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier:
                #print "press contol plus"
                cursor = self.textCursor()
                self.selectAll()
                self.setFontPointSize(self.fontPointSize()+2)
                self.currentSize = self.fontPointSize()
                self.setTextCursor(cursor)
        elif event.key() == QtCore.Qt.Key_Minus:
            if event.modifiers() == QtCore.Qt.ControlModifier :
                #print "press contol minus"
                cursor = self.textCursor()
                self.selectAll()
                self.setFontPointSize(self.fontPointSize()-2)
                self.currentSize = self.fontPointSize()
                self.setTextCursor(cursor)



    def onSnippetTextEdited (self):
        #print "edit in", self.currentSize
        text = self.toPlainText()

        parm = hou.parm(self.pathLabel.text())
        if parm != None:
            parm.set(text)
            self.pathLabel.setStyleSheet(stylesheet.styles["valid"])
        else:
            self.pathLabel.setText("Drag & Drop a parameter above:")
            self.pathLabel.setStyleSheet(stylesheet.styles["invalid"])

        if text == "" or text.startswith("\n"):
            font = QtGui.QFont()
            font.setPointSize(self.currentSize)
            self.setCurrentFont(font)
            pass
        else:
            #self.currentSize = self.fontPointSize()
            pass





    def parmCreate(self, node):
        try:
            import vexpressionmenu
            parmname = 'snippet'
            vexpressionmenu.createSpareParmsFromChCalls(node, parmname)
        except error:
            print "cannot create parms"



    def onParmChanged(self, **kwargs):
        try:
            linkedParm = hou.parm(self.pathLabel.text())
            parms = kwargs["parm_tuple"]
            
            for parm in parms:
                if linkedParm != None and parm !=None:
                    if type(linkedParm.eval()) == type(parm.eval()):
                        if self.toPlainText() != parm.eval():
                            self.setText(parm.eval())
                            break
            pass
        except error:
            print error


    def setUpCallback(self, node):
        self.removeCallBack(node)
        #print "add"
        node.addEventCallback((hou.nodeEventType.ParmTupleChanged,), self.onParmChanged)

    def removeCallBack(self, node):
        #print "remove event handler", node.name()
        node.removeAllEventCallbacks()

import hou
from PySide2 import QtWidgets, QtCore, QtGui


class expressionTreeWidget(QtWidgets.QTreeWidget):
    
    selected = []
    mimeData = QtCore.QMimeData()

    def __init__(self, parent=None):
        QtWidgets.QTreeWidget.__init__(self, parent)

        self.setItemsExpandable(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        #self.setDragDropMode(self.DragDrop)
        self.setDragDropMode(self.InternalMove)
        self.setAlternatingRowColors(True)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

    
    def mousePressEvent(self, event):
        super(expressionTreeWidget, self).mousePressEvent(event)
        self.selected = self.selectedItems()
        if len(self.selected)>0:
            self.mimeData = QtCore.QMimeData()
            #mimeData.setData("application/treeItem", "1")
            #self.mimeData.setData("text/plain", self.selected[0].text(0))
            self.mimeData.setText(self.selected[0].text(1))
            #print self.selected[0].text(1)
            #print "mouse press", self.mimeData.text()
            #mimeData = super(expressionTreeWidget, self).mimeData(self.selected)
            drag = QtGui.QDrag(self)
            #drag.setMimeData(mimeData)
            drag.setMimeData(self.mimeData)
            drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)
            #drag.start(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction)
            pass

    def mouseReleaseEvent(self, event):
        #super(expressionTreeWidget, self).mouseReleaseEvent(event)
        print "release: ", event
        pass
        '''
        return_val = super( QtWidgets.QTreeWidget, self ).mouseReleaseEvent( event )
        #print "mouse release"
        #print hou.ui.curDesktop().paneTabUnderCursor().type()
        widget = QtWidgets.QApplication.instance().widgetAt(event.globalX(), event.globalY())
        if widget:
            self.searchChildren(widget)
        '''


    def mouseMoveEvent(self, event):
        #super(expressionTreeWidget, self).mouseMoveEvent(event)
        #print "move: ", event
        pass
        
    def searchChildren(self, parent):
        for child in parent.children():
                if child:
                    if isinstance(child, QtGui.QTextFrame):
                        pass
                    self.searchChildren(child)

    def dragEnterEvent(self, event):
        #super(expressionTreeWidget, self).dragEnterEvent(event)
        event.acceptProposedAction()
        #print "dragenter: ", event.mimeData().text()
        pass

    def dragMoveEvent(self, event):
        #super(expressionTreeWidget, self).dragMoveEvent(event)
        #print "drag move"
        event.acceptProposedAction()
        pass


    def dropEvent(self, event):
        #if event.mimeData().hasFormat(self.mimeTypes()[0]):
        print "drop: ", event.mimeData().formats()
        super(expressionTreeWidget, self).dropEvent(event)
        
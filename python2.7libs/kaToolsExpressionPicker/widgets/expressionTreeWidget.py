import hou
from PySide2 import QtWidgets, QtCore, QtGui


class expressionTreeWidget(QtWidgets.QTreeWidget):
    mimeData = QtCore.QMimeData()
    def __init__(self, parent=None):
        QtWidgets.QTreeWidget.__init__(self, parent)

        self.setItemsExpandable(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        #self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setAlternatingRowColors(True)
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

    def mouseReleaseEvent(self, event):
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
        drag = QtGui.QDrag(self)
        drag.setMimeData(self.mimeData)
        drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)

    def searchChildren(self, parent):
        for child in parent.children():
                #print child
                if child:
                    if isinstance(child, QtGui.QTextFrame):
                        #print child.childFrames()
                        pass
                    self.searchChildren(child)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        print event.mimeData().text()
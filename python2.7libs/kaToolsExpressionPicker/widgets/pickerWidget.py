import hou
import toolutils
from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import addExpression, stylesheet, vexSyntaxHighlighter
from kaToolsExpressionPicker.widgets import expressionTreeWidget, snippet, saveDialog, snippetDialog

reload(addExpression)
reload(stylesheet)
reload(expressionTreeWidget)
reload(snippet)
reload(saveDialog)
reload(snippetDialog)

class editFlags:
    __edit = 0
    __clear = 1
    __current = 0
    def __init__(self, init = 0):
        self.setFlag(init)
        pass

    def flag(self):
        return self.__current

    def setFlag(self, val):
        self.__current = val

    def edit(self):
        return self.__edit

    def clear(self):
        return self.__clear


class pickerWidget1(QtWidgets.QFrame):
    def __init__(self, parent = None):
        super(pickerWidget, self).__init__(parent)


        layout = QtWidgets.QVBoxLayout()

        view = QtWidgets.QTreeView()
        view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(['col1', 'col2', 'col3'])
        view.setModel(model)
        #view.setUniformRowHeights(True)

        for i in range(3):
            parent1 = QtGui.QStandardItem('Family {}. Some long status text for sp'.format(i))
            for j in range(3):
                child1 = QtGui.QStandardItem('Child {}'.format(i*3+j))
                child2 = QtGui.QStandardItem('row: {}, col: {}'.format(i, j+1))
                child3 = QtGui.QStandardItem('row: {}, col: {}'.format(i, j+2))
                parent1.appendRow([child1, child2, child3])
            model.appendRow(parent1)
            # span container columns
            view.setFirstColumnSpanned(i, view.rootIndex(), True)

        layout.addWidget(view)
        self.setLayout(layout)



class pickerWidget(QtWidgets.QFrame):

    prevClicked = QtWidgets.QTreeWidgetItem()
    flag = editFlags()
    
    
    def __init__(self, parent = None):
        #super(pickerWidget, self).__init__(parent)
        QtWidgets.QFrame.__init__(self, parent)
        
        self.draggedItem = None

        layout = QtWidgets.QVBoxLayout()
        #layout.setContentsMargins(0,0,0,0)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        ### set up buttons
        buttonLayout = QtWidgets.QHBoxLayout()
        self.refreshButton = QtWidgets.QPushButton("Refresh")
        self.sortButton = QtWidgets.QPushButton("Sort")
        self.saveButton = QtWidgets.QPushButton("Save")
        self.deleteButton = QtWidgets.QPushButton("Delete")
        buttonLayout.addWidget(self.refreshButton)
        buttonLayout.addWidget(self.sortButton)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.deleteButton)
        self.refreshButton.clicked.connect(self.onRefreshClicked)
        self.refreshButton.clicked.connect(self.onSortClicked)
        self.saveButton.clicked.connect(self.onSaveClicked)
        self.deleteButton.clicked.connect(self.onDeleteClicked)

    
        ### set up tree widget
        self.treeWidget = expressionTreeWidget.expressionTreeWidget()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget.setColumnWidth(0, 150)
        self.treeWidget.setColumnWidth(1, 800)
        self.treeWidget.setAutoScroll(False)
        self.treeWidget.setHeaderLabels(["Name", "Expression"])

        self.treeWidget.itemClicked.connect(self.onItemClicked)
        self.treeWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        

        searchLayout = QtWidgets.QHBoxLayout()
        self.staticSearchText = QtWidgets.QLabel()
        self.staticSearchText.setText("Filter : ")
        self.searchTextArea = QtWidgets.QLineEdit()
        self.clearFilterButton = QtWidgets.QPushButton("Clear")
        self.searchTextArea.textEdited.connect(self.onSearchTextEdited)
        self.searchTextArea.editingFinished.connect(self.onEditFinished)
        self.clearFilterButton.clicked.connect(self.onClearFilterClicked)
        searchLayout.addWidget(self.staticSearchText)
        searchLayout.addWidget(self.searchTextArea)
        searchLayout.addWidget(self.clearFilterButton)

        labelLayout = QtWidgets.QHBoxLayout()
        self.pathLabel = QtWidgets.QLabel()
        self.pathLabel.setStyleSheet(stylesheet.styles["initial"])
        self.pathLabel.setText("Drop parameter above:")
        #self.pathLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum))

        self.clearButton = QtWidgets.QPushButton("Clear")
        self.clearButton.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        labelLayout.addWidget(self.pathLabel)
        #labelLayout.addStretch(0)
        labelLayout.addWidget(self.clearButton)
        self.clearButton.clicked.connect(self.onClearClicked)

        self.textArea = snippet.snippet(pathLabel = self.pathLabel)
        cursor = self.textArea.textCursor()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textArea.setCurrentFont(font)
        
        
        layout.addLayout(buttonLayout)
        layout.addLayout(searchLayout)
        layout.addWidget(self.splitter)
        self.splitter.addWidget(self.treeWidget)
        self.splitter.addWidget(self.textArea)
        layout.addLayout(labelLayout)
        self.setLayout(layout)
        self.splitter.setSizes([250,100])

        self.preset = addExpression.presetXML()
        
        self.updateTree()
        self.setStyleSheet(hou.qt.styleSheet())




    def closeEvent(self, event):
        if hou.parm(self.pathLabel.text()) !=None:
            self.textArea.removeCallBack(hou.parm(self.pathLabel.text()).node())
        super(pickerWidget,self).closeEvent(event)




    def onItemDoubleClicked(self, item, column):
        #self.treeWidget.editItem(item, column)
        newName = item.text(0)
        newExp = item.text(1)
        snippetDia = snippetDialog.snippetDialog(parent = self, text=item.text(column))
        result = snippetDia.exec_()
        if result == QtWidgets.QDialog.Accepted:
            if column == 0:
                newName = snippetDia.getNewText()
            elif column == 1:
                newExp = snippetDia.getNewText()
            categoryList = self.getParentItems(item)
            #print categoryList
            self.preset = addExpression.presetXML()
            self.preset.updateExpression(categoryList, item.text(0), newName, newExp)

            self.onRefreshClicked()

        

    def onItemClicked(self, item, column):
        '''
        if item.isSelected() == True:
            if self.prevClicked is item:
                selectecNodes = hou.selectedNodes()
                selectecNode = None
                if len(selectecNodes) == 0:
                    return
                selectecNode = selectecNodes[0]
                if selectecNode.type() == hou.sopNodeTypeCategory().nodeTypes()["attribwrangle"]:
                    self.draggedItem = item.text(1)
                    parmText = selectecNode.parm("snippet").eval()
                    selectecNode.parm("snippet").set(parmText + self.draggedItem)
            self.prevClicked = item
        '''
        if item.childCount()>0:
            if item.isExpanded() == False:
                item.setExpanded(True)
            else:
                item.setExpanded(False)


    def onRefreshClicked(self):
        self.preset = addExpression.presetXML()
        #menus = self.importXmlMenus()
        #menus, categories = self.importExpressions(menus)
        self.updateTree()

    def onSortClicked(self):
        self.preset.sortXML()
        self.onRefreshClicked()


    def onSaveClicked(self):
        savedia = saveDialog.saveDialog()
        result = savedia.exec_()
        if result == QtWidgets.QDialog.Accepted:
            category, name = savedia.getCatandName()
            self.preset = addExpression.presetXML()
            self.preset.saveXML(category, name, self.textArea.toPlainText())
            self.onRefreshClicked()
        


    def onDeleteClicked(self):
        items = self.treeWidget.selectedItems()
        if len(items)>0:
            for item in items:
                categoryList = self.getParentItems(item)
                name = item.text(0)
                self.preset.deleteExpression(categoryList, name)
            self.onRefreshClicked()


    def getParentItems(self, item):
        if isinstance(item, QtWidgets.QTreeWidgetItem):
            parentItem = item.parent()
            if isinstance(parentItem, QtWidgets.QTreeWidgetItem):
                categoryList = self.getParentItems(parentItem)
                categoryList.append(parentItem.text(0))
                return categoryList
            else:
                return []
        else:
            return []





    def onSearchTextEdited(self, text):
        allItems = self.treeWidget.findItems("", QtCore.Qt.MatchStartsWith | QtCore.Qt.MatchRecursive)
        for item in allItems:
            item.setHidden(False)
        if text != "":
            for i in range(self.treeWidget.topLevelItemCount()):
                child = self.treeWidget.topLevelItem(i)
                if text in child.text(0):
                    pass
                else:
                    self.setVisiblity(text, child)



    def setVisiblity(self, text, rootItem):
        if text in rootItem.text(0):
            return 1
        else:
            count = rootItem.childCount()
            found = 0
            if count > 0:
                for i in range(count):
                    found += self.setVisiblity(text, rootItem.child(i))
                if found>0:
                    #rootItem.setHidden(True)
                    return 1
                else:
                    rootItem.setHidden(True)
                    return 0
            else:
                rootItem.setHidden(True)
                return 0
                


    def onEditFinished(self):
        self.treeWidget.setFocus()


    def onClearFilterClicked(self):
        self.searchTextArea.setText("")
        self.onSearchTextEdited("")


    def onClearClicked(self):
        self.pathLabel.setText("Cleared.")
        self.flag.setFlag(self.flag.clear())
        self.textArea.setText("")
        self.pathLabel.setStyleSheet(stylesheet.styles["initial"])




    def rrrr(self):
        print "resize"
        
        allItems = self.treeWidget.findItems("", QtCore.Qt.MatchStartsWith | QtCore.Qt.MatchRecursive)
        for item in allItems:
            count = item.childCount()
            if count==0:
                print item.expArea.toPlainText()
                print item.expArea.viewport().size()
                item.setSizeHint(1, item.expArea.document().size().toSize()*1.1)
                item.expArea.setFixedHeight(item.expArea.document().size().height())

        pass

    

############################################################



    def clear(self):
        '''
        length = self.treeWidget.topLevelItemCount()
        if length > 0:
            for i in range(0, length):
                #print i
                self.clearItems(self.treeWidget.topLevelItem(0))
                self.treeWidget.takeTopLevelItem(0)
        '''
        self.treeWidget.clear()



    def clearItems(self, item):
        #print item
        length = item.childCount()
        if length > 0:
            for i in range(0, length):
                item.child(0)
                item.removeChild(item.child(0))
                parent.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled) #QtCore.Qt.ItemIsEditable | 


    def updateTree(self):
        while True:
            try:
                if self.treeWidget.itemPressed is not None:
                    self.treeWidget.itemPressed.disconnect()
            except Exception:
                #print Exception
                break
        while True:
            try:
                if self.treeWidget.itemDoubleClicked is not None:
                    self.treeWidget.itemDoubleClicked.disconnect()
            except Exception:
                #print Exception
                break
        while True:
            try:
                if self.treeWidget.itemClicked is not None:
                    self.treeWidget.itemClicked.disconnect()
            except Exception:
                #print Exception
                break
        
        self.clear()

        font = None
        for expression in self.preset.expressions:
            categories = self.preset.getParents(expression)
            #print expression.name, categories
            parent = self.treeWidget
            for i, categoryName in enumerate(categories):
                items = []
                if isinstance(parent, expressionTreeWidget.expressionTreeWidget):
                    items = parent.findItems(categoryName, 0)
                    #print "parent is tree"
                elif isinstance(parent, QtWidgets.QTreeWidgetItem):
                    #print "parent is item" , parent.text(0)
                    for i in range(parent.childCount()):
                        if parent.child(i).text(0) == categoryName:
                            items.append(parent.child(i))
                if len(items) == 0:
                    parent = QtWidgets.QTreeWidgetItem(parent)
                    parent.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled) #QtCore.Qt.ItemIsEditable | 
                    parent.setText(0, categoryName)
                    parent.setExpanded(False)

                    font = parent.font(0)
                    font.setPointSize(11)
                    font.setBold(True)
                    parent.setFont(0, font)
                else:
                    parent = items[0]
                    font = parent.font(0)

            #child = expTreeItem(parent)
            child = QtWidgets.QTreeWidgetItem(parent)
            child.setText(0, expression.name)
            #child.expArea.setText(expression.expression)
            child.setText(1, expression.expression)
            child.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled) #QtCore.Qt.ItemIsEditable | 
            child.setToolTip(1, expression.expression)

            font.setPointSize(10)
            font.setBold(False)
            for column in range (child.columnCount()):
                child.setFont(column, font)


        #self.treeWidget.itemPressed.connect(self.onItemPressed)
        self.treeWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        pass






class expTreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent=None):
        super(expTreeItem, self).__init__(parent)
        
        self.expArea = QtWidgets.QTextBrowser()
        #self.expArea.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed , QtWidgets.QSizePolicy.Fixed ))
        #self.expArea.setMinimumHeight(10)
        vexSyntax = vexSyntaxHighlighter.vexSyntaxHighlighter(self.expArea.document())
        self.expArea.setReadOnly(True)
        #self.expArea.setEnabled(False)
        #self.expArea.setMouseTracking(False)
        self.expArea.setTextInteractionFlags(QtCore.Qt.NoTextInteraction )
        self.expArea.setStyleSheet(stylesheet.styles["templateAreaAlt"])

        self.expArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.treeWidget().setItemWidget(self, 1, self.expArea)
        self.setSizeHint(1, QtCore.QSize(10, 800))
        
        pass


    def text(self, column):
        return self.expArea.toPlainText()

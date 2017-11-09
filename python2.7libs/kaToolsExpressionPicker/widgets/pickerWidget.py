import hou
import toolutils
from PySide2 import QtWidgets, QtCore, QtGui

from kaToolsExpressionPicker import addExpression, stylesheet
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

class pickerWidget(QtWidgets.QFrame):

    prevClicked = QtWidgets.QTreeWidgetItem()
    flag = editFlags()
    currentSize = 12
    
    def __init__(self, parent = None):
        #super(pickerWidget, self).__init__(parent)
        QtWidgets.QFrame.__init__(self, parent)
        
        self.draggedItem = None

        layout = QtWidgets.QVBoxLayout()
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
        #self.treeWidget.setFocusPolicy(QtWidgets.Qt.WheelFocus)
        #self.treeWidget.itemPressed.connect(self.onItemPressed)
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        self.treeWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)

        searchLayout = QtWidgets.QHBoxLayout()
        self.staticSearchText = QtWidgets.QLabel()
        self.staticSearchText.setText("Filter : ")
        self.searchTextArea = QtWidgets.QLineEdit()
        self.searchTextArea.textEdited.connect(self.onSearchTextEdited)
        self.searchTextArea.editingFinished.connect(self.onEditFinished)
        searchLayout.addWidget(self.staticSearchText)
        searchLayout.addWidget(self.searchTextArea)

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
        self.textArea.textChanged.connect(self.onSnippetTextEdited)
        
        
        layout.addLayout(buttonLayout)
        layout.addLayout(searchLayout)
        layout.addWidget(self.splitter)
        self.splitter.addWidget(self.treeWidget)
        self.splitter.addWidget(self.textArea)
        layout.addLayout(labelLayout)
        self.setLayout(layout)

        #print self.splitter.size()
        self.splitter.setSizes([250,100])

        self.preset = addExpression.presetXML()
        #menus = self.importXmlMenus()
        #menus, categories = self.importExpressions(menus)
        #self.updateTree(menus, categories)
        self.updateTree()




    def onItemDoubleClicked(self, item, column):
        #self.treeWidget.editItem(item, column)
        snippetDia = snippetDialog.snippetDialog()
        result = snippetDia.exec_()
        if result == QtWidgets.QDialog.Accepted:
            pass

        

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




    def onSnippetTextEdited(self):
        text = self.textArea.toPlainText()
        if "\t" in text:
            text = text.replace("\t", "    ")
            self.textArea.setText(text)
            cursor = self.textArea.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            self.textArea.setTextCursor(cursor)
        if self.flag.flag() == self.flag.edit():
            parm = hou.parm(self.pathLabel.text())
            if parm != None:
                parm.set(text)
                self.pathLabel.setStyleSheet(stylesheet.styles["valid"])
            else:
                self.pathLabel.setText("Invalid. Drop a parameter above:")
                self.pathLabel.setStyleSheet(stylesheet.styles["invalid"])
        elif self.flag.flag() == self.flag.clear():
            pass
        if text == "":
            #cursor = self.textArea.textCursor()
            #self.textArea.selectAll()
            #self.textArea.setFontPointSize(self.currentSize)
            #self.textArea.setTextCursor(cursor)
            font = QtGui.QFont()
            font.setPointSize(self.currentSize)
            self.textArea.setCurrentFont(font)
        else:
            self.currentSize = self.textArea.fontPointSize()
        

        self.flag = editFlags()



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


    def onClearClicked(self):
        self.pathLabel.setText("Cleared.")
        self.flag.setFlag(self.flag.clear())
        self.textArea.setText("")
        self.pathLabel.setStyleSheet(stylesheet.styles["initial"])


    

############################################################


    def importXmlMenus(self):
        # Read Presets
        menus = self.preset.makeMenus()
        return menus


    def importExpressions(self, menus):
        num = len(menus)/2
        categories = []
        for i in range(0, num):
            menus[i*2+1] = self.preset.exportExpression({"selectedlabel" : menus[i*2]})
            categories.append(self.preset.exportCategory({"selectedlabel" : menus[i*2]}))
        return menus, categories


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
                parent.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)


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
                    parent.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)
                    parent.setText(0, categoryName)
                    parent.setExpanded(False)

                    font = parent.font(0)
                    font.setPointSize(11)
                    font.setBold(True)
                    parent.setFont(0, font)
                else:
                    parent = items[0]
                    font = parent.font(0)

            child = QtWidgets.QTreeWidgetItem(parent)
            child.setText(0, expression.name)
            child.setText(1, expression.expression)
            child.setFlags(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)
            child.setToolTip(1, expression.expression)
            #print child.sizeHint(1).width(), child.sizeHint(1).height()
            font.setPointSize(10)
            font.setBold(False)
            for column in range (child.columnCount()):
                child.setFont(column, font)



        #self.treeWidget.itemPressed.connect(self.onItemPressed)
        self.treeWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.treeWidget.itemClicked.connect(self.onItemClicked)
        pass



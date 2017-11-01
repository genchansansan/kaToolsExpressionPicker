# -*- coding: utf-8 -*-
import hou
#import xml.etree.ElementTree as ET
import sys
#import xml.parsers.expat as ep
import lxml.etree as let
import re
import os

class categoryData:
	parent = None
	name = ''
	myselfData = None
	parentData = None
	def __init__(self, parent = None, myself = None):
		self.myselfData = myself
		self.parentData = parent
		if parent != None :
			if "name" in parent.keys():
				self.parent = parent.attrib[("name")]
		if myself != None:
			self.name = myself.attrib[("name")]

class expressionData(categoryData):
	expression=''
	categories = []
	def __init__(self, parent = None, myself = None):
		self.myselfData = myself
		self.parentData = parent
		if parent != None:
			self.parent = parent.attrib[("name")]
		if myself != None:
			self.name = myself.attrib[("name")]
			self.expression = myself.text



class presetXML:

	parser = ""
	menus = []
	inSet=False
	inExp=False
	expression=''
	XMLPath=''
	tree2 = let.ElementTree()
	kwargs = None
	expressions = []
	categories = []


	def __init__(self, kwargs=None):
		#scriptPath = os.path.split(os.path.split(os.path.split(__file__)[0])[0])
		scriptPath = ""
		for path in os.sys.path:
			scriptPath = os.path.split(path)[0] + '/expressions1.xml'
			if os.path.exists(scriptPath):
				#print scriptPath
				break
		self.XMLPath = scriptPath
		parser = let.XMLParser(resolve_entities=False, remove_blank_text=True, strip_cdata=False)
		self.tree2 = let.parse(self.XMLPath, parser)
		self.kwargs = kwargs
		self.readAll()



###########################################################################

	def findCategory(self, root):
		categories = list(root)
		for child in categories:
			if child.tag == "category":
				category = categoryData(root, child)
				self.categories.append(category)
				#print category
				self.findCategory(child)
			elif child.tag == "expression":
				expression = expressionData(root, child)
				self.expressions.append(expression)




	def getParents(self, data):
		parentName = data.parentData
		#print parentName
		if parentName != None:
			for category in self.categories:
				if category.myselfData == parentName:
					categoryList = self.getParents(category)
					categoryList.append(parentName.attrib[("name")])
					return categoryList
			#print "done2"
			return []
		else:
			#print "done"
			return []


	def readAll(self):
		root = self.tree2.getroot()
		self.expressions = []
		self.categories = []
		self.findCategory(root)
		#print [e.name for e in self.categories]
		#print [e.parent for e in self.categories]
		#print [self.getParents(e) for e in self.expressions]
		#print [e.name for e in self.expressions]
		pass

	def saveXML(self, saveCategory, saveName, exp):
		root = self.tree2.getroot()

		#accept, names = hou.ui.readMultiInput("Preset Name:\n(Use \"/\" for sub categories)", ["Category:", "Name:"], buttons=('OK','Cancel') , close_choice=1)
		#if accept == 1:
		#	return
		#categories = names[0].split("/")
		#name = names[1]

		categories = saveCategory.split("/")
		name = saveName

		expression = exp
		expression = let.CDATA(expression)

		expressionElement = let.Element("expression")
		expressionElement.set("name", name)
		expressionElement.text = expression

		parent = root
		rootPath = "."
		for i in range(len(categories)):
			rootPath = rootPath + "/category"
			foundCategories = parent.findall(rootPath + "[@name='" + categories[i] + "']")
			#print rootPath
			if len(foundCategories) >0:
				parent = foundCategories[0]
				#print "found", parent.attrib[("name")]
			else:
				categoryElement = let.Element("category")
				categoryElement.set("name", categories[i])
				parent.append(categoryElement)
				parent = categoryElement
				#print "not found", parent.attrib[("name")]
		parent.append(expressionElement)

		self.tree2.write(self.XMLPath, encoding="utf-8", method="xml", pretty_print = True)


	def findWhereToAdd(self, element):
		if element.tag != "expression":
			exsistingCategories = list(element)
			pass


	def exportExpression(self, kwargs):
		expression = self.getExpression(kwargs)
		return expression

	def exportCategory(self, kwargs):
		category = self.getCategory(kwargs)
		return category

	def paste(self, kwargs):
		expression = self.getExpression(kwargs)
		kwargs["parms"][0].set(kwargs["parms"][0].eval() + expression)


	def getExpression(self, kwargs):
		root = self.tree2.getroot()
		expression = root.find("./set[@name='" + kwargs["selectedlabel"] +"']").find('expression').text
		return expression

	def getCategory(self, kwargs):
		root = self.tree2.getroot()
		category = ""
		try:
			category = root.find("./set[@name='" + kwargs["selectedlabel"] +"']").attrib[("category")]
			#print category
		except KeyError:
			#print "no category"
			category = "no category"
		return category


	def makeMenus(self):
		root = self.tree2.getroot()
		self.menus = []
		for menuset in root:
			if menuset.tag == "set":
				self.menus.append(menuset.attrib[("name")])
				self.menus.append(menuset.attrib[("name")])
		return self.menus

		

	def saveXMLDEL(self,kwargs):
		root = self.tree2.getroot()

		#accept, name = hou.ui.readInput("Preset Name:", buttons=('OK','Cancel'), close_choice=1)
		accept, names = hou.ui.readMultiInput("Preset Name:", ["Category:", "Name:"], buttons=('OK','Cancel'), default_choice=0, close_choice=1)
		if accept == 1:
			return
		category = names[0]
		name = names[1]

		expression = kwargs["parms"][0].eval()
		expression = let.CDATA(expression)

		setElement = let.Element("set")
		setElement.set("name", name)
		setElement.set("category", category)
		expressionElement = let.Element("expression")
		expressionElement.text = expression
		root.append(setElement)
		setElement.append(expressionElement)

		self.tree2.write(self.XMLPath, encoding="utf-8", method="xml", pretty_print = True)



	def deleteExpression(self, categoryList, name):
		root = self.tree2.getroot()
		length = len(name)
		if length==0:
			return
		element = self.getElement(categoryList, name)
		parent = None
		if element != None:
			for data in self.expressions:
				if data.myselfData == element:
					parent = data.parentData
					break
			if parent != None:
				parent.remove(element)
				self.updateXMLFile()
		


	def getElement(self, categoryList, name):
		root = self.tree2.getroot()
		element = None
		rootPath = "."
		for i in range(len(categoryList)):
			rootPath = rootPath + "/category"
			rootPath = rootPath + "[@name='" + categoryList[i] + "']"
		rootPath = rootPath + "/expression[@name='" +  name + "']"
		#print rootPath
		foundCategories = root.findall(rootPath)
		if len(foundCategories) >0:
				element = foundCategories[0]
		return element

	def updateXMLFile(self):
		self.tree2.write(self.XMLPath, encoding="utf-8", method="xml", pretty_print = True)


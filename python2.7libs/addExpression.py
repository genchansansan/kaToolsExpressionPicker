# -*- coding: utf-8 -*-
import hou
#import xml.etree.ElementTree as ET
import sys
#import xml.parsers.expat as ep
import lxml.etree as let
import re
import os


class wranglePreset:

	parser = ""
	menus = []
	inSet=False
	inExp=False
	expression=''

	def __init__(self, kwargs=None):
		
		scriptPath = os.path.split(os.path.split(__file__)[0])
		#print hou.expandString("$HOUDINI_PATH").split(os.pathsep)
		#self.XMLPath = re.split("[;:]", hou.expandString("$HOUDINI_PATH"))[-2] + '/expressions.xml'
		self.XMLPath = scriptPath[0] + '/expressions.xml'
		parser = let.XMLParser(resolve_entities=False, remove_blank_text=True, strip_cdata=False)
		self.tree2 = let.parse(self.XMLPath, parser)
		self.kwargs = kwargs



###########################################################################


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

	def getElement(self, name):
		root = self.tree2.getroot()
		element = None
		try:
			element = root.find("./set[@name='" + name +"']")
		except KeyError:
			element = None
		return element



	def makeMenus(self):
		root = self.tree2.getroot()
		self.menus = []
		for menuset in root:
			if menuset.tag == "set":
				self.menus.append(menuset.attrib[("name")])
				self.menus.append(menuset.attrib[("name")])
		return self.menus


	def findCategories(self, root):
		categories = root.find("./categories")
		if categories is None:
			return categories
		else:
			element = let.Element("categories")
			return element



	def findCategory(self, categories, category):
		categories = root.find("./categories")
		for category in categories:
			return

		

	def saveXML(self,kwargs):
		root = self.tree2.getroot()

		#accept, name = hou.ui.readInput("Preset Name:", buttons=('OK','Cancel'), close_choice=1)
		accept, names = hou.ui.readMultiInput("Preset Name:", ["Category:", "Name:"], buttons=('OK','Cancel') , close_choice=1)
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



	def deleteExpression(self, name):
		root = self.tree2.getroot()
		length = len(name)
		if length==0:
			return
		element = self.getElement(name)
		if element != None:
			root.remove(element)
			self.updateXMLFile()

	def updateXMLFile(self):
		self.tree2.write(self.XMLPath, encoding="utf-8", method="xml", pretty_print = True)

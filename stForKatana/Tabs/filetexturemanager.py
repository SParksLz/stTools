from Katana import QtGui, QtCore
from Katana import Qt
from Katana import Nodes3DAPI, Utils, NodegraphAPI
# from Katana import 
from UI4.Widgets.SceneGraphView.ColumnDataType import ColumnDataType
from UI4.Tabs import BaseTab
import UI4.App.Layouts
import UI4.Widgets
from UI4.Widgets.SceneGraphView import SceneGraphViewIconManager

import sys
import os
import re

class FileTextureManager(BaseTab):
	def __init__(self, parent=None):
		UI4.Tabs.BaseTab.__init__(self, parent)
		#button
		self.__sceneFileManager = QtGui.QPushButton(self)
		self.__setpath = QtGui.QPushButton(self)
		self.__reset = QtGui.QPushButton(self)
		self.__browser = QtGui.QPushButton(self)

		self.__setpath.setText('Set Path')
		self.__sceneFileManager.setText('Detect file texture path')
		self.__reset.setText('Reset')
		self.__browser.setText('Browser')
		#tree widget
		self.__Tree = QtGui.QTreeWidget(self)
		self.__label = QtGui.QLabel(self)
		self.__label.setText('Target Directory')
		self.__pathedit = QtGui.QLineEdit(self)


		self.__midlegroup = QtGui.QGroupBox(self)
		self.__undergroup = QtGui.QGroupBox(self)
		self.__undergroup.setLayout(QtGui.QHBoxLayout())
		self.__midlegroup.setLayout(QtGui.QHBoxLayout())


		self.__undergroup.layout().addWidget(self.__setpath)
		self.__undergroup.layout().addWidget(self.__reset)
		self.__midlegroup.layout().addWidget(self.__label)
		self.__midlegroup.layout().addWidget(self.__pathedit)
		self.__midlegroup.layout().addWidget(self.__browser)



		all_paths = get_all_imagepath()
		all_dir = imagepath_to_directory(all_paths)
		dir_type = classiffy(all_dir)




		vBoxlayout = QtGui.QVBoxLayout()		
		vBoxlayout.addWidget(self.__sceneFileManager)
		vBoxlayout.addWidget(self.__Tree)
		vBoxlayout.addWidget(self.__midlegroup)
		vBoxlayout.addWidget(self.__undergroup)
		# vBoxlayout.addStretch()
		self.setLayout(vBoxlayout)
		# self.__itermlist = None

		# print xxx
		self.__sceneFileManager.clicked.connect(self.show_treeview)
		self.__setpath.clicked.connect(self.modify_path)
		self.__reset.clicked.connect(self.reset_treeview)
		self.__browser.clicked.connect(self.browser)
		# print self.__itermlist

	def reset_treeview(self):
		self.__Tree.clear()	
	def show_treeview(self):
		self.__Tree.clear()
		all_paths = get_all_imagepath()
		all_dir = imagepath_to_directory(all_paths)
		dir_type = classiffy(all_dir)
		all_childiterm = []

		for i in dir_type:
			# print i
			parent = QtGui.QTreeWidgetItem(self.__Tree)
			parent.setText(0,i)
			parent.setFlags(parent.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
			parent.setCheckState(0, QtCore.Qt.Unchecked)
			for path in all_paths:
				# print path
				if '/'.join(path.split('/')[:-1]) == i:
					child = QtGui.QTreeWidgetItem(parent)
					child.setText(0, '/'+path.split('/')[-1])
					child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
					child.setCheckState(0, QtCore.Qt.Unchecked)
					all_childiterm.append(child)
					# if child.data(0, QtCore.Qt.CheckStateRole) == QtCore.Qt.Unchecked:
					# 	print 'false'
		# print all_childiterm
		return all_childiterm


	def get_all_child(self):
		num = self.__Tree.topLevelItemCount()
		all_items = []
		for i in range(num):
			current_parent = self.__Tree.topLevelItem(i)
			for x in range(current_parent.childCount()):
				all_items.append(current_parent.child(x))
		return all_items

	def get_checked_children(self, list):
		checked_child = []
		for i in list:
			if i.data(0, QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked:
				checked_child.append(i)
		return checked_child

	def check_tree(self):
		pathlist = []
		listx = self.get_all_child()
		checked_list = self.get_checked_children(listx)
		for i in checked_list:
			path = i.parent().text(0)+i.text(0)
			pathlist.append(path)
		return pathlist

	def browser(self):
		self.__filebrowser = QtGui.QFileDialog()
		directory = self.__filebrowser.getExistingDirectory()
		self.__pathedit.setText('%s'%(str(directory)))
	def modify_path(self):
		listy = self.get_all_child()
		listv = self.get_checked_children(listy)
		all_asn_node = NodegraphAPI.GetAllNodesByType('ArnoldShadingNode')
		# print all_asn_node
		for node in all_asn_node:
			if node.getParameter('parameters.filename.value'):
				for x in listv:
					old_dir = x.parent().text(0)
					path = x.parent().text(0)+x.text(0)
					if node.getParameter('parameters.filename.value').getValue(0) == path:
						new_path = self.__pathedit.displayText()+x.text(0)
						print new_path
						node.getParameter('parameters.filename.value').setValue(str(new_path), 0)



def get_all_imagepath():
	all_asn_node = NodegraphAPI.GetAllNodesByType('ArnoldShadingNode')
	all_material_node = NodegraphAPI.GetAllNodesByType('Material')
	all_asn_texture_path = [i.getParameter('parameters.filename.value').getValue(0) for i in all_asn_node
			if i.getParameter('nodeType').getValue(0) == 'image']
	all_texture_path = all_asn_texture_path
	for mat in all_material_node:
		if mat.getParameter('shaders.arnoldSurfaceShader.value') is not None :
			if mat.getParameter('shaders.arnoldSurfaceShader.value').getValue(0) is not None and mat.getParameter('shaders.arnoldSurfaceShader.value').getValue(0)=='image' :
				all_texture_path.append(mat.getParameter('shaders.arnoldSurfaceParams.filename.value').getValue(0))
	return all_texture_path

def imagepath_to_directory(path_list):
	all_directory = ['/'.join(path.split('/')[:-1]) for path in path_list]
	return all_directory

def classiffy(dir_path):
	directory = []
	[directory.append(i) for i in dir_path if not i in directory]
	return directory





PluginRegistry = [("KatanaPanel", 2.0, "X/File Texture Manager",
					FileTextureManager)]
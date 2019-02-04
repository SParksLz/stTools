# -*- coding: utf-8 -*-
# @Author: liuzhen
# @Date:   2018-07-27 11:01:41
# @Last Modified by:   liuzhen
# @Last Modified time: 2018-07-27 11:12:44

from Katana import QtCore, QtGui, UI4, QT4Widgets, QT4FormWidgets
from Katana import NodegraphAPI, Utils
from Katana import UniqueName, FormMaster
import os
import ScriptActions as SA
import logging
log = logging.getLogger('Solver_XEditor')


class Solver_XEditor(QtGui.QWidget):

	def __init__(self, parent, node):

	 	QtGui.QWidget.__init__(self, parent)
	 	self.__node = node
	 	nodename = node.getName()
	 	#Path parameter
	 	pathparameter = self.__node.getParameter('Path')
	 	pathpolicy = UI4.FormMaster.CreateParameterPolicy(None, pathparameter)
	 	factory = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory
	 	w = factory.buildWidget(self, pathpolicy)
	 	lo = '0'
	 	hi = '1'
	 	#SOLVER button group..
	 	#Variables..
	 	self.__varsolver = QtGui.QPushButton(self)
	 	self.__varsolver.setText('Var_Solver')
	 	#XML..
	 	self.__xmlsolver = QtGui.QPushButton(self)
	 	self.__xmlsolver.setText('XML_Solver')
	 	#ASS..
	 	self.__ASSsolver = QtGui.QPushButton(self)
	 	self.__ASSsolver.setText('ASS_Solver')
	 	#Camera..
	 	self.__camsolver = QtGui.QPushButton(self)
	 	self.__camsolver.setText('CAM_Solver')

	 	self.__buttongroup = QtGui.QGroupBox(self)
	 	self.__buttongroup.setLayout(QtGui.QVBoxLayout())
	 	self.__buttongroup.setTitle('Asset Solver')
	 	self.__buttongroup.layout().addWidget(self.__varsolver)
	 	self.__buttongroup.layout().addWidget(self.__xmlsolver)
	 	self.__buttongroup.layout().addWidget(self.__ASSsolver)
	 	self.__buttongroup.layout().addWidget(self.__camsolver)
	 	
	 	#lod button
	 	#hi button
	 	self.__hibutton = QtGui.QPushButton(self)
	 	self.__hibutton.setText('Mode_hi')
	 	#lo button
	 	self.__lobutton = QtGui.QPushButton(self)
	 	self.__lobutton.setText('Mode_lo')
	 	#plaintext
	 	self.__info = QtGui.QPlainTextEdit()
	 	self.__info.setFixedHeight(27.5)
	 	self.__info.setFixedWidth(120)
	 	self.__info.setReadOnly(True)
	 	#self.__info.setPlainText("xxxx")

	 	self.__lodbuttongroup = QtGui.QGroupBox(self)
	 	self.__lodbuttongroup.setLayout(QtGui.QHBoxLayout())
	 	self.__lodbuttongroup.setTitle('level-of-detail')
	 	self.__lodbuttongroup.layout().addStretch()
	 	self.__lodbuttongroup.layout().addWidget(self.__hibutton)
	 	self.__lodbuttongroup.layout().addWidget(self.__lobutton)
	 	self.__lodbuttongroup.layout().addWidget(self.__info)
	 	self.__lodbuttongroup.layout().addStretch()

	 	#main layout..
	 	mainlayout = QtGui.QVBoxLayout()
	 	mainlayout.addWidget(w)
	 	mainlayout.addWidget(self.__buttongroup)
	 	mainlayout.addWidget(self.__lodbuttongroup)

	 	self.setLayout(mainlayout)

	 	QtCore.QObject.connect(self.__varsolver, QtCore.SIGNAL('clicked()'), self.X_var_clicked)
	 	QtCore.QObject.connect(self.__xmlsolver, QtCore.SIGNAL('clicked()'), self.X_xml_clicked)
	 	QtCore.QObject.connect(self.__ASSsolver, QtCore.SIGNAL('clicked()'), self.X_ASS_clicked)
	 	QtCore.QObject.connect(self.__camsolver, QtCore.SIGNAL('clicked()'), self.X_cam_clicked)

	 	#hi/lo button
	 	QtCore.QObject.connect(self.__lobutton, QtCore.SIGNAL('clicked()'), self.X_lo_clicked)
	 	QtCore.QObject.connect(self.__hibutton, QtCore.SIGNAL('clicked()'), self.X_hi_clicked)

	def X_var_clicked(self):
		SA.X_varibleSolver(SA.X_listdir_num(self.__node.getParameter('Path').getValue(0)),
						   SA.X_listdir(self.__node.getParameter('Path').getValue(0)),
						   NodegraphAPI.GetRootNode())
	def X_xml_clicked(self):
		print '%s' % self.__node
		switchport = SA.X_getXml(self.__node.getParameter('Path').getValue(0),SA.X_getVar(NodegraphAPI.GetRootNode()),self.__node)
		mergein = SA.getmergenode(self.__node).addInputPort('XML_Asset')
		mergein.connect(switchport)
	def X_ASS_clicked(self):
		assout = SA.X_getAss(self.__node.getParameter('Path').getValue(0),SA.X_getVar(NodegraphAPI.GetRootNode()), parent,self.__node)
		mergein = SA.getmergenode(self.__node).addInputPort('Ass')
		mergein.connect(assout)
	def X_cam_clicked(self):
		camout = SA.X_getcam(self.__node.getParameter('Path').getValue(0),SA.X_getVar(NodegraphAPI.GetRootNode()),self.__node)
		mergein = SA.getmergenode(self.__node).addInputPort('camera')
		mergein.connect(camout)
	def X_lo_clicked(self):
		lo = "0"
		SA.changeSwitch(lo)
		self.__info.setPlainText("Mode:lo")
	def X_hi_clicked(self):
		hi = "1"
		SA.changeSwitch(hi)
		self.__info.setPlainText("Mode:hi")

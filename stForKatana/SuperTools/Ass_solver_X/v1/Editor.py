from Katana import QtCore, QtGui, UI4
from Katana import NodegraphAPI
from Katana import UniqueName, FormMaster
from Katana import DrawingModule

import os
import ScriptActions as SA
import logging

log = logging.getLogger('Ass_solver_XEditor')

class Ass_solver_XEditor(QtGui.QWidget):

	def __init__(self, parent, node):

		super(Ass_solver_XEditor, self).__init__()
		self.__node = node
		nodename = node.getName()

		self.__treelable = ['Name','Type']

		factory = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory
		#path parameter..
		Ass_path = self.__node.getParameter('assFile_path')
		asslocation_path = self.__node.getParameter('Ass_Location')
		# asslocation_path.setExpression("'/root/world/geo/ASS'", 0)
		# asslocation_path.setExpressionFlag(True)
		to_location = self.__node.getParameter('to_location')

		#setting parameter

		asspath_policy = UI4.FormMaster.CreateParameterPolicy(None, Ass_path)
		asspath_widget = factory.buildWidget(self, asspath_policy)

		asslocation_policy = UI4.FormMaster.CreateParameterPolicy(None, asslocation_path)
		asslocation_widget = factory.buildWidget(self, asslocation_policy)

		to_location_policy = UI4.FormMaster.CreateParameterPolicy(None, to_location)
		to_location_widget = factory.buildWidget(self, to_location_policy)
		#Button
		self.__solve = QtGui.QPushButton(self)
		self.__solve.setText('Solve')
		#ASS tree..
		self.__asstree = QtGui.QTreeWidget(self)
		self.__asstree.setHeaderLabels(self.__treelable)

		#Group
		self.__buttongroup = QtGui.QGroupBox(self)
		self.__buttongroup.setLayout(QtGui.QHBoxLayout())
		self.__buttongroup.layout().addWidget(self.__solve)
		self.__buttongroup.layout().addStretch()

		self.__locationgroup = QtGui.QGroupBox(self)
		self.__locationgroup.setLayout(QtGui.QHBoxLayout())
		self.__locationgroup.layout().addWidget(asslocation_widget)
		self.__locationgroup.layout().addWidget(to_location_widget)

		#Main layout..
		self.__mainlayout = QtGui.QVBoxLayout()

		#Group
		self.__mainlayout.addWidget(asspath_widget)
		self.__mainlayout.addWidget(self.__locationgroup)
		self.__mainlayout.addWidget(self.__buttongroup)
		self.__mainlayout.addWidget(self.__asstree)

		self.setLayout(self.__mainlayout)

		self.__solve.clicked.connect(self.button_clicked)

	def button_clicked(self):
		children = [x.getType() for x in self.__node.getChildren()]
		if 'Group' not in children:
			SA.Createnode(self.__node, self.__node.getParameter('assFile_path').getValue(0))
			grouplist = SA.getGroupnode(self.__node)
			print 'xxxxxxx'
			print grouplist
			for group in grouplist:
				A_iterm = QtGui.QTreeWidgetItem(self.__asstree)
				A_iterm.setText(0, '%s' %(group.getName()))
				A_iterm.setText(1, '%s' %(group.getType()))
				standinlist = SA.getStandinnode(group)
				print 'xxxxxxxx'
				print standinlist
				for standin in standinlist:
					B_iterm = QtGui.QTreeWidgetItem(A_iterm)
					B_iterm.setText(0, '%s' %(standin.getName()))
					B_iterm.setText(1, '%s' %(standin.getType()))

		DrawingModule.AutoPositionNodes(self.__node.getChildren())
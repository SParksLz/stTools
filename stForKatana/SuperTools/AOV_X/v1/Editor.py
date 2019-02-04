from Katana import QtCore, QtGui, UI4, QT4Widgets, QT4FormWidgets
from Katana import NodegraphAPI, Utils
from Katana import UniqueName, FormMaster
import os
import ScriptActions as SA
import logging
log = logging.getLogger('AOV_XEditor')


class AOV_XEditor(QtGui.QWidget):

	def __init__(self, parent, node):
		QtGui.QWidget.__init__(self, parent)
		self.__node = node
		nodename = node.getName()
		self._ps = '''AO_aov : ambient_occlution
Fresnel_aov : Fresnel
cryptoobject_aov : crypto_object
cryptomaterial_aov : crypto_material
motionvector_aov : motion_vector
				   '''

		factory = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory
		#set aovs to one path

		# satopparameter = self.__node.getParameter('Path')
		# satoppolicy = UI4.FormMaster.CreateParameterPolicy(None, satopparameter)
		# satopw = factory.buildWidget(self, satoppolicy)
		# self.__satop = QtGui.QPushButton(self)
		# self.__satop.setText('Set_all_AOVs_to_one_path')
		#beauty
		# self.__beauty = QtGui.QCheckBox(self)
		# self.__beauty.setText('Beauty')
		# beautyparameter = self.__node.getParameter('Beauty_path')
		# beautypolicy = UI4.FormMaster.CreateParameterPolicy(None, beautyparameter)
		# beautyw = factory.buildWidget(self, beautypolicy)
		#P N Z ao cn
		# self._deep_path = self.__node.getParameter('Deep_path')
		# self._deep_policy = UI4.FormMaster.CreateParameterPolicy(None, self._deep_path)
		# self._deepwidget = factory.buildWidget(self, self._deep_policy)

		self._deep = QtGui.QCheckBox(self)
		self._deep.setText('Use deep image')
		self._deep.setChecked(self.checkbox_init('deep'))

		self.__p = QtGui.QCheckBox(self)
		self.__p.setText('Position')
		self.__p.setChecked(self.checkbox_init('position'))

		self.__n = QtGui.QCheckBox(self)
		self.__n.setText('Normal')
		self.__n.setChecked(self.checkbox_init('normal'))

		self.__z = QtGui.QCheckBox(self)
		self.__z.setText('Depth')
		self.__z.setChecked(self.checkbox_init('depth'))

		self.__mv = QtGui.QCheckBox(self)
		self.__mv.setText('MotionVector')
		self.__mv.setChecked(self.checkbox_init('motionvector'))

		self.__ao = QtGui.QCheckBox(self)
		self.__ao.setText('Ambient_occlution')
		self.__ao.setChecked(self.checkbox_init('ambientocclution'))

		self.__cn = QtGui.QCheckBox(self)
		self.__cn.setText('Fresnel')
		self.__cn.setChecked(self.checkbox_init('Fresnel'))

		self._text = QtGui.QPlainTextEdit()
		self._text.setPlainText(self._ps)
		#P N Z output_path
		# Pparameter = self.__node.getParameter('Position_path')
		# Ppolicy = UI4.FormMaster.CreateParameterPolicy(None, Pparameter)
		# Pw = factory.buildWidget(self, Ppolicy)
		# Nparameter = self.__node.getParameter('Normal_path')
		# Npolicy = UI4.FormMaster.CreateParameterPolicy(None, Nparameter)
		# Nw = factory.buildWidget(self, Npolicy)
		# Zparameter = self.__node.getParameter('Depth_path')
		# Zpolicy = UI4.FormMaster.CreateParameterPolicy(None, Zparameter)
		# Zw = factory.buildWidget(self, Zpolicy)

		#ambient occlution
		# aoparameter = self.__node.getParameter('ambientocclution_path')
		# aopolicy = UI4.FormMaster.CreateParameterPolicy(None, aoparameter)
		# aow = factory.buildWidget(self, aopolicy)

		#CN
		# cnparameter = self.__node.getParameter('cn')
		# cnpolicy = UI4.FormMaster.CreateParameterPolicy(None, cnparameter)
		# cnw = factory.buildWidget(self, cnpolicy)

		#crypto_object
		self.__crypto_object = QtGui.QCheckBox(self)
		self.__crypto_object.setText('crypto_object')
		self.__crypto_object.setChecked(self.checkbox_init('cryptoobject'))
		# crypto_object_parameter = self.__node.getParameter('Crypto_Object_path')
		# crypto_object_policy = UI4.FormMaster.CreateParameterPolicy(None, crypto_object_parameter)
		# crypto_objectw = factory.buildWidget(self, crypto_object_policy)

		#crypto_material
		self.__crypto_material = QtGui.QCheckBox(self)
		self.__crypto_material.setText('crypto_material')
		self.__crypto_material.setChecked(self.checkbox_init('cryptomaterial'))

		self.__emission = QtGui.QCheckBox(self)
		self.__emission.setText('emission')
		self.__emission.setChecked(self.checkbox_init('emission'))
		# crypto_material_parameter = self.__node.getParameter('Crypto_Material_path')
		# crypto_material_policy = UI4.FormMaster.CreateParameterPolicy(None, crypto_material_parameter)
		# crypto_materialw = factory.buildWidget(self, crypto_material_policy)
		# #merge_output
		# # self.__mergenode = QtGui.QCheckBox(self)
		# # self.__mergenode.setText('merge_aov')
		# mergenode_parameter = self.__node.getParameter('aov_merge_path')
		# mergenode_policy = UI4.FormMaster.CreateParameterPolicy(None, mergenode_parameter)
		# mergenodew = factory.buildWidget(self, mergenode_policy)

		#utils
		self.__selectAll = QtGui.QCheckBox(self)
		self.__selectAll.setText('Select all')
		#group setup
		self.__utilsgroup = QtGui.QGroupBox(self)
		# self.__beautygroup = QtGui.QGroupBox(self)
		self.__pgroup = QtGui.QGroupBox(self)
		self.__ngroup = QtGui.QGroupBox(self)
		self.__zgroup = QtGui.QGroupBox(self)
		self.__mvgroup = QtGui.QGroupBox(self)
		self.__aogroup = QtGui.QGroupBox(self)
		self.__cngroup = QtGui.QGroupBox(self)

		self.__crypto_object_group = QtGui.QGroupBox(self)
		self.__crypto_material_group = QtGui.QGroupBox(self)
		self.__emission_group = QtGui.QGroupBox(self)

		# self.__mergegroup = QtGui.QGroupBox(self)

		#group layout
		self.__utilsgroup.setLayout(QtGui.QHBoxLayout())
		# self.__beautygroup.setLayout(QtGui.QHBoxLayout())
		self.__pgroup.setLayout(QtGui.QHBoxLayout())
		self.__ngroup.setLayout(QtGui.QHBoxLayout())
		self.__zgroup.setLayout(QtGui.QHBoxLayout())
		self.__mvgroup.setLayout(QtGui.QHBoxLayout())
		self.__aogroup.setLayout(QtGui.QHBoxLayout())
		self.__cngroup.setLayout(QtGui.QHBoxLayout())

		self.__crypto_object_group.setLayout(QtGui.QHBoxLayout())
		self.__crypto_material_group.setLayout(QtGui.QHBoxLayout())
		self.__emission_group.setLayout(QtGui.QHBoxLayout())

		# self.__mergegroup.setLayout(QtGui.QHBoxLayout())

		#add widget to group
		self.__utilsgroup.layout().addWidget(self.__selectAll)
		# self.__utilsgroup.layout().addWidget(self._deep)
		# self.__utilsgroup.layout().addWidget(self.__satop)
		# self.__utilsgroup.layout().addWidget(satopw)

		# self.__beautygroup.layout().addWidget(self.__beauty)
		# self.__beautygroup.layout().addStretch()
		# self.__beautygroup.layout().addWidget(beautyw)

		self.__pgroup.layout().addWidget(self.__p)
		self.__pgroup.layout().addStretch()
		# self.__pgroup.layout().addWidget(Pw)

		self.__ngroup.layout().addWidget(self.__n)
		self.__ngroup.layout().addStretch()
		# self.__ngroup.layout().addWidget(Nw)

		self.__zgroup.layout().addWidget(self.__z)
		self.__zgroup.layout().addStretch()
		# self.__zgroup.layout().addWidget(Zw)

		self.__mvgroup.layout().addWidget(self.__mv)
		self.__mvgroup.layout().addStretch()

		self.__aogroup.layout().addWidget(self.__ao)
		self.__aogroup.layout().addStretch()
		# self.__aogroup.layout().addWidget(aoparameter)

		self.__cngroup.layout().addWidget(self.__cn)
		self.__cngroup.layout().addStretch()
		# self.__cngroup.layout().addWidget(cnparameter)

		self.__crypto_object_group.layout().addWidget(self.__crypto_object)
		self.__crypto_object_group.layout().addStretch()
		# self.__crypto_object_group.layout().addWidget(crypto_objectw)

		self.__crypto_material_group.layout().addWidget(self.__crypto_material)
		self.__crypto_material_group.layout().addStretch()

		self.__emission_group.layout().addWidget(self.__emission)

		# self.__crypto_material_group.layout().addStretch()
		# self.__crypto_material_group.layout().addWidget(crypto_materialw)

		# self.__mergegroup.layout().addWidget(self.__mergenode)
		# self.__mergegroup.layout().addStretch()
		# self.__mergegroup.layout().addWidget(mergenodew)
		#mainlayout setting...
		self._checkgroup = QtGui.QGroupBox(self)
		self._checkgroup.setLayout(QtGui.QVBoxLayout())

		self._linegroup = QtGui.QGroupBox(self)
		self._linegroup.setLayout(QtGui.QVBoxLayout())

		self._ggroup = QtGui.QGroupBox(self)
		self._ggroup.setLayout(QtGui.QHBoxLayout())

		self._checkgroup.layout().addWidget(self.__utilsgroup)
		# mainlayout.addWidget(self.__beautygroup)
		self._checkgroup.layout().addWidget(self.__pgroup)
		self._checkgroup.layout().addWidget(self.__ngroup)
		self._checkgroup.layout().addWidget(self.__zgroup)
		self._checkgroup.layout().addWidget(self.__mvgroup)
		self._checkgroup.layout().addWidget(self.__aogroup)
		self._checkgroup.layout().addWidget(self.__cngroup)
		self._checkgroup.layout().addWidget(self.__crypto_object_group)
		self._checkgroup.layout().addWidget(self.__crypto_material_group)
		self._checkgroup.layout().addWidget(self.__emission_group)
		# self._checkgroup.layout().addStretch()

		self._ggroup.layout().addWidget(self._checkgroup)
		self._ggroup.layout().addWidget(self._linegroup)
		# self._linegroup.layout().addWidget(self._linegroup)
		self._deepgroup = QtGui.QGroupBox()
		self._deepgroup.setStyleSheet('QWidget{background-color:rgb(26,26,70)}')
		self._deepgroup.setLayout(QtGui.QHBoxLayout())
		self._deepgroup.layout().addWidget(self._deep)
		# self._deepgroup.layout().addWidget(self._deepwidget)

		self._linegroup.layout().addWidget(self._text)
		mainlayout = QtGui.QVBoxLayout()
		mainlayout.addWidget(self._ggroup)
		mainlayout.addWidget(self._deepgroup)
		mainlayout.addStretch()
		# mainlayout.addWidget(self.__mergegroup)

		self.setLayout(mainlayout)
		# self._deepwidget.hide()


		# QtCore.QObject.connect(self.__beauty,QtCore.SIGNAL("stateChanged(int)"),lambda v : self.stateChanged('Beauty',not bool(v)))
		QtCore.QObject.connect(self.__p,QtCore.SIGNAL("stateChanged(int)"),lambda v : self.stateChanged('position',not bool(v)))
		QtCore.QObject.connect(self.__n,QtCore.SIGNAL("stateChanged(int)"),lambda v : self.stateChanged('normal',not bool(v)))
		QtCore.QObject.connect(self.__z,QtCore.SIGNAL("stateChanged(int)"),lambda v : self.stateChanged('depth',not bool(v)))
		QtCore.QObject.connect(self.__ao,QtCore.SIGNAL("stateChanged(int)"),lambda v : self.stateChanged('ambientocclution',not bool(v)))
		QtCore.QObject.connect(self.__cn,QtCore.SIGNAL("stateChanged(int)"),lambda v : self.stateChanged('Fresnel',not bool(v)))
		QtCore.QObject.connect(self.__crypto_object,QtCore.SIGNAL("stateChanged(int)"),lambda v : self.stateChanged('cryptoobject',not bool(v)))
		QtCore.QObject.connect(self.__crypto_material,QtCore.SIGNAL("stateChanged(int)"),lambda v : self.stateChanged('cryptomaterial',not bool(v)))
		QtCore.QObject.connect(self.__emission,QtCore.SIGNAL("stateChanged(int)"),lambda v : self.stateChanged('emission',not bool(v)))

		self._deep.stateChanged.connect(self.passall)
		self.__mv.stateChanged.connect(lambda v : self.stateChanged('motionvector',not bool(v)))
		# self._deep.stateChanged.connect(self.print_x)
		# QtCore.QObject.connect(self.__satop,QtCore.SIGNAL('clicked()'), self.setPath)
		self.__selectAll.stateChanged.connect(lambda v: self.selectall(v))

	def selectall(self, v):
		# self.__beauty.setChecked(v)
		self.__p.setChecked(v)
		self.__n.setChecked(v)
		self.__z.setChecked(v)
		self.__mv.setChecked(v)
		self.__ao.setChecked(v)
		self.__cn.setChecked(v)
		self.__crypto_object.setChecked(v)
		self.__crypto_material.setChecked(v)
		self.__emission.setChecked(v)
		if v == 2 :
			self._deep.setChecked(0)


	def stateChanged(self,aov,v):
		list = SA.get_passed_nodelist(aov, self.__node)
		# print '````````````````````````'
		# print v
		# print list
		SA.set_node_passed(list,v)
		if v == False :
			self._deep.setChecked(0)
		# mergenode = SA.get_upnode(self.__node)
		# SA.set_mergeoutput(self.__node, mergenode)

	def setPath(self):
		xxx = self.__node.getParameter('Path').getValue(0)
		SA.set_aovs_to_onepath(self.__node, xxx)


	def print_x(self):
		if self._deep.checkState() == 0:
			self._deepwidget.hide()
		elif self._deep.checkState() == 2:
			pass
			# self._deepwidget.setVisible(True)
		# print self._deep.checkState()

	def passall(self):
		list = SA.get_passed_nodelist('deep', self.__node)
		if self._deep.checkState() == 2 :
			self.__selectAll.setChecked(0)
			self.__p.setChecked(0)
			self.__n.setChecked(0)
			self.__z.setChecked(0)
			self.__mv.setChecked(0)
			self.__ao.setChecked(0)
			self.__cn.setChecked(0)
			self.__crypto_object.setChecked(0)
			self.__crypto_material.setChecked(0)
			self.__emission.setChecked(0)
			SA.set_node_passed(list, False)
			# self._deepwidget.setVisible(True)
		if self._deep.checkState() == 0 :
			SA.set_node_passed(list, True)
			# self._deepwidget.hide()

	def checkbox_init(self, aov):
		state = 0
		list = SA.get_passed_nodelist(aov, self.__node)
		if list[0].isBypassed() == True:
			return state
		if list[0].isBypassed() == False:
			state = 2
			return state
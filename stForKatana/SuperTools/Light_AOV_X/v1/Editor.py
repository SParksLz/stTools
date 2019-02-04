from Katana import QtCore, QtGui, UI4, QT4Widgets, QT4FormWidgets
from Katana import NodegraphAPI, Utils
from Katana import UniqueName, FormMaster
import ScriptActions as SA
import logging
log = logging.getLogger('Light_AOV_XEditor')

class Light_AOV_XEditor(QtGui.QWidget):
	def __init__(self, parent, node):
		QtGui.QWidget.__init__(self, parent)
		self.__node = node
		nodename = node.getName()
		factory = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory


		light_aov_parameter = self.__node.getParameter('Light_AOV_Name')
		light_aov_parameterpolicy = UI4.FormMaster.CreateParameterPolicy(None, light_aov_parameter)
		light_aov_parameterw = factory.buildWidget(self, light_aov_parameterpolicy)

		self._direct = QtGui.QCheckBox(self)
		self._direct.setText('Direct')
		self._direct.setCheckState(self.checkbox_init('Direct'))
		self._direct.stateChanged.connect(lambda v : SA.set_node_passed(SA.get_passed_nodelist('Direct', self.__node), not bool(v)))

		self._indirect = QtGui.QCheckBox(self)
		self._indirect.setText('Indirect')
		self._indirect.setCheckState(self.checkbox_init('Indirect'))
		self._indirect.stateChanged.connect(lambda v : SA.set_node_passed(SA.get_passed_nodelist('Indirect', self.__node), not bool(v)))

		self._diffuse = QtGui.QCheckBox(self)
		self._diffuse.setText('Diffuse')
		self._diffuse.setCheckState(self.checkbox_init('Diffuse'))
		self._diffuse.stateChanged.connect(lambda v : SA.set_node_passed(SA.get_passed_nodelist('Diffuse', self.__node), not bool(v)))

		self._specular = QtGui.QCheckBox(self)
		self._specular.setText('Specular')
		self._specular.setCheckState(self.checkbox_init('Specular'))
		self._specular.stateChanged.connect(lambda v : SA.set_node_passed(SA.get_passed_nodelist('Specular', self.__node), not bool(v)))

		self._coat = QtGui.QCheckBox(self)
		self._coat.setText('Coat')
		self._coat.setCheckState(self.checkbox_init('Coat'))
		self._coat.stateChanged.connect(lambda v : SA.set_node_passed(SA.get_passed_nodelist('Coat', self.__node), not bool(v)))

		self._sss = QtGui.QCheckBox(self)
		self._sss.setText('SSS')
		self._sss.setCheckState(self.checkbox_init('SSS'))
		self._sss.stateChanged.connect(lambda v : SA.set_node_passed(SA.get_passed_nodelist('SSS', self.__node), not bool(v)))

		self._transmission = QtGui.QCheckBox(self)
		self._transmission.setText('Transmission')
		self._transmission.setCheckState(self.checkbox_init('Transmission'))
		self._transmission.stateChanged.connect(lambda v : SA.set_node_passed(SA.get_passed_nodelist('Transmission', self.__node), not bool(v)))

		self._checkgroup = QtGui.QGroupBox(self)
		self._checkgroup.setLayout(QtGui.QVBoxLayout())

		self._checkgroup.layout().addWidget(light_aov_parameterw)
		self._checkgroup.layout().addWidget(self._direct)
		self._checkgroup.layout().addWidget(self._indirect)
		self._checkgroup.layout().addWidget(self._diffuse)
		self._checkgroup.layout().addWidget(self._specular)
		self._checkgroup.layout().addWidget(self._coat)
		self._checkgroup.layout().addWidget(self._sss)
		self._checkgroup.layout().addWidget(self._transmission)

		#group layout
		self.__lightaovname = QtGui.QGroupBox(self)
		self.__lightaovname.setLayout(QtGui.QHBoxLayout())
		self.__lightaovname.layout().addWidget(self._checkgroup)
		self.__lightaovname.layout().addStretch()

		mainlayout = QtGui.QVBoxLayout()
		mainlayout.addWidget(self.__lightaovname)

		self.setLayout(mainlayout)

		# def set_pass(self, aovname):

	def checkbox_init(self, aov):
		state = 0
		list = SA.get_passed_nodelist(aov, self.__node)
		if list[0].isBypassed() == True:
			return state
		if list[0].isBypassed() == False:
			state = 2
			return state
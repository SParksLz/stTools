from Katana import NodegraphAPI, DrawingModule, Utils, PyXmlIO as XIO, UniqueName
import logging
import ScriptActions as SA
log = logging.getLogger('Light_AOV_X.Node')

direct = "'%s'"%('C[DSV]')
indirect = "'%s'"%('C[DSV][DSVOB].')
diffuse = "'%s'"%('C<RD>.')
specular = '"'+'%s'%("C<RS[^'coat']>.")+'"'
coat = '"'+'%s'%("C<RS'coat'>.")+'"'
transmission = "'%s'"%('C<TS>.')
sss = "'%s'"%('C<TD>.')
b1 = "'%s'"%('<L.')
b2 = "'%s'"%('>')
dd = '%s'%('"')+'%s'%("'")+'%s'%('"')
lightaov = 'self.getParent().Light_AOV_Name'

class Light_AOV_XNode(NodegraphAPI.SuperTool):

	def __init__(self):
		self.hideNodegraphGroupControls()
		self.getParameters().createChildString('Light_AOV_Name', '')
		self.addInputPort('In')
		self.addOutputPort('out')
		self.__buildDefaultNetwork()

	def __buildDefaultNetwork(self):

		Light_AOV_inputport = self.getSendPort('In')
		Light_AOV_outputport = self.getReturnPort('out')

		#ArnoldOutputChannelDefine
		direct_aocd_node = NodegraphAPI.CreateNode('ArnoldOutputChannelDefine', self)
		direct_aocd_node.setName('Direct_AOCD')
		dire_attr = SA.create_attr('Direct_', self)
		dire_tiled = SA.create_tiled('Direct_', self)
		# direct_aocd_node.getParameter('nodes.driverParameters.tiled.enable').setValue(1, 0)
		# direct_aocd_node.getParameter('nodes.driverParameters.tiled.value').setValue(1, 0)
		indirect_aocd_node = NodegraphAPI.CreateNode('ArnoldOutputChannelDefine', self)
		indirect_aocd_node.setName('Indirect_AOCD')
		indire_attr = SA.create_attr('Indirect_', self)
		indire_tiled = SA.create_tiled('Indirect_', self)

		diffuse_aocd_node = NodegraphAPI.CreateNode('ArnoldOutputChannelDefine', self)
		diffuse_aocd_node.setName('Diffuse_AOCD')
		diffuse_attr = SA.create_attr('Diffuse_', self)
		diffuse_tiled = SA.create_tiled('Diffuse_', self)

		specular_aocd_node = NodegraphAPI.CreateNode('ArnoldOutputChannelDefine', self)
		specular_aocd_node.setName('Specular_AOCD')
		specular_attr = SA.create_attr('Specular_', self)
		specular_tiled = SA.create_tiled('Specular_', self)

		coat_aocd_node = NodegraphAPI.CreateNode('ArnoldOutputChannelDefine', self)
		coat_aocd_node.setName('Coat_AOCD')
		coat_attr = SA.create_attr('Coat_', self)
		coat_tiled = SA.create_tiled('Coat_', self)

		sss_aocd_node = NodegraphAPI.CreateNode('ArnoldOutputChannelDefine', self)
		sss_aocd_node.setName('SSS_AOCD')
		sss_attr = SA.create_attr('SSS_', self)
		sss_tiled = SA.create_tiled('SSS_', self)

		transmission_aocd_node = NodegraphAPI.CreateNode('ArnoldOutputChannelDefine', self)
		transmission_aocd_node.setName('Transmission_AOCD')
		transmission_attr = SA.create_attr('Transmission_', self)
		transmission_tiled = SA.create_tiled('Transmission_', self)

		#renderoutputdefine
		direct_rod_node = NodegraphAPI.CreateNode('RenderOutputDefine', self)
		direct_rod_node.setName('Direct_ROD')
		indirect_rod_node = NodegraphAPI.CreateNode('RenderOutputDefine', self)
		indirect_rod_node.setName('Indirect_ROD')
		diffuse_rod_node = NodegraphAPI.CreateNode('RenderOutputDefine', self)
		diffuse_rod_node.setName('Diffuse_ROD')
		specular_rod_node = NodegraphAPI.CreateNode('RenderOutputDefine', self)
		specular_rod_node.setName('Specular_ROD')
		coat_rod_node = NodegraphAPI.CreateNode('RenderOutputDefine', self)
		coat_rod_node.setName('Coat_ROD')
		sss_rod_node = NodegraphAPI.CreateNode('RenderOutputDefine', self)
		sss_rod_node.setName('SSS_ROD')
		transmission_rod_node = NodegraphAPI.CreateNode('RenderOutputDefine',self)
		transmission_rod_node.setName('Transmission_ROD')


		# merge_rod_node = NodegraphAPI.CreateNode('RenderOutputDefine', self)
		# merge_rod_node.setName('Merge_ROD')

		#connect node
		SA.connect_node(direct_aocd_node, direct_rod_node)
		SA.connect_node(direct_rod_node, dire_attr)
		SA.connect_node(dire_attr, dire_tiled)
		SA.connect_node(dire_tiled, indirect_aocd_node)
		SA.connect_node(indirect_aocd_node, indirect_rod_node)
		SA.connect_node(indirect_rod_node, indire_attr)
		SA.connect_node(indire_attr, indire_tiled)
		SA.connect_node(indire_tiled, diffuse_aocd_node)
		SA.connect_node(diffuse_aocd_node, diffuse_rod_node)
		SA.connect_node(diffuse_rod_node, diffuse_attr)
		SA.connect_node(diffuse_attr, diffuse_tiled)
		SA.connect_node(diffuse_tiled, specular_aocd_node)
		SA.connect_node(specular_aocd_node, specular_rod_node)
		SA.connect_node(specular_rod_node, specular_attr)
		SA.connect_node(specular_attr, specular_tiled)
		SA.connect_node(specular_tiled, coat_aocd_node)
		SA.connect_node(coat_aocd_node, coat_rod_node)
		SA.connect_node(coat_rod_node, coat_attr)
		SA.connect_node(coat_attr, coat_tiled)
		SA.connect_node(coat_tiled, sss_aocd_node)
		SA.connect_node(sss_aocd_node, sss_rod_node)
		SA.connect_node(sss_rod_node, sss_attr)
		SA.connect_node(sss_attr, sss_tiled)
		SA.connect_node(sss_tiled, transmission_aocd_node)
		SA.connect_node(transmission_aocd_node, transmission_rod_node)
		SA.connect_node(transmission_rod_node, transmission_attr)
		SA.connect_node(transmission_rod_node, transmission_tiled)
		direct_aocd_node.getInputPortByIndex(0).connect(Light_AOV_inputport)
		transmission_tiled.getOutputPortByIndex(0).connect(Light_AOV_outputport)

		#set parameter value
		#aocd
		SA.set_aocd_parameter(direct_aocd_node, "'Direct'"+'+'+"'_'"+'+'+lightaov, "'Direct'"+'+'+"'_'"+'+'+lightaov, direct+'+'+b1+'+'+dd+'+'+lightaov+'+'+dd+'+'+b2)
		SA.set_aocd_parameter(indirect_aocd_node, "'Indirect'"+'+'+"'_'"+'+'+lightaov, "'Indirect'"+'+'+"'_'"+'+'+lightaov, indirect+'+'+b1+'+'+dd+'+'+lightaov+'+'+dd+'+'+b2)
		SA.set_aocd_parameter(diffuse_aocd_node, "'Diffuse'"+'+'+"'_'"+'+'+lightaov, "'Diffuse'"+'+'+"'_'"+'+'+lightaov, diffuse+'+'+b1+'+'+dd+'+'+lightaov+'+'+dd+'+'+b2)
		SA.set_aocd_parameter(specular_aocd_node, "'Specular'"+'+'+"'_'"+'+'+lightaov, "'Specular'"+'+'+"'_'"+'+'+lightaov, specular+'+'+b1+'+'+dd+'+'+lightaov+'+'+dd+'+'+b2)
		SA.set_aocd_parameter(coat_aocd_node, "'Coat'"+'+'+"'_'"+'+'+lightaov, "'Coat'"+'+'+"'_'"+'+'+lightaov, coat+'+'+b1+'+'+dd+'+'+lightaov+'+'+dd+'+'+b2)
		SA.set_aocd_parameter(sss_aocd_node, "'SSS'"+'+'+"'_'"+'+'+lightaov, "'SSS'"+'+'+"'_'"+'+'+lightaov, sss+'+'+b1+'+'+dd+'+'+lightaov+'+'+dd+'+'+b2)
		SA.set_aocd_parameter(transmission_aocd_node, "'Transmission'"+'+'+"'_'"+'+'+lightaov, "'Transmission'"+'+'+"'_'"+'+'+lightaov, transmission+'+'+b1+'+'+dd+'+'+lightaov+'+'+dd+'+'+b2)
		#rod
		SA.set_rod_parameter(direct_rod_node, "'Direct'"+'+'+"'_'"+'+'+lightaov, "'Direct'"+'+'+"'_'"+'+'+lightaov)
		SA.set_rod_parameter(indirect_rod_node, "'Indirect'"+'+'+"'_'"+'+'+lightaov, "'Indirect'"+'+'+"'_'"+'+'+lightaov)
		SA.set_rod_parameter(diffuse_rod_node, "'Diffuse'"+'+'+"'_'"+'+'+lightaov, "'Diffuse'"+'+'+"'_'"+'+'+lightaov)
		SA.set_rod_parameter(specular_rod_node, "'Specular'"+'+'+"'_'"+'+'+lightaov, "'Specular'"+'+'+"'_'"+'+'+lightaov)
		SA.set_rod_parameter(coat_rod_node, "'Coat'"+'+'+"'_'"+'+'+lightaov, "'Coat'"+'+'+"'_'"+'+'+lightaov)
		SA.set_rod_parameter(sss_rod_node, "'SSS'"+'+'+"'_'"+'+'+lightaov, "'SSS'"+'+'+"'_'"+'+'+lightaov)
		SA.set_rod_parameter(transmission_rod_node, "'Transmission'"+'+'+"'_'"+'+'+lightaov, "'Transmission'"+'+'+"'_'"+'+'+lightaov)


	def addParameterHints(self, attrName, inputDict):
		inputDict.update(_ExtraHints.get(attrName, {}))

_ExtraHints = {
	'Light_AOV_X.Light_AOV_Name':{
		'widget':'string',
	},
}
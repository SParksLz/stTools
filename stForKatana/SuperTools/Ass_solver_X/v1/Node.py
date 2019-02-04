from Katana import NodegraphAPI
import logging
import ScriptActions as ScriptActions

log = logging.getLogger('Ass_solver_X.Node')

class Ass_solver_XNode(NodegraphAPI.SuperTool):

	def __init__(self):
		self.hideNodegraphGroupControls()
		self.getParameters().createChildString('assFile_path', '')
		self.getParameters().createChildString('Ass_Location', '')
		self.getParameters().createChildString('to_location', '')
		self.getParameter('Ass_Location').setValue('/root/world/geo/ASS', 0)
		# self.getParameter('Ass_Location').setExpressionFlag(True)
		self.addOutputPort('out')
		self.addInputPort('in')
		self.__buildDefaultNetwork()



	def addParameterHints(self, attrName, inputDict):
		inputDict.update(_ExtraHints.get(attrName, {}))

	def __buildDefaultNetwork(self):
		ass_node_out = self.getReturnPort('out')
		ass_node_in = self.getSendPort('in')

		location_node = NodegraphAPI.CreateNode('LocationCreate', self)
		location_node.setName('%s' % (r'__ASS'))
		location_node.getParameter('locations.i0').setExpression('self.getParent().Ass_Location', 0)
		location_node.getParameter('locations.i0').setExpressionFlag(True)
		local_in = location_node.addInputPort('in')
		local_out = location_node.getOutputPortByIndex(0)

		ass_node_in.connect(local_in)

		# self.__group = NodegraphAPI.CreateNode('Group', self)
		# self.__group.setName('_AssFile')
		# group_out = self.__group.getOutputPortByIndex(0)
		# # G_input = self.__group.addInputPort('in')
		# G_output = self.__group.addOutputPort('out')
		# # G_send = self.__group.getSendPort('in')
		# G_return = self.__group.getReturnPort('out')
		# group_merge = NodegraphAPI.CreateNode('Merge', self.__group)
		# G_merge_out = group_merge.getOutputPortByIndex(0)
		# G_merge_out.connect(G_return)

		mergenode = NodegraphAPI.CreateNode('Merge', self)
		mergenode_out = mergenode.getOutputPortByIndex(0)
		merge_in = mergenode.addInputPort('i0')
		merge_in.connect(local_out)
		# merge_in_ii = mergenode.addInputPort('i1')
		# G_output.connect(merge_in_ii)

		hierachycope = NodegraphAPI.CreateNode('HierarchyCopy', self)
		# hierachycope.AddGroup()
		hierachycope._flushAll()
		hierachycope.getParameter('pruneSource').setValue(1.0, 0)
		hierachycope.getParameter('copies.copy1.sourceLocation').setExpression('self.getParent().Ass_Location', 0)
		hierachycope.getParameter('copies.copy1.sourceLocation').setExpressionFlag(True)
		hierachycope.getParameter('copies.copy1.destinationLocations.i0').setExpression('self.getParent().to_location', 0)
		hierachycope.getParameter('copies.copy1.destinationLocations.i0').setExpressionFlag(True)
		hierachy_in = hierachycope.getInputPortByIndex(0)
		hierachy_out = hierachycope.getOutputPortByIndex(0)
		mergenode_out.connect(hierachy_in)
		hierachy_out.connect(ass_node_out)

_ExtraHints = {
	'Ass_solver_X.assFile_path':{
		'widget':'assetIdInput',
		'dirsOnly':True
	},
	'Ass_solver_X.Ass_Location':{
		'widget':'scenegraphLocation',
	},
	'Ass_solver_X.to_location':{
		'widget':'scenegraphLocation',
	},
}
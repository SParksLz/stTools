# -*- coding: utf-8 -*-
# @Author: liuzhen
# @Date:   2018-07-27 11:01:41
# @Last Modified by:   liuzhen
# @Last Modified time: 2018-07-27 11:12:47
from Katana import NodegraphAPI, DrawingModule, Utils, PyXmlIO as XIO, UniqueName
import logging
import ScriptActions as SA
log = logging.getLogger('Solver_X.Node')

class Solver_XNode(NodegraphAPI.SuperTool):

	def __init__(self):
		self.hideNodegraphGroupControls()
		self.addOutputPort('out')
		self.getParameters().createChildString('Path','')
		self.__buildDefaultNetwork()


	def addParameterHints(self, attrName, inputDict):
		inputDict.update(_ExtraHints.get(attrName, {}))

	def __buildDefaultNetwork(self):
	 	mergenode = NodegraphAPI.CreateNode('Merge', self)
	 	#mergenode.setName('Merge_X')
	 	SA.AddNodeReferenceParam(self, 'node_merge', mergenode)
	 	mout = mergenode.getOutputPortByIndex(0)
	 	self.getReturnPort(self.getOutputPortByIndex(0).getName()).connect(mout)










_ExtraHints = {
    'Solver_X.Path':{
        'widget':'assetIdInput',
    },
}

import os
import logging
from Katana import NodegraphAPI, DrawingModule, Utils
log = logging.getLogger('dsMtlX_ResolveEditor')

def connect_node(node1, node2):
	output_port = node1.getOutputPortByIndex(0)
	input_port = node2.getInputPortByIndex(0)
	output_port.connect(input_port)

def set_aocd_parameter(aocdnode, name, channel, lpe):
	with NodegraphAPI.InteractiveContext():
		aocdnode.getParameter('type').setValue('RGB', 0)
		aocdnode.getParameter('name').setExpression('%s' %(name), 0)
		aocdnode.getParameter('name').setExpressionFlag(True)
		aocdnode.getParameter('channel').setExpression('%s' %(channel), 0)
		aocdnode.getParameter('channel').setExpressionFlag(True)
		aocdnode.getParameter('lightPathExpression').setExpression('%s' %(lpe), 0)
		aocdnode.getParameter('lightPathExpression').setExpressionFlag(True)
		aocdnode.flushAll()

def set_rod_parameter(rodnode, name, channel):
	rodnode.getParameter('outputName').setExpression('%s' %(name), 0)
	rodnode.getParameter('outputName').setExpressionFlag(True)
	with NodegraphAPI.InteractiveContext():
		rodnode.checkDynamicParameters()
		rodnode.getParameter('args.renderSettings.outputs.outputName.type.enable').setValue(1,0)
		rodnode.getParameter('args.renderSettings.outputs.outputName.type.value').setValue('color', 0)
		# rodnode.checkDynamicParameters()
		# rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.convertSettings.exrOptimize.enable').setValue(1,0)
		# rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.convertSettings.exrOptimize.value').setValue('No',0)
		rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.value').setExpression('%s' %(channel),0)
		rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.value').setExpressionFlag(True)
		rodnode.getParameter('args.renderSettings.outputs.outputName.rendererSettings.channel.enable').setValue(1, 0)

def create_attr(name, parent):
	attrnode = NodegraphAPI.CreateNode('AttributeSet', parent)
	attrnode.setName(name+'attr')
	attrnode.getParameter('paths.i0').setValue('/root',0)
	attrnode.getParameter('attributeName').setExpression("'"+'arnoldGlobalStatements.outputChannels.'+"'"+"+"+"self.getNodeName().split('_')[0]"+"+"+"'"+'_'+"'"+'+'+'self.getParent().Light_AOV_Name'+"+"+"'"+'.driverParameters.half_precision'+"'",0)
	attrnode.getParameter('attributeName').setExpressionFlag(True)
	attrnode.getParameter('attributeType').setValue('float',0)
	attrnode.getParameter('numberValue.i0').setValue(1.0,0)
	return attrnode
def create_tiled(name, parent):
	attrnode = NodegraphAPI.CreateNode('AttributeSet', parent)
	attrnode.setName(name+'exrOptimize')
	attrnode.getParameter('paths.i0').setValue('/root',0)
	attrnode.getParameter('attributeName').setExpression("'"+'renderSettings.outputs.'+"'"+"+"+"self.getNodeName().split('_')[0]"+"+"+"'"+'_'+"'"+'+'+'self.getParent().Light_AOV_Name'+"+"+"'"+'.rendererSettings.convertSettings.exrOptimize'+"'",0)
	attrnode.getParameter('attributeName').setExpressionFlag(True)
	attrnode.getParameter('attributeType').setValue('string',0)
	attrnode.getParameter('stringValue.i0').setValue('No',0)
	return attrnode
def get_passed_nodelist(aovname, parent):
		nodelist = parent.getChildren()
		X_node = []
		for i in nodelist :
			if i.getParent() == parent and i.getName().split('_')[0] == '%s' %(aovname):
				X_node.append(i)
		return X_node


def set_node_passed(nodelist,v):
        for i in nodelist:
                i.setBypassed(v)
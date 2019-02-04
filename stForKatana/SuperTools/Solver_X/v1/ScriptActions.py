# -*- coding: utf-8 -*-
# @Author: liuzhen
# @Date:   2018-07-27 11:01:41
# @Last Modified by:   liuzhen
# @Last Modified time: 2018-07-27 11:12:52
from Katana import NodegraphAPI, DrawingModule, Utils
import os
# import logging
# log = logging.getLogger('Solver_XEditor')

 
# class Xbase(object):
# 	def __init__(self, name, parent):
# 		self.__name = name
# 		self.__parent = parent
# 		self.__node = None

def GetRefNode(gnode, key):
    p = gnode.getParameter('node_'+key)
    if not p:
        return None
    
    return NodegraphAPI.GetNode(p.getValue(0))

def getmergenode(gnode):
	return GetRefNode(gnode, 'merge')

def AddNodeReferenceParam(destNode, paramName, node):
    param = destNode.getParameter(paramName)
    if not param:
        param = destNode.getParameters().createChildString(paramName, '')
    
    param.setExpression('getNode(%r).getNodeName()' % node.getName())

def X_dirpath():
	dir = os.path.dirname(__file__)
	return dir

def X_listdir(filepath):
	dir = os.listdir(filepath)
	return dir

def X_listdir_num(filepath):
	dir = os.listdir(filepath)
	num = len(dir)
	return num

def X_getVar(rootnode):
	return rootnode.getParameter('variables.myShot.value').getValue(0)
def X_varibleSolver(num, dir, rootnode):
	# dir = os.listdir(filepath)
	# num = len(dir)
	# print num
	rootnode.getParameter("variables").createChildGroup("myShot")
	rootnode.getParameter("variables.myShot").createChildNumber("enable",1)
	rootnode.getParameter("variables.myShot").createChildString("value","")

	rootnode.getParameter("variables.myShot").createChildStringArray("options",num)

	for i in range(num):
	        array = rootnode.getParameter("variables.myShot.options")
	        array.getChildByIndex(i).setValue("%s" %(dir[i]),0)

def X_getXml(filepath, curdir, parent):
	path = str(filepath)+'/'+str(curdir)
	file = os.listdir(path)
	mergenode = NodegraphAPI.CreateNode('Merge', parent)
	switchnode = NodegraphAPI.CreateNode('Switch', parent)
	supertool_path = os.path.dirname(__file__)
	lua_path = supertool_path+"/"+"test.lua"
	lua = open(lua_path)
	script = lua.read()
	lua.close()

	a = 'xml'
	for i in file:
		print i.split('.')[-1]
		if i.split('.')[-1] == a:
			xml_node = NodegraphAPI.CreateNode('ScenegraphXml_In', parent)
			xml_node.setName(i)
			print 'create node'
			xml_node_out = xml_node.getOutputPort('out')
			print 'add port'
			xml_node.getParameter('asset').setValue(filepath+'/'+curdir+'/'+i,0)
			print 'setvalue'
			#OpScript...
			op_node = NodegraphAPI.CreateNode('OpScript', parent)
			op_node.getParameter('CEL').setValue('xxxx',0)
			op_node.getParameter('script.lua').setValue(script,0)
			op_node_in = op_node.getInputPortByIndex(0)
			op_node_out = op_node.getOutputPort("out")
			miip = mergenode.addInputPort('i0')
			xml_node_out.connect(op_node_in)
			op_node_out.connect(miip)
	#Lod...
	for weight in range(2):
		Lod = NodegraphAPI.CreateNode('LodSelect', parent)
		Lod.getParameter('CEL').setValue('/root/world/geo//*', 0)
		Lod.getParameter('mode').setValue('by weight', 0)
		Lod.getParameter('selectionWeight').setValue(str(weight), 0)
		Lod_in = Lod.getInputPortByIndex(0)
		Lod_in.connect(mergenode.getOutputPortByIndex(0))
		Lod_out = Lod.getOutputPortByIndex(0)
		siip = switchnode.addInputPort('i0')
		Lod_out.connect(switchnode.getInputPortByIndex(weight))
	return switchnode.getOutputPortByIndex(0)
	# parent.getReturnPort('out').connect(switchnode.getOutputPortByIndex(0))
# def X_varResolve(filepath, num, dir, gnode):
# 	mergenode = NodegraphAPI.CreateNode('Merge', gnode)
# 	for i in dir:
# 		xml_node = NodegraphAPI.CreateNode('ScenegraphXml_In', gnode)
# 		xml_node_out = xml_node.getOutputPort('out')
# 		xml_node.getParameter('asset').setValue(filepath+'/'+dir[num]+'/',0)
# 		miip = mergenode.addInputPort('i0')
# 		xml_node_out.connect(miip)
def X_getAss(filepath, curdir, parent):
	path = str(filepath)+'/'+str(curdir)
	file = os.listdir(path)
	group = NodegraphAPI.CreateNode('Group', parent)
	group.addOutputPort('out')
	mergenode = NodegraphAPI.CreateNode('Merge',group)


	for i in file:
		if i.endswith('ass'):
			assnode = NodegraphAPI.CreateNode('ArnoldStandin', group)
			assnode.getParameter('filename').setValue(filepath+'/'+curdir+'/'+i,0)
			assout = assnode.getOutputPortByIndex(0)
			miip = mergenode.addInputPort('i0')
			assout.connect(miip)
	group.getReturnPort('out').connect(mergenode.getOutputPortByIndex(0))
	return group.getOutputPortByIndex(0)

def changeSwitch(num):
	parameter = NodegraphAPI.GetNode('Switch').getParameter('in')
	parameter.setValue('%s' %(num),0)

def X_getcam(filepath, curdir, parent):
	path = str(filepath)+'/'+str(curdir)
	file = os.listdir(path)
	cam_group = NodegraphAPI.CreateNode('Group', parent)
	cam_group.setName('Camera_Group')
	cam_group.addOutputPort('out')
	cam_mergenode = NodegraphAPI.CreateNode('Merge', cam_group)
	for cam in file:
		if cam.endswith('abc'):
			camnode = NodegraphAPI.CreateNode('Alembic_In', cam_group)
			camnode.getParameter('abcAsset').setValue(filepath+'/'+curdir+'/'+cam,0)
			camout = camnode.getOutputPortByIndex(0)
			cmiip = cam_mergenode.addInputPort('i0')
			camout.connect(cmiip)
	cam_group.getReturnPort('out').connect(cam_mergenode.getOutputPortByIndex(0))
	return cam_group.getOutputPortByIndex(0)
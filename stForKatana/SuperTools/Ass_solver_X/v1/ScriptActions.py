from Katana import NodegraphAPI
import os

def folderlist_sovler(path):
	folder_path = path
	folderlist = os.listdir(folder_path)
	return folderlist

def create_group(path, parent):
	folderlist = folderlist_sovler(path)
	listX = []
	port_list = []
	node_list = []
	if folderlist:
		for folder in folderlist:
			group = NodegraphAPI.CreateNode('Group', parent)
			group.setName('arnoldstandin_%s' % (folder))
			group_out = group.addOutputPort('out')
			port_list.append(group_out)
			node_list.append(group)
			mergenode = NodegraphAPI.CreateNode('Merge', group)
			merge_out = mergenode.getOutputPortByIndex(0)
			merge_out.connect(group.getReturnPort('out'))
		listX = [port_list, node_list]
	return listX


def file_classify(path):
	filelist = os.listdir(path)
	file_classlist = [x.split('.')[0] for x in filelist if x.endswith('.ass')]
	file_classlist = list(set(file_classlist))
	return file_classlist

def Createnode(parent, path):
	result = ''
	listpath = os.listdir(path)
	folder_list = []
	folder_file = []
	for folder in listpath:
		#Set Group node
		if folder.endswith('.abc'):
			abc_in = NodegraphAPI.CreateNode('Alembic_In', parent)
			abc_in.setName('%s'%(folder))
			abc_in.getParameter('abcAsset').setValue(path+folder,0)
			abc_in.getParameter('name').setExpression('self.getParent().Ass_Location'+"+"+"'"+'/Guides'+"'")
			abc_in.getParameter('name').setExpressionFlag(True)
			abc_outport = abc_in.getOutputPortByIndex(0)
			va = NodegraphAPI.CreateNode('VisibilityAssign', parent)
			va.getParameter('CEL').setExpression('self.getParent().Ass_Location'+"+"+"'"+'/Guides'+"'")
			va.getParameter('CEL').setExpressionFlag(True)
			va.getParameter('args.visible.value').setValue(0,0)
			va.getParameter('args.visible.enable').setValue(1,0)
			va_input = va.getInputPortByIndex(0)
			va_output = va.getOutputPortByIndex(0)
			main_merge = get_mergenode(parent)
			main_port = main_merge.addInputPort('i0')
			abc_outport.connect(va_input)
			va_output.connect(main_port)



		else:
			Group_node_x = NodegraphAPI.CreateNode('Group', parent)
			Group_node_x.setName('%s' % (folder))
			group_port_v1 = Group_node_x.addOutputPort('out')
			group_port_v2 = Group_node_x.getReturnPort('out')
			merge_inside = NodegraphAPI.CreateNode('Merge', Group_node_x)
			inside_port = merge_inside.getOutputPortByIndex(0)
			inside_port.connect(group_port_v2)
			main_merge = get_mergenode(parent)
			main_port = main_merge.addInputPort('i0')
			main_port.connect(group_port_v1)
			#assfile
			path_x = path + '%s' % (folder)
			a = file_classify(path_x)
			print 'a:%s' %(a)
			allfile = os.listdir(path_x)
			for class_x in a:
				folder_file = [file for file in allfile if file.split('.')[0] == class_x]
				folder_list.append(folder_file)
				print folder_file
				# print folder_list
				# for fileclass in a:
				# 	print fileclass
				# 	print len(fileclass)
				if len(folder_file) == 1:
					createassnode(Group_node_x, path+'/%s/' % (folder), class_x, 'lookfile')
				else:
					createassnode(Group_node_x, path+'/%s/' % (folder), class_x, 'sequence')


def detect_nodes(parent):
	all_arnoldstandin = [x.getName() for x in NodegraphAPI.GetAllNodesByType('ArnoldStandin')
						 if x.getParent() == parent]

	return all_arnoldstandin

def get_mergenode(groupnode):

	children = groupnode.getChildren()
	for child in children:
		if child.getType() == 'Merge':
			return child

def createassnode(parent, path, name, result):
	if result == 'lookfile':
		print 'lookfile'
		filepath = "'"+'%s%s.ass' % (path, name) +"'"

		#Arnold Standin
		arstandin = NodegraphAPI.CreateNode('ArnoldStandin', parent)
		arstan_out = arstandin.getOutputPortByIndex(0)
		arstandin.setName('%s_lookfile' %(name))
		arstandin.getParameter('location').setExpression('(self.getParent()).getParent().Ass_Location'+'+'+"'/'"+"'%s'" %(name), 0)
		arstandin.getParameter('location').setExpressionFlag(True)
		arstandin.getParameter('filename').setExpression(filepath, 0)
		arstandin.getParameter('filename').setExpressionFlag(True)

		mergenode = get_mergenode(parent)
		merge_in = mergenode.addInputPort('i0')
		merge_in.connect(arstan_out)

	elif result == 'sequence':
		print 'sequence'
		filepath = "'"+'%s%s' % (path, name) + r'.%04d.ass' + "'"+r" %(frame)"
		arstandin = NodegraphAPI.CreateNode('ArnoldStandin', parent)
		arstan_out = arstandin.getOutputPortByIndex(0)
		arstandin.setName('%s_sequence' %(name))
		arstandin.getParameter('location').setExpression('(self.getParent()).getParent().Ass_Location'+'+'+"'/'"+"'%s'" %(name), 0)
		arstandin.getParameter('location').setExpressionFlag(True)
		arstandin.getParameter('filename').setExpression(filepath, 0)
		arstandin.getParameter('filename').setExpressionFlag(True)

		mergenode = get_mergenode(parent)
		merge_in = mergenode.addInputPort('i0')
		merge_in.connect(arstan_out)

def getGroupnode(parent):
	groupnodelist = [x for x in parent.getChildren() if x.getType() == 'Group']
	return groupnodelist

def getStandinnode(parent):
	groupnodelist = [x for x in parent.getChildren() if x.getType() == 'ArnoldStandin']
	return groupnodelist
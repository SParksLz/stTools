import hou


class node(object) :
    def __init__(self, nodePath):
        self.nodePath = nodePath
        self.node = hou.node(nodePath)






def sortNodeList(nodeList) :
    nodeList = [hou.node(i) for i in nodeList]
    # print nodeList
    nodeList.sort(key=getSopNodePrimNum, reverse=True)
    # print list_sorted
    # for node in nodeList :
    #     print getSopNodePrimNum(node)
    return nodeList

def getSopNodePrimNum(node) :
    geo = node.geometry()
    primNum = len(geo.prims())
    return primNum

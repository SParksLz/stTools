import hou



class node(object) :
    def __init__(self, nodePath):
        self.nodePath = nodePath
        self.node = hou.node(nodePath)



